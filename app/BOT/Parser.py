#Understand User Input.

def detect_intent(message):
    lower_message=message.lower()
    if any(word in lower_message for word in ["look","search" ]): #And so on more synonyms for investigate
        return "investigate"
    if any(word in lower_message for word in ["chat","speak" ]): #And so on more synonyms for talk
        return "talk"
    if any(word in lower_message for word in ["leave","run" ]): #And so on more synonyms for investigate
        return "investigate"



    return "challenge"

