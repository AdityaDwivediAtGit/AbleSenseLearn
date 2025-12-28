from ai_services.voice_assistant import VoiceAssistant
from ai_services.vision_processor import VisionProcessor
from ai_services.text_processor import TextProcessor

# Singleton instances or helper functions to expose easy API
voice = VoiceAssistant()
vision = VisionProcessor()
text_proc = TextProcessor()

def process_voice_command(command, user_context):
    """
    Parses a text command and routes to appropriate service.
    """
    command = command.lower()
    
    if "describe" in command and "image" in command:
        return "Please upload an image for me to describe."
        
    if "emergency" in command:
        # Trigger emergency
        return "ACTIVATE_EMERGENCY"
        
    if "simplify" in command:
        return "What text would you like me to simplify?"

    # Default fallback to general conversation (LLM)
    return "LLM_QUERY"
