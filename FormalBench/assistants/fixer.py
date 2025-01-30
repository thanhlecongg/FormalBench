from .state import FixingState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import system, human, ai
from .assistants import FixingAssistant
import os
from ..evaluation import create_verifier
from .utils import _print_event
import torch
import gc
from .example import _GUIDANCE
from FormalBench.assistants.failure_analysis import extract_errors, classify_failures
from . import config
import re

_ERROR_INFO_TEMPLATE = """
- Error Type: {error_type}
{error_description}
{fix_instructions}

"""
def contains_jml_annotations(java_code):
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

def analyze_failures(error_message):
    error_set = set()
    if "NOT IMPLEMENTED:" in error_message:
        if "\sum" in error_message or "\\num_of" in error_message or "\product" in error_message:
            error_set.add("UnsupportedSumNumOfProductQuantifierExpression")
        if "\min" in error_message or "\max" in error_message:
            error_set.add("UnsupportedMinMaxQuantifierExpression")
    else:
        errors = extract_errors(error_message)
            
        for level, error in errors:
            failure_type = classify_failures(level, error)
            if failure_type is not None:
                error_set.add(failure_type)
    error_info = ""
    for error in error_set:
        error_info += _ERROR_INFO_TEMPLATE.format(
            error_message=error_message,
            error_type=error,
            error_description=_GUIDANCE[error]["description"],
            fix_instructions=_GUIDANCE[error]["guidance"]
        )

    
    return error_info
        


    
    
class SpecFixer():

    def __init__(
            self, 
            workflow="SpecGen", 
            language="java", 
            max_iters=3, 
            model_name="gpt-3.5-turbo", 
            use_docker=False, 
            timeout=300,
            tmp_dir=None
        ):
        self.state = FixingState()
        self.workflow = self.basic_workflow()
        self.max_iters = max_iters
        self.model_name = model_name
        self.timeout = timeout
        if tmp_dir is not None:
            self.tmp_dir = tmp_dir
        else:
            self.tmp_dir = os.path.join(os.path.join(os.getcwd(), "tmp/"), model_name)
        os.makedirs(self.tmp_dir, exist_ok=True)
                
        if language == "java":
            if use_docker:
                self.verifier = create_verifier("OpenJML")
            else:
                self.verifier = create_verifier("OpenJMLWithoutDocker")
              
            self.fix_sys_mes = "You are an experts on Java Modeling Language (JML). Your task is to fix the JML specifications annotated in the target Java code." \
                            +  "You will be provided the error messages from the OpenJML tool and you need to fix the specifications accordingly."

            self.language = "java"
            self.spec_language = "JML"

        elif language == "c":
            raise NotImplementedError("C language is not supported yet")
        else:
            raise ValueError(
                f"Unsupported language: {language}. Please select either 'java' or 'c'"
            )

        if workflow == "basic":
            self.workflow = self.basic_workflow()
        else:
            return NotImplementedError(f"Workflow {workflow} not implemented")
        
        self.fixer = FixingAssistant(model_name=model_name, language=language)
        
    def fix_spec(self, state: FixingState, config: RunnableConfig = None):
        new_state = state
        
        state["curr_error"] = state["analysis_results"][-1][1]
        error_info = analyze_failures(state["curr_error"])
        state["error_info"] = error_info
        new_state["n_iters"] += 1

        try:
            new_state["curr_spec"], new_messages = self.fixer.__call__(state, config=config)
        except torch.OutOfMemoryError:
            for item in gc.garbage:
                del item
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            new_state["curr_spec"] = None
            new_messages = []

        new_state["messages"] = new_messages
        return new_state

    def verify_specs(self, state: FixingState, config: RunnableConfig = None):
        new_state = state
        curr_spec = state.get("curr_spec")
        
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
            f.write(curr_spec)
        
        is_valid = contains_jml_annotations(curr_spec)
        if not is_valid:
            print("Invalid JML annotations")
            new_state["analysis_results"].append((-4, "Invalid JML annotations", curr_spec))
            return new_state

        n_errors, output = self.verifier.verify(tmp_path, timeout=self.timeout)
        new_state["analysis_results"].append((n_errors, output, curr_spec))
        return new_state

    def analysis_condition(self, state: FixingState):
        n_errors, _, _ = state["analysis_results"][-1]
        if n_errors == 0:
            print("Verification successful !!!")
            return "verified"
        
        if n_errors < 0:
            print("Verification failed !!!")
            return "out_of_scope"

        if state["n_iters"] >= state["max_iters"]:
            print("Maximum iterations reached !!!")
            return "max_iters_reached"
        
        assert n_errors > 0
        print("Verification failed !!!")
        return "failed"

    def basic_workflow(self):
        builder = StateGraph(FixingState)
        builder.add_node("fix_spec", self.fix_spec)
        builder.add_node("verify_specs", self.verify_specs)
        builder.add_edge(START, "fix_spec")
        builder.add_edge("fix_spec", "verify_specs")
        builder.add_conditional_edges("verify_specs", self.analysis_condition,
                                      {
                                          "verified": END,
                                          "failed": END,
                                          "out_of_scope": END,
                                      })
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

    def repair(self, original_spec: str, original_analysis_results, class_name: str, config: dict, verbose=True):
        print(f"Repairing the specification for class: {class_name}")
        query = {
            "messages": [],
            "class_name": class_name,
            "lang": self.language,
            "spec_lang": self.spec_language,
            "max_iters": self.max_iters,
            "fix_sys_mes": self.fix_sys_mes,
            "n_iters": 0,
            "curr_spec": original_spec,
            "first_spec": original_spec,
            "analysis_results": [original_analysis_results],
            "first_error": original_analysis_results[1],
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
        return results

