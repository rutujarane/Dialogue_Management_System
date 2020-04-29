import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be a `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be a `Microphone` instance")

    #Listen from microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":

    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #Begin Dialogue
    instructions = (
        "Hi! How may I help you today?\n"
    ).format()

    print(instructions)
    time.sleep(3)

    #Take input and Recognize
    for j in range(PROMPT_LIMIT):
        print('Start Speaking!')
        audio = recognize_speech_from_mic(recognizer, microphone)
        if audio["transcription"]:
            break
        if not audio["success"]:
            break
        print("I didn't catch that. What did you say?\n")

    if audio["error"]:
        print("ERROR: {}".format(audio["error"]))

    print("You said: {}".format(audio["transcription"]))

    print("Is that correct? Y or N:")
    correct = input()

    if correct=='Y':
        print("Successful transcription!")
    else:
        print("Please try again!")