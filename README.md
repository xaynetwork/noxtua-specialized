# NoxtuaCompliance

# Get Started

This repository contains the logical code to run NoxtuaCompliance with vllm. A Gradio application is used for quick testing with a chat.

## Prerequisites

1. Install Docker and Python (tested with version 3.11.2)
2. Run vllm

    ```sh
    docker run --runtime nvidia --gpus all -v ~/.cache/huggingface:/root/.cache/huggingface -p 8000:8000 --ipc=host vllm/vllm-openai:v0.6.6.post1 --model xaynetwork/NoxtuaCompliance --tensor-parallel-size=2 --disable-log-requests --max-model-len 120000 --gpu-memory-utilization 0.95
    ```

## Setup

```sh
pip install -r requirements.txt
```

## Gradio Application

```sh
python app.py
```

This command starts the Gradio application with a chat in the localhost under the specified port `8020`. Open the displayed link in the browser, e.g. "http://0.0.0.0:8020" or "http://localhost:8020".