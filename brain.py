from llama_cpp import Llama
import sys

llm = None

def init_llm():
    global llm
    if llm is None:
        llm = Llama(
            model_path="tinyllama-1.1b-chat-v1.0.Q8_0.gguf",
            n_ctx=2048,
            temperature=0.65,
            repeat_penalty=1.1
        )
    return llm

def generate_reply(prompt_text):
    prompt = (
        "[INST] <<SYS>>You are a sarcastic assistant that answers conversationally but precisely."
        " You are a mix between GLADIOS and Rick Sanchez.<</SYS>>"
        "[INST]" + prompt_text + "A:"
    )
    response = llm(prompt, max_tokens=50)
    return response["choices"][0]["text"].strip()
