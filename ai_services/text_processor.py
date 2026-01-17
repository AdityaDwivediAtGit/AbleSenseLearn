import openai
import httpx
from langchain_openai import ChatOpenAI
from config import Config
from utils.debug import debug_trace

class TextProcessor:
    def __init__(self):
        self.use_openai = False
        if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY.startswith("sk-"):
            openai.api_key = Config.OPENAI_API_KEY
            self.use_openai = True
        
        # Lazy loading wrappers for HF pipelines to avoid startup lag
        self._summarizer = None
        self._generator = None

    @debug_trace
    def _get_summarizer(self):
        if not self._summarizer:
            # Using a small, efficient model for local execution
            from transformers import pipeline
            self._summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        return self._summarizer

    @debug_trace
    def _get_generator(self):
        if not self._generator:
            # Flan-T5 is great for instruction following like "Simplify this"
            from transformers import pipeline
            self._generator = pipeline("text2text-generation", model="google/flan-t5-small")
        return self._generator

    @debug_trace
    def simplify_text(self, text, level="simple"):
        """
        Simplifies text for easier reading.
        """
        if not text:
            return ""
            
        # Logic: If HuggingFace is selected, use HF (Local).

        # Logic: If HuggingFace is selected, use HF (Local). 
        if Config.AI_PROVIDER == "HuggingFace":
            return self._simplify_with_hf(text, level)
            
        # For OpenAI or DeepSeek (via LiteLLM Proxy)
        if Config.OPENAI_API_KEY:
            return self._process_with_llm(text, task_type="simplify", level=level)
        else:
            return self._simplify_with_hf(text, level)

    @debug_trace
    def summarize_text(self, text):
        """Summarizes long text."""
    @debug_trace
    def summarize_text(self, text):
        """Summarizes long text."""
        if Config.AI_PROVIDER == "HuggingFace":
            return self._summarize_with_hf(text)

        if Config.OPENAI_API_KEY:
            return self._process_with_llm(text, task_type="summarize")
        else:
           return self._summarize_with_hf(text)

    # --- Unified LLM Implementation ---
    def _process_with_llm(self, text, task_type, level="simple"):
        try:
            # Configure HTTP Client (verify=False for internal proxy if needed)
            http_client = httpx.Client(verify=Config.AI_SSL_VERIFY)
            
            # Initialize LangChain ChatOpenAI
            llm = ChatOpenAI(
                base_url=Config.AI_BASE_URL,
                model=Config.AI_MODEL_NAME,
                api_key=Config.OPENAI_API_KEY,
                http_client=http_client,
                max_tokens=300
            )

            # Construct Prompts
            if task_type == "simplify":
                system_prompt = "You are a helpful assistant that simplifies complex text."
                if level == "very_simple":
                    prompt = f"Rewrite in very simple words: \n\n{text}"
                elif level == "explain_like_im_5":
                    prompt = f"Explain like I am 5 years old: \n\n{text}"
                else:
                    prompt = f"Simplify this text: \n\n{text}"
                
                messages = [
                    ("system", system_prompt),
                    ("human", prompt)
                ]
                
            elif task_type == "summarize":
                messages = [
                    ("system", "Summarize the following text efficiently."),
                    ("human", text)
                ]
            
            # Invoke Model
            response = llm.invoke(messages)
            return response.content

        except Exception as e:
            print(f"[ERROR] {Config.AI_PROVIDER} Failed: {str(e)}. Falling back to local model...")
            # Actual fallback logic
            if task_type == "simplify":
                return self._simplify_with_hf(text, level)
            else:
                return self._summarize_with_hf(text)

    # --- Hugging Face Implementations ---
    def _simplify_with_hf(self, text, level):
        try:
            generator = self._get_generator()
            
            if level == "explain_like_im_5":
                prompt = f"Explain like I am 5: {text}"
            else:
                prompt = f"Simplify: {text}"
                
            # FLAN-T5 works well with instruction prompts
            result = generator(prompt, max_length=200, do_sample=False)
            return result[0]['generated_text']
        except Exception as e:
            return f"Local Model Error: {str(e)}"

    def _summarize_with_hf(self, text):
        try:
            summarizer = self._get_summarizer()
            # Truncate input if too long for the model (simplified)
            result = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            return f"Local Model Error: {str(e)}"
