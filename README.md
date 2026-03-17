# ⚙️ SysAI — AI-Powered System Log Analyzer

> Paste any server error or system log → get instant root cause analysis in English & Japanese

🔗 **[Live Demo → https://huggingface.co/spaces/zahidmohd/sysai-log-analyzer](https://huggingface.co/spaces/zahidmohd/sysai-log-analyzer)**

## What it does
- Analyzes server logs, stack traces, OS errors, DB errors instantly
- Identifies root cause and provides step-by-step fixes
- Bilingual output — English + 日本語 (Japanese)
- Severity classification: Critical / Warning / Info
- 5 built-in real-world error examples

## Tech Stack
- Model: Qwen2.5-72B-Instruct (via HuggingFace Inference API)
- UI: Gradio 6
- Deployment: HuggingFace Spaces

## Run Locally
pip install gradio huggingface_hub
python app.py

## Built By
Zahid Mohammed  
