# FormalBench: A Comprehensive Evaluation of LLMs on Formal Specification Inference

[![Build and test](https://github.com/thanhlecongg/FormalBench/actions/workflows/build_and_test.yml/badge.svg)](https://github.com/thanhlecongg/FormalBench/actions/workflows/build_and_test.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Release](https://img.shields.io/badge/Release-0.1.0-orange.svg)](https://github.com/thanhlecongg/FormalBench/tree/e15a061b237e0fd49cc10628fca79f47a653ddf1)
[![Dataset](https://img.shields.io/badge/Dataset-v1.0-yellow.svg)](https://huggingface.co/datasets/FormalBench/FormalBench/tree/main)


This repository contains evaluation infrastructure for FormalBench including evaluation metrics and wrappers for calling LLMs. If you found this repository to be useful, please cite our research paper:

```
@article{le2025can,
  title={Can LLMs Reason About Program Semantics? A Comprehensive Evaluation of LLMs on Formal Specification Inference},
  author={Le-Cong, Thanh and Le, Bach and Murray, Toby},
  journal={arXiv preprint arXiv:2503.04779},
  year={2025}
}
```

## Prerequisites

FormalBench have two modes:
- Docker mode, which requires the docker in your local computers
- Non-Docker mode, which requires Ubuntu 20.04

Versions:
- Python 3.12
- Pip 25.0
- Java 11
- Clang-12

## Installation

- Step 1: Clone FormalBench to local computers:
```
git clone https://github.com/thanhlecongg/FormalBench.git
```

- Step 2: Create virtual environment with Python (default version of FormalBench is Python 3.12)
```
python3 -m venv .env
. .env/bin/activate
```

- Step 3: Install FormalBench
```
pip3 install -e .[default]
```

- Step 4: Setup API keys:
To use LLMs and langsmith (optional), please setup the enviroment file at `FormalBench/config/.env`. See the following for an example:
```
OPENAI_API_KEY=<OpenAI API Key>
DEEPSEEK_API_KEY = <DeepSeek API Key>
ANTHROPIC_API_KEY = <Anthropic API Key>
HF_TOKEN=<HunggingFace Access Token>
### Optional
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=<LangSmith API key>
LANGSMITH_PROJECT=<LangSmith Projet Name>
```

## Supported Features

- Language: Currently, we support: 
    - Java with its specification language, JML
    - C with its specification language, ACSL
- Verification tools: Currently, we provide wrapper to two tools:
    - [OpenJML](https://www.openjml.org/) tool version 17 & 21 to verify Java programs annotated by JML
    - [Frama-C](https://frama-c.com/) tool version 26 (Iron) to verify C programs annotated by ACSL
- Evaluation metrics:
    - Consistency metrics: Verification success rate & failure rate
    - Completeness metrics: We implemented our completeness metric based mutation analysis:
        - For Java, we use [Major framework](https://mutation-testing.org/) 
        - For C, we use [Mull framework](https://mull.readthedocs.io/en/latest/HowMullWorks.html)
- LLM-based specification inference:
    - workflow:
        - basic: Generate spec and verify it using verfication tool
        - only_gen: Only generate spec
    - prompt_type: zero shot, few shot, least-to-most, chain-of-thought
    - LLMs: DeepSeekV3, GPT-4o, GPT3.5, o3-mini, o1-mini, Claude3.5-Sonnet, CodeQwen2.5 (QwenCoder-32B), CodeQwen1.5-7B, CodeLLama-34B, DeepSeekV2-32B

## Basic Usage

Please refers to `demo` folder and `demo/USAGE.MD` for detailed instructions and examples
