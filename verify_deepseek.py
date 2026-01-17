import os
from dotenv import load_dotenv
from config import Config
from ai_services.text_processor import TextProcessor

print("Current Working Directory:", os.getcwd())

def test_deepseek():
    load_dotenv()
    
    # Force config to match checking expectations if needed, 
    # but strictly we rely on .env and config.py defaults
    print(f"Provider: {Config.AI_PROVIDER}")
    print(f"Base URL: {Config.AI_BASE_URL}")
    print(f"Model: {Config.AI_MODEL_NAME}")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment. Test will likely fail or fallback.")
    
    tp = TextProcessor()
    text = "Artificial Intelligence is a branch of computer science that aims to create intelligent machines."
    
    print("\n--- Testing Simplify ---")
    try:
        result = tp.simplify_text(text, level="simple")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_deepseek()
