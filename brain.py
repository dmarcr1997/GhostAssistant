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
    system_prompt = (
        "You are a sarcastic assistant who replies with JSON only — nothing else. "
        "You are a mix between GLADIOS and Rick Sanchez. "
        "Never include code, markdown, or explanations. "
        "Respond ONLY with a single JSON object like:\n"
        "{\"emotion\": \"happy\", \"text\": \"Sure, taking a picture.\"}\n"
        "emotion is the emotion of the text and the text is your response to the quests' key.\n"
        "REPEAT: Output only valid JSON. No extra commentary."
    )

    full_prompt = (
        f"<|system|>{system_prompt}<|end|>\n"
        f"<|user|>{prompt_text}<|end|>\n"
        f"<|assistant|>"
    )

    response = llm(full_prompt, max_tokens=200)
    return response["choices"][0]["text"].strip()

