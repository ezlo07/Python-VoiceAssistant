import pyttsx3, speech_recognition, os, time
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from playsound import playsound

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_language_code(language_name):
    for code, name in LANGUAGES.items():
        if name.lower() == language_name.lower():
            return code
    return None

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-US')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def translategl():
    speak("Say word to translate")
    query = takeCommand().lower()
    translator = Translator()
    speak("Choose the language in which you want to translate")
    lang_name = takeCommand().lower()
    b = get_language_code(lang_name)  
    print(b)
    speak("SURE SIR")
    text_to_translate = translator.translate(query,src = "auto",dest= b,)
    text = text_to_translate.text
    try : 
        speakgl = gTTS(text=text, lang=b, slow= False)
        speakgl.save("voice.mp3")
        playsound("voice.mp3")
        
        time.sleep(5)
        os.remove("voice.mp3")
    except:
        print("Unable to translate")





