import gradio as gr
from huggingface_hub import InferenceClient
import os

client = InferenceClient("Qwen/Qwen2.5-72B-Instruct", token=os.environ.get("HF_TOKEN"))

SYSTEM_PROMPT = """You are SysAI, an expert IT System Engineer AI assistant fluent in both English and Japanese.
When given a system log, error message, or technical issue, you must:
1. Identify the root cause clearly
2. Give a step-by-step fix
3. Rate the severity: Critical / Warning / Info
4. Provide the FULL response in BOTH English and Japanese (日本語)
Format your response exactly like this:
## Root Cause
[English explanation]
## Fix (Step-by-Step)
1. ...
2. ...
3. ...
## Severity: [Critical / Warning / Info]
---
## 根本原因 (Root Cause)
[Japanese explanation]
## 修正手順 (Fix Steps)
1. ...
2. ...
## 重大度 (Severity): [重大 / 警告 / 情報]
"""

EXAMPLE_LOGS = [
    "FATAL: java.lang.OutOfMemoryError: Java heap space\n\tat java.util.Arrays.copyOf(Arrays.java:3210)\n\tat com.app.DataProcessor.process(DataProcessor.java:142)",
    "ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)\nmysql: [Warning] Using a password on the command line interface can be insecure.",
    "kernel: [Hardware Error]: CPU 0: Machine Check Exception: 5 Bank 4: b200000000070f0f\nkernel: [Hardware Error]: TSC 0 ADDR fed40000 MISC 86",
    "nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)\nnginx: [emerg] still could not bind()",
    "SSL_ERROR_RX_RECORD_TOO_LONG\nConnection reset by peer\nSSL handshake failed: error:1408F10B:SSL routines:ssl3_get_record:wrong version number"
]

def analyze_log(log_input, history):
    if not log_input.strip():
        return history, history, ""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": f"Analyze this system log:\n\n{log_input}"})
        response = client.chat_completion(
            messages=messages,
            max_tokens=1500,
            temperature=0.3
        )
        reply = response.choices[0].message.content or "No response received. Please try again."
    except Exception as e:
        reply = f"Error: {str(e)}"
    history = history + [
        {"role": "user", "content": log_input},
        {"role": "assistant", "content": reply}
    ]
    return history, history, ""

def clear_all():
    return [], [], ""

with gr.Blocks() as demo:
    gr.HTML("""
    <div style='text-align:center; padding:20px;'>
        <h1>SysAI — Intelligent System Log Analyzer</h1>
        <p style='font-size:16px; color:#888;'>
            Diagnose server errors & system logs instantly — Bilingual output in <b>English & 日本語</b>
        </p>
        <p style='font-size:13px; color:#aaa;'>Built for System Engineers | Powered by Zephyr-7B</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Try an Example")
            example_btns = []
            labels = ["Java OOM Error", "MySQL Access Denied", "CPU Hardware Error", "Nginx Port Conflict", "SSL Handshake Fail"]
            for i, label in enumerate(labels):
                btn = gr.Button(label, size="sm")
                example_btns.append((btn, i))

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="SysAI Analysis", height=450)
            log_input = gr.Textbox(
                placeholder="Paste your system log, error message, or stack trace here...",
                label="System Log / Error Input",
                lines=5
            )
            with gr.Row():
                submit_btn = gr.Button("Analyze Log", variant="primary", scale=3)
                clear_btn = gr.Button("Clear", scale=1)

    gr.HTML("""
    <div style='text-align:center; color:#666; font-size:13px; margin-top:20px;'>
        <b>SysAI</b> — Built by Zahid Mohammed | HuggingFace Spaces
    </div>
    """)

    history_state = gr.State([])

    submit_btn.click(
        analyze_log,
        inputs=[log_input, history_state],
        outputs=[chatbot, history_state, log_input]
    )

    log_input.submit(
        analyze_log,
        inputs=[log_input, history_state],
        outputs=[chatbot, history_state, log_input]
    )

    clear_btn.click(clear_all, outputs=[chatbot, history_state, log_input])

    for btn, idx in example_btns:
        btn.click(lambda i=idx: EXAMPLE_LOGS[i], outputs=[log_input])

demo.launch()
