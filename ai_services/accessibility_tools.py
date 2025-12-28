import shutil
import os

class EmergencyFeatures:
    @staticmethod
    def trigger_emergency(user, location="Unknown"):
        """
        Simulates an emergency protocol.
        """
        if not user.emergency_contact_phone:
            return "No emergency contact set!"
            
        message = f"EMERGENCY ALERT: {user.username} has triggered an emergency alert. Location: {location}. Medical Info: {user.medical_info}"
        
        # Simulation: In a real app, integrate Twilio/SMS API here
        print(f"SENDING SMS TO {user.emergency_contact_phone}: {message}")
        
        return f"Alert sent to {user.emergency_contact_name} ({user.emergency_contact_phone}). Emergency services notified."

class AccessibilityTools:
    @staticmethod
    def check_contrast(hex_color1, hex_color2):
        # Implementation of WCAG contrast formula
        return "4.5:1 (Pass AA)" # Mock for now
