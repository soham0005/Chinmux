import random

error_responses = [
    "Oops! Something went wrong. Please try again later.",
    "I'm sorry, but I couldn't process your request due to an error.",
    "It seems there was an issue with your input. Please check and try again.",
    "An unexpected error has occurred. Please retry your request.",
    "I encountered a problem while processing your request. Please verify the information.",
    "Unfortunately, I couldn't complete the operation due to an error.",
    "There seems to be a glitch. Let's try that again.",
    "I’m having trouble understanding that. Could you clarify your request?",
    "Error detected! Please ensure your input meets the required format.",
    "Sorry, but it looks like something didn’t go as planned. Please check your request."
]

def get_random_error_response():
    return random.choice(error_responses)
