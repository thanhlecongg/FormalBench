import os
from dotenv import load_dotenv
import FormalBench

_LIB_DIR = os.path.dirname(FormalBench.__file__)

load_dotenv(dotenv_path=os.path.join(_LIB_DIR, "config/.env"))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "false"
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
print(os.environ["LANGCHAIN_TRACING_V2"])