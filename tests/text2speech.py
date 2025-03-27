import pyttsx3


text = ("Hello World!")

def text2speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.setProperty('rate', 90) 
    engine.say(text)
    engine.runAndWait()



text2speech(text)