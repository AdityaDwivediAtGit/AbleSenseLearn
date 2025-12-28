import openai
from config import Config

class TextProcessor:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def simplify_text(self, text, level="simple"):
        """
        Simplifies text for easier reading.
        level: 'simple', 'very_simple', 'explain_like_im_5'
        """
        if not text:
            return ""
            
        system_prompt = "You are a helpful assistant that simplifies complex text for people with cognitive disabilities or low reading literacy."
        
        if level == "very_simple":
            prompt = f"Rewrite the following text in very simple words, short sentences, and separate complex ideas: \n\n{text}"
        elif level == "explain_like_im_5":
            prompt = f"Explain the following text like I am 5 years old: \n\n{text}"
        else:
            prompt = f"Simplify the following text to make it easier to read: \n\n{text}"

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error simplifying text: {str(e)}"

    def summarize_text(self, text):
        """Summarizes long text into key points."""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize the key points of this text in a clear, bulleted list."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error summarizing text: {str(e)}"
