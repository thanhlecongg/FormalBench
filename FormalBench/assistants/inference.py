from .state import State
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import system, human, ai
from .assistants import GenerationAssistant
import os
from ..evaluation.tools.verifier import create_verifier
from .utils import _print_event
import torch
import gc
from .example import *
from . import config
import re

def contains_annotations(java_code):
    # Split the code into lines
    lines = java_code.splitlines()
    
    # Flag to track if we are inside a block comment
    inside_block_comment = False
    
    # Regex patterns for detecting JML annotations
    single_line_jml_pattern = re.compile(r"^\s*//@.*")  # Detects //@ comments
    block_comment_start_pattern = re.compile(r"^\s*/\*@")  # Detects start of /*@ block
    block_comment_end_pattern = re.compile(r"\s*\*/")  # Detects end of */ block
    
    for line in lines:
        # Check if the line matches a single-line JML comment
        if single_line_jml_pattern.match(line):
            return True
        
        # Check if we are entering or inside a block comment
        if inside_block_comment:
            if block_comment_end_pattern.match(line):
                inside_block_comment = False
        elif block_comment_start_pattern.match(line):
            inside_block_comment = True
            return True  # Block comment with JML found, return True immediately

    return False  # No JML annotations found

class SpecInfer():
    def __init__(
            self, 
            workflow="basic", 
            language="java", 
            model_name="deepseekv3", 
            use_docker=True, 
            prompt_type="zero_shot", 
            timeout=300,
            tmp_dir=None
        ):
        self.state = State()
        self.model_name = model_name
        self.timeout = timeout
        
        if tmp_dir is not None:
            self.tmp_dir = tmp_dir
        else:
            self.tmp_dir = os.path.join(os.path.join(os.getcwd(), "tmp/"), model_name)
        os.makedirs(self.tmp_dir, exist_ok=True)
                
        if language == "java":
            if workflow != "only_gen":
                if use_docker:
                    self.verifier = create_verifier("OpenJML")
                else:
                    self.verifier = create_verifier("OpenJMLWithoutDocker")
            
            if prompt_type == "two_shot":
                self.gen_sys_mes = (
                    "You are an expert in Java Modeling Language (JML). "
                    "You will be provided with Java code snippets. "
                    "Your task is to generate JML specifications for the given Java code. "
                    "The specifications should be written as annotations within the Java code and must be compatible with the OpenJML tool for verification. "
                    "Ensure the specifications include detailed preconditions, postconditions, necessary loop invariants, invariants, assertions, and any relevant assumptions."
                    "Please also adhere to the following syntax guidelines for JML:\n"
                    "JML text is written in comments that either:\n"
                    "a) begin with //@ and end with the end of the line, or\n"
                    "b) begin with /*@ and end with */. Lines within such a block comment may have the first non-whitespace characters be a series of @ symbols\n"
                )
            else:
                self.gen_sys_mes = (
                    "You are an expert in Java Modeling Language (JML). "
                    "You will be provided with Java code snippets."
                    "Your task is to generate JML specifications for the given Java code. "
                    "The specifications should be written as annotations within the Java code and must be compatible with the OpenJML tool for verification. "
                    "Ensure the specifications include detailed preconditions, postconditions, necessary loop invariants, invariants, assertions, and any relevant assumptions. "
                    
                )
                
            self.language = "java"
            self.spec_language = "JML"
            self.gen_query = "Please generate JML specifications for the provided Java code." 
            self.example_set = JavaExample
        elif language == "c":
            if workflow != "only_gen":
                assert use_docker, "FramaC without docker is not implemented yet. Please use FramaC with docker."
                self.verifier = create_verifier("FramaC")
            
            if prompt_type == "two_shot":
                self.gen_sys_mes = (
                    "You are an expert in Frama-C. "
                    "You will be provided with C code snippets. "
                    "Your task is to generate ACSL specifications for the given C code. "
                    "The specifications should be written as annotations within the C code and must be compatible with the Frama-C tool for verification. "
                    "Ensure the specifications include detailed preconditions, postconditions, necessary loop invariants, invariants, assertions, and any relevant assumptions. "
                    "Also, ensure that necessary #include are maintained from the original code. "
                    "Please adhere to the following syntax guidelines for ACSL: "
                    "Specification language text is placed inside special C comments; its lexical structure mostly follows that of ANSI/ISO C."
                )
            else:  
                self.gen_sys_mes = (
                    "You are an expert in Frama-C. "
                    "You will be provided with C code snippets. "
                    "Your task is to generate ACSL specifications for the given C code. "
                    "The specifications should be written as annotations within the C code and must be compatible with the Frama-C tool for verification. "
                    "Ensure the specifications include detailed preconditions, postconditions, necessary loop invariants, invariants, assertions, and any relevant assumptions. "
                    "Also, ensure that necessary #include are maintained from the original code."
                )
            self.language = "c"
            self.spec_language = "ACSL"
            self.gen_query = "Please generate ACSL specifications for the provided C code." 
            self.example_set = CExample
        else:
            raise ValueError(
                f"Currently, we only Java and C language are supported. Please select 'java' or 'c' as the language."
            )
        self.prompt_type = prompt_type
        self.workflow_name = workflow
        
        if workflow == "basic":
            self.workflow = self.basic_workflow()
        elif workflow == "only_gen":
            self.workflow = self.only_gen_workflow()
        else:
            return NotImplementedError(f"Workflow {workflow} not implemented")
        
        self.generator = GenerationAssistant(prompt_type=self.prompt_type, model_name=self.model_name)
        
    def gen_init_spec(self, state: State, config: RunnableConfig = None):
        new_state = state
        new_state["n_iters"] += 1
        
        try:
            new_state["first_spec"], new_messages = self.generator.__call__(state, config=config)
        except torch.OutOfMemoryError:
            for item in gc.garbage:
                del item
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            new_state["first_spec"] = None
            new_messages = []

        new_state["curr_spec"] = new_state["first_spec"]
        new_state["messages"] = new_messages
        return new_state

    def verify_specs(self, state: State, config: RunnableConfig = None):
        new_state = state
        curr_spec = state.get("curr_spec")
        if curr_spec is None:
            curr_spec = state["first_spec"]
        
        if new_state.get("analysis_results") is None:
            new_state["analysis_results"] = []
            
        if curr_spec is None:
            print("OOM")
            new_state["analysis_results"].append((-2, "OOM", None))
            return new_state
        
        if len(curr_spec) == 0:
            print("Empty specification")
            new_state["analysis_results"].append((-3, "Empty specification", None))
            return new_state

        class_name = state["class_name"]
        language = state["lang"]
        tmp_path = os.path.join(self.tmp_dir, f"{class_name}.{language}")
        with open(tmp_path, "w") as f:
            if self.language == "c" and "#include <limits.h>" not in curr_spec:
                f.write("#include <limits.h>\n")
            f.write(curr_spec)
        
        is_valid = contains_annotations(curr_spec)
        if not is_valid:
            print("Invalid JML annotations")
            new_state["analysis_results"].append((-4, "Invalid JML annotations", curr_spec))
            return new_state

        n_errors, output = self.verifier.verify(tmp_path, timeout=self.timeout)
        new_state["analysis_results"].append((n_errors, output, curr_spec))
        return new_state

    def analysis_condition(self, state: State):
        n_errors, _, _ = state["analysis_results"][-1]
        if n_errors == 0:
            print("Verification successful !!!")
            return "verified"

        print("Verification failed !!!")
        return "failed"

    def basic_workflow(self):
        builder = StateGraph(State)
        builder.add_node("gen_init_spec", self.gen_init_spec)
        builder.add_node("verify_specs", self.verify_specs)
        builder.add_edge(START, "gen_init_spec")
        builder.add_edge("gen_init_spec", "verify_specs")
        builder.add_conditional_edges("verify_specs", self.analysis_condition,
                                      {
                                          "verified": END,
                                          "failed": END
                                      })
        memory = MemorySaver()
        workflow = builder.compile(checkpointer=memory)

        return workflow
    
    def only_gen_workflow(self):
        builder = StateGraph(State)
        builder.add_node("gen_init_spec", self.gen_init_spec)
        builder.add_edge(START, "gen_init_spec")
        builder.add_edge("gen_init_spec", END)
        memory = MemorySaver()
        workflow = builder.compile(checkpointer=memory)

        return workflow

    def stream_query(self, query: dict, config: dict, verbose=True):
        _printed = set()
        events = self.workflow.stream(query, config, stream_mode="values")
        for event in events:
            if verbose:
                _print_event(event, _printed)
                            
        last_event = event
        return last_event

    def generate(self, code: str, class_name: str, config: dict, verbose=True):
        print(f"Generating specifications for {class_name} ...")
        if self.prompt_type in ["fs_ltm"]:
            example_code1 = self.example_set.EXAMPLE_CODE2
            example_code2 = self.example_set.EXAMPLE_CODE3
            example_spec1 = self.example_set.EXAMPLE_LTM_RESPONSE2
            example_spec2 = self.example_set.EXAMPLE_LTM_RESPONSE3
        else:
            example_code1 = self.example_set.EXAMPLE_CODE1
            example_code2 = self.example_set.EXAMPLE_CODE2
            example_spec1 = self.example_set.EXAMPLE_SPEC1
            example_spec2 = self.example_set.EXAMPLE_SPEC2
        
        query = {
            "gen_sys_mes": self.gen_sys_mes,
            "messages": [],
            "gen_query": self.gen_query,
            "class_name": class_name,
            "lang": self.language,
            "spec_lang": self.spec_language,
            "n_iters": 0,
            "code": code,
            "example_code1": example_code1,
            "example_code2": example_code2,
            "example_spec1": example_spec1,
            "example_spec2": example_spec2,
            
        }
        
        last_event = self.stream_query(query, config, verbose=verbose)
        messages = []
        for idx, mess in enumerate(last_event["messages"]):
            if type(mess) == system.SystemMessage:
                role = "system"
            elif type(mess) == human.HumanMessage:
                role = "human"
            elif type(mess) == ai.AIMessage:
                role = "ai"
            else:
                raise ValueError(f"Unknown message type: {type(mess)}")
            
            messages.append({
                "idx": idx,
                "response": mess.content,
                "response_metadata": mess.response_metadata,
                "role": role
            })

        if self.workflow_name == "basic":
            analysis_results =  last_event["analysis_results"]
            last_error = analysis_results[-1][0]
            if last_error == 0:
                status = "verified"
            elif last_error > 0:
                status = "failed"
            elif last_error == -1:
                status = "timeout"
            elif last_error == -2:
                status = "OOM"
            elif last_error == -3:
                status = "empty_spec"
            elif last_error == -4:
                status = "invalid_jml"
            elif last_error == -5:
                status = "internal_error"
            else:
                raise ValueError(f"Unknown error code: {last_error}")
            
            results = {
                "analysis_results": analysis_results,
                "spec": last_event["curr_spec"],
                "status": status,
                "messages": messages
            }
        elif self.workflow_name == "only_gen":
            results = {
                "spec": last_event["first_spec"],
                "messages": messages
            }
        
        print("Specifications generated !!!")
        return results

