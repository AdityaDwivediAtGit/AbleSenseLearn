import openai
from config import Config
from transformers import pipeline
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
            self._summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        return self._summarizer

    @debug_trace
    def _get_generator(self):
        if not self._generator:
            # Flan-T5 is great for instruction following like "Simplify this"
            self._generator = pipeline("text2text-generation", model="google/flan-t5-small")
        return self._generator

    @debug_trace
    def simplify_text(self, text, level="simple"):
        """
        Simplifies text for easier reading.
        """
        if not text:
            return ""
            
        # Test Mode Check
        if Config.ENABLE_TEST_DATA:
            return f"[TEST DATA] This is a simplified version of your text. ({level})"

        # Logic: If HuggingFace is selected, use HF (Local). 
        # If OpenAI/DeepSeek selected AND key exists, use OpenAI client with custom base_url.
        
        if Config.AI_PROVIDER == "HuggingFace":
            return self._simplify_with_hf(text, level)
            
        # For OpenAI or DeepSeek
        if Config.OPENAI_API_KEY:
            # Re-configure OpenAI client dynamically
            openai.api_key = Config.OPENAI_API_KEY
            openai.base_url = Config.AI_BASE_URL
            return self._simplify_with_openai(text, level)
        else:
            # Fallback if no key provided but provider selected? 
            # We'll default to HF local if they forgot key, or return error string?
            # Let's fallback to HF local for robustness
            return self._simplify_with_hf(text, level)

    @debug_trace
    def summarize_text(self, text):
        """Summarizes long text."""
        if Config.ENABLE_TEST_DATA:
            return "[TEST DATA] - Point 1\n- Point 2\n- Point 3"

        if Config.AI_PROVIDER == "HuggingFace":
            return self._summarize_with_hf(text)

        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
            openai.base_url = Config.AI_BASE_URL
            return self._summarize_with_openai(text)
        else:
           return self._summarize_with_hf(text)

    # --- OpenAI/DeepSeek Implementations ---
    def _simplify_with_openai(self, text, level):
        system_prompt = "You are a helpful assistant that simplifies complex text."
        if level == "very_simple":
            prompt = f"Rewrite in very simple words: \n\n{text}"
        elif level == "explain_like_im_5":
            prompt = f"Explain like I am 5 years old: \n\n{text}"
        else:
            prompt = f"Simplify this text: \n\n{text}"

        try:
            # Note: We use Config.AI_MODEL_NAME
            response = openai.chat.completions.create(
                model=Config.AI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"{Config.AI_PROVIDER} Error: {str(e)}. Falling back to local model..."

    def _summarize_with_openai(self, text):
        try:
            response = openai.chat.completions.create(
                model=Config.AI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Summarize key points."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"{Config.AI_PROVIDER} Error: {str(e)}"

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
