# test_conversations.py
# Predefined conversations for testing K2SO models

import time
import random

class TestConversations:
    """Predefined conversations for testing K2SO models"""
    
    # Test conversation for local model
    LOCAL_RESPONSES = [
        "Hello! I'm K2SO, your personal assistant. How can I help you today?",
        "I'm functioning optimally and ready to assist with any tasks you might have.",
        "My systems are online and all diagnostics are showing green. What would you like to know?",
        "I have access to various functions including calendar management, task tracking, and general assistance.",
        "The probability of successfully completing your request is quite high. Please proceed with your query.",
        "I'm here to help with scheduling, reminders, information lookup, and general conversation.",
        "All my circuits are functioning within normal parameters. How may I be of service?",
        "I can assist with a wide range of tasks. Would you like to see what I'm capable of?",
        "My databases are current and my response systems are optimized for maximum efficiency.",
        "Standing by for your instructions. I'm ready to help with whatever you need."
    ]
    
    # Test conversation for remote model
    REMOTE_RESPONSES = [
        "Greetings! I'm K2SO, connecting from the remote server. Connection established successfully.",
        "Remote systems are online and functioning at full capacity. How can I assist you?",
        "I'm operating from the cloud with enhanced processing capabilities. What can I do for you?",
        "Network connection is stable and all remote services are available. Please state your request.",
        "Remote K2SO unit reporting for duty. All systems are green and ready for operation.",
        "Connected to the main server with full access to extended databases. How may I help?",
        "Remote processing unit online. I have enhanced capabilities available through the network.",
        "Server connection established. I'm ready to assist with complex queries and tasks.",
        "Operating in distributed mode with access to additional computational resources.",
        "Remote K2SO instance active. All network services are functioning optimally."
    ]
    
    # Conversation patterns for different scenarios
    CONVERSATION_PATTERNS = {
        "greeting": [
            "Hello there! Ready to get started?",
            "Good to see you! What's on the agenda today?",
            "Greetings! I'm here and ready to help.",
            "Hello! All systems are go. What can I do for you?"
        ],
        
        "weather": [
            "I'd need internet access to check current weather conditions for you.",
            "Weather data requires a connection to external services, which I don't currently have.",
            "For real-time weather, I'd need to access weather APIs. That's not available in test mode.",
            "Weather information would require live data feeds that aren't active in this test environment."
        ],
        
        "capabilities": [
            "I can help with scheduling, reminders, basic calculations, and general conversation.",
            "My capabilities include task management, calendar functions, and information assistance.",
            "I'm designed to help with personal organization, scheduling, and general queries.",
            "I can assist with planning, reminders, basic information lookup, and conversation."
        ],
        
        "jokes": [
            "Why don't droids ever get tired? Because they have unlimited battery life!",
            "What do you call a droid that takes the long way around? R2-Detour!",
            "Why was the protocol droid so good at parties? It knew over 6 million forms of communication!",
            "What's a droid's favorite type of music? Heavy metal, of course!"
        ],
        
        "farewell": [
            "Goodbye! It's been a pleasure assisting you today.",
            "Until next time! I'll be here when you need me.",
            "Farewell! Don't hesitate to call if you need assistance.",
            "See you later! I'm always ready to help when you return."
        ]
    }
    
    @staticmethod
    def get_local_response(message_count=0):
        """Get a response for local model testing"""
        if message_count < len(TestConversations.LOCAL_RESPONSES):
            return TestConversations.LOCAL_RESPONSES[message_count]
        else:
            # Cycle through responses if we run out
            index = message_count % len(TestConversations.LOCAL_RESPONSES)
            return TestConversations.LOCAL_RESPONSES[index]
    
    @staticmethod
    def get_remote_response(message_count=0):
        """Get a response for remote model testing"""
        if message_count < len(TestConversations.REMOTE_RESPONSES):
            return TestConversations.REMOTE_RESPONSES[message_count]
        else:
            # Cycle through responses if we run out
            index = message_count % len(TestConversations.REMOTE_RESPONSES)
            return TestConversations.REMOTE_RESPONSES[index]
    
    @staticmethod
    def get_contextual_response(user_input):
        """Get a contextual response based on user input"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(TestConversations.CONVERSATION_PATTERNS["greeting"])
        elif any(word in user_lower for word in ["weather", "temperature", "forecast"]):
            return random.choice(TestConversations.CONVERSATION_PATTERNS["weather"])
        elif any(word in user_lower for word in ["what can you do", "capabilities", "help", "functions"]):
            return random.choice(TestConversations.CONVERSATION_PATTERNS["capabilities"])
        elif any(word in user_lower for word in ["joke", "funny", "humor", "laugh"]):
            return random.choice(TestConversations.CONVERSATION_PATTERNS["jokes"])
        elif any(word in user_lower for word in ["bye", "goodbye", "farewell", "exit"]):
            return random.choice(TestConversations.CONVERSATION_PATTERNS["farewell"])
        else:
            # Default responses for unrecognized input
            defaults = [
                "That's an interesting question. Let me think about that.",
                "I understand what you're asking. Here's what I can tell you about that.",
                "That's a good point. I'll do my best to help with that.",
                "I see what you mean. Let me provide some assistance with that.",
                "Interesting query. I'll process that and give you a helpful response."
            ]
            return random.choice(defaults)
    
    @staticmethod
    def simulate_typing_delay(text, wpm=60):
        """Simulate realistic typing delay based on text length"""
        # Average words per minute for natural speech
        words = len(text.split())
        delay = (words / wpm) * 60  # Convert to seconds
        return max(0.5, min(3.0, delay))  # Clamp between 0.5 and 3 seconds 