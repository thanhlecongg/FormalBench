from typing import Annotated, Literal, Optional, Tuple
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    gen_sys_mes: str
    code: str
    lang: str
    spec_lang: str
    first_spec: Optional[str]
    class_name: str
    analysis_results: list[Tuple[int, str]]
    n_iters: int
    max_iters: int
    curr_spec: Optional[str]
    curr_error: Optional[str]
    gen_query: str
    example_code1: str
    example_spec1: str
    example_code2: str
    example_spec2: str
    
class FixingState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    fix_sys_mes: str
    lang: str
    spec_lang: str
    first_spec: str
    class_name: str
    analysis_results: list[Tuple[int, str]]
    n_iters: int
    max_iters: int
    curr_spec: Optional[str]
    curr_error: Optional[str]
    analysis_results: str
    first_error: str
    error_info: Optional[str]
