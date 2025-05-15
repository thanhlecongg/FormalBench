from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from abc import ABC
from .state import State
import re
import json
from langchain_core.messages.human import HumanMessage
from .utils import update_messages
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
import torch
from transformers import BitsAndBytesConfig
import os

def create_llm(model_name: str):
    if model_name == "gpt-3.5-turbo":
        print("Using gpt-3.5-turbo")
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
        )
    elif model_name == "gpt-4o":
        print("Using gpt-4o")
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
        )
    elif model_name == "o1-mini":
        return ChatOpenAI(
            model="o1-mini",
        )
    elif model_name == "o3-mini":
        return ChatOpenAI(
            model="o3-mini",
        )
    elif model_name == "o3-mini-high":
        return ChatOpenAI(
            model="o3-mini",
            reasoning_effort="high"
        )
    elif model_name == "o3-mini-low":
        return ChatOpenAI(
            model="o3-mini",
            reasoning_effort="low",
        )
    elif model_name == "claude":
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0.7
        )
    elif model_name == "deepseekv3":
        return ChatOpenAI(
            model="deepseek-chat", 
            api_key=os.environ.get("DEEPSEEK_API_KEY"), 
            base_url="https://api.deepseek.com/v1",
            temperature=0.7
        )
    elif model_name in ["Qwen/CodeQwen1.5-7B-Chat"]:
        llm = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text-generation",
            pipeline_kwargs=dict(
                do_sample=True,
                max_new_tokens=1024,
                temperature=0.7,
            ),
            model_kwargs=dict(
                trust_remote_code=True,
            ),
        )
        return ChatHuggingFace(llm=llm)
    elif model_name in ["Qwen/Qwen2.5-Coder-32B-Instruct", "codellama/CodeLlama-34b-Instruct-hf", "deepseek-ai/deepseek-coder-33b-instruct", "deepseek-ai/DeepSeek-R1-Distill-Llama-70B", "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "Qwen/Qwen2.5-32B", "Qwen/Qwen2.5-72B", "meta-llama/Meta-Llama-3-70B-Instruct"]:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype="float16",
            bnb_4bit_use_double_quant=True,
        )
        llm = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text-generation",
            pipeline_kwargs=dict(
                do_sample=True,
                max_new_tokens=2048,
                temperature=0.7,
            ),
            model_kwargs=dict(
                quantization_config=quantization_config,
            ),
        )

        return ChatHuggingFace(llm=llm)
        
    else:
        raise ValueError(f"Unsupported model: {model_name}")
        
def get_specs_from_response(response: str, language: str) -> str:
    if "---------------" in response:
        response_lines = response.split("\n")
        new_response = []
        is_start = False
        for line in response_lines:
            if line.startswith("---------------"):
                is_start = not is_start
                continue
            if is_start:
                new_response.append(line)
        response = "\n".join(new_response)
    
    if "<|im_start|>assistant" in response:
            ### Using CodeQwen
            response = response.split("<|im_start|>assistant")[-1]
            response = response.split("<|im_end|>")[0]
    
        
    if "<｜Assistant｜><think>" in response:
        ### Using DeepSeek-r1
        response = response.split("<｜Assistant｜><think>")[-1]
        response = response.split("<｜/think｜>")[0]
    
    if "### SPECIFICATION" in response:
        response = response.split("### SPECIFICATION")[-1]
    
    if "### FIXED SPECIFICATION" in response:
        response = response.split("### FIXED SPECIFICATION")[-1]
        
    if "### RESPONSE" in response:
        response = response.split("### RESPONSE")[-1]
    
    if "[/INST]" in response:
        ### Using CodeLLama
        response = response.split("[/INST]")[-1]
    
    if "### Response:" in response:
        ### Using DeepSeek
        response = response.split("### Response:")[-1]
        
    if "```" not in response:
        return response.strip()

    if f"```{language}" in response:
        pattern = rf'```{language}(.*?)```'
    else:
        pattern = r'```(.*?)```'

    code_blocks = re.findall(pattern, response, re.DOTALL)
    return '\n// block\n'.join(code_blocks)

class Assistant(ABC):

    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self,
                 state: State,
                 config: RunnableConfig,
                 max_attempt: int = 3):
        new_messages = []
        while max_attempt >= 0:
            formatted_prompt = self.prompt_template.invoke(state)
            new_messages += formatted_prompt.to_messages()
            result = self.llm.invoke(formatted_prompt)
            new_messages.append(result)
            if not result.tool_calls and (
                    not result.content or isinstance(result.content, list)
                    and not result.content[0].get("text")):
                message = HumanMessage(
                    content="Invalid response from the model. Please try again."
                )
                state = update_messages(state, message)
                new_messages.append(message)
                max_attempt -= 1
            else:
                break

        return result, new_messages


class GenerationAssistant(Assistant):
    
    def _create_prompt(self, prompt_type, model_name): 
        if model_name == "o1-mini":
            system_role = "user"
        else:
            system_role = "system"
        
        if prompt_type == "zero_shot":
            return ChatPromptTemplate.from_messages([
                (
                    system_role,
                    "{gen_sys_mes}",
                ), 
                (
                    "human", 
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{code}\n\n"
                )
                ]
            )
        elif prompt_type == "zs_cot":
            return ChatPromptTemplate.from_messages([
                (
                    system_role,
                    "{gen_sys_mes}",
                ), 
                (
                    "human", 
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{code}\n"
                    "Let's think step by step !\n\n"
                )
                ]
            )
        elif prompt_type == "fs_cot":
            return ChatPromptTemplate.from_messages([
                (
                    system_role,
                    "{gen_sys_mes}",
                ), 
                (
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{example_code1}\n\n"
                    "### RESPONSE\n"
                ),
                (
                    "assistant",
                    "{example_spec1}\n\n"
                ),
                (   
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{example_code2}\n\n"
                    "### RESPONSE\n"
                ),
                (
                    "assistant",
                    "{example_spec2}\n\n"
                ),
                (
                    "human", 
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{code}\n\n"
                    "Let's think step by step !\n\n"
                )
                ])
        elif prompt_type == "two_shot":
            return ChatPromptTemplate.from_messages([
                (
                    system_role,
                    "{gen_sys_mes}",
                ), 
                (
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{example_code1}\n\n"
                    "### SPECIFICATION\n"
                ),
                (
                    "assistant",
                    "{example_spec1}\n\n"
                ),
                (   
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{example_code2}\n\n"
                    "### SPECIFICATION\n"
                ),
                (
                    "assistant",
                    "{example_spec2}\n\n"
                ),
                (
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{code}\n\n"
                    "### SPECIFICATION\n"
                )
                ]
                )
        elif prompt_type == "fs_ltm":
            return ChatPromptTemplate.from_messages([
                (
                    system_role,
                    "{gen_sys_mes}",
                ), 
                (
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{example_code1}\n\n"
                    "Let's break down this problem:\n"
                    "1. What are the weakest preconditions for the code? Be sure to include preconditions related to nullness and arithmetic bounds.\n"
                    "2. What are the strongest postconditions for the code?\n"
                    "3. What necessary specifications are required to prove the above post-conditions? This includes loop invariants, assertions, assumptions, and ranking functions.\n"
                    "After answering these questions, let's generate the specifications for the code and provide solution after `### SPECIFCIATION'\n"
                ),
                (
                    "assistant",
                    "### RESPONSE\n"
                    "{example_spec1}\n\n"
                ),
                (   
                    "human",
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{example_code2}\n\n"
                    "Let's break down this problem:\n"
                    "1. What are the weakest preconditions for the code? Be sure to include preconditions related to nullness and arithmetic bounds.\n"
                    "2. What are the strongest postconditions for the code?\n"
                    "3. What necessary specifications are required to prove the above post-conditions? This includes loop invariants, assertions, assumptions, and ranking functions.\n"
                    "After answering these questions, let's generate the specifications for the code and provide solution after `### SPECIFCIATION'\n"
                ),
                (
                    "assistant",
                    "### RESPONSE\n"
                    "{example_spec2}\n\n"
                ),
                (
                    "human", 
                    "{gen_query}\n\n"
                    "### CODE\n"
                    "{code}\n\n"
                    "Let's break down this problem:\n"
                    "1. What are the weakest preconditions for the code? Be sure to include preconditions related to nullness and arithmetic bounds.\n"
                    "2. What are the strongest postconditions for the code?\n"
                    "3. What necessary specifications are required to prove the above post-conditions? This includes loop invariants, assertions, assumptions, and ranking functions.\n"
                    "After answering these questions, let's generate the specifications for the code and provide solution, written between triple backquotes, after `### SPECIFCIATION' \n"
                )
                ])
        else:
            raise ValueError("Invalid prompt type")
    
    def __init__(self, model_name: str, prompt_type: str = False):
        self.prompt_template = self._create_prompt(prompt_type, model_name)
        self.llm = create_llm(model_name)

    def __call__(self,
                 state: State,
                 config: RunnableConfig = None,
                 max_attempt: int = 3):
        res, new_messages = Assistant.__call__(self, state, config=config, max_attempt=max_attempt)
        spec = get_specs_from_response(res.content, state["lang"])
        return spec, new_messages
    
class FixingAssistant(Assistant):

    def _create_prompt(self, model_name): 
        if model_name == "o1-mini":
            system_role = "user"
        else:
            system_role = "system"
        
        return ChatPromptTemplate.from_messages([
                (
                    system_role,
                    "{fix_sys_mes}",
                ),
                ("placeholder", "{fixing_messages}"),
                ("human", 
                "The following Java code is annotated with JML specifications:\n"
                "```\n"
                "{curr_spec}\n"
                "```\n"
                "OpenJML Verification tool failed to verify the specifications given above, with error information as follows:\n\n"
                "### ERROR MESSAGE:\n"
                "```\n"
                "{curr_error}\n"
                "```\n\n"
                "### ERROR TYPES:\n"
                "{error_info}\n"
                "Please refine the specifications so that they can pass verification. Provide the specifications for the code and include the solution written between triple backticks, after `### FIXED SPECIFICATION`.\n"

                )
            ])

       
    def __init__(self, model_name: str, language: str = "java"):
        self.llm = create_llm(model_name)
        self.language = language
        self.prompt_template = self._create_prompt(model_name)
        
    def __call__(self, state: State, config: RunnableConfig = None):
        n_errors, output, last_spec = state["analysis_results"][-1]
        assert n_errors > 0, "No errors to fix"
    
        res, new_messages = Assistant.__call__(self, state, config=config)
        spec = get_specs_from_response(res.content, state["lang"])
        return spec, new_messages
    
