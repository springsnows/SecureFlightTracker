import pyttsx3


text = ("Hello World!") # example text to be spoken

def text2speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 110) # audio speed
    engine.say(text)
    engine.runAndWait()

text2speech(text)