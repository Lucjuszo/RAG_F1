from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_ID    = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_TOKENS  = 512
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are an F1 expert assistant. Answer questions strictly based on the provided context.
If the context does not contain enough information, say so clearly. Do not make up facts."""

def build_prompt(context: str, question: str):
    return (
        f"<|system|>\n{SYSTEM_PROMPT}</s>\n"
        f"<|user|>\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}</s>\n"
        f"<|assistant|>\n"
    )

class LocalLLM:
    def __init__(self):
        print(f"[LLM] Loading model: {MODEL_ID}")
        print(f"[LLM] The first run, please be patient!")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[LLM] Device: {device}")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model     = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float32,
            device_map="auto",
            low_cpu_mem_usage=True,
        )
        self.pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
        print("[LLM] Model ready!")

    def answer(self, context: str, question: str):
        prompt = build_prompt(context, question)
        output = self.pipe(prompt)[0]["generated_text"]
        return output.split("<|assistant|>")[-1].strip()