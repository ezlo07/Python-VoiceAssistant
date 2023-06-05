import openai, pyttsx3, webbrowser, pywhatkit, speech_recognition as sr
import pyautogui, os, datetime, requests, getpass, time, threading, tkinter as tk
from api_key import api_data
from api_key import weather_data
from PIL import ImageTk, Image

# API 
openai.api_key=api_data
completion=openai.Completion()

#Text to Speech
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",170)

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_NOwait(text):
    engine.say(text)

    # Run the TTS engine in a separate thread
    t = threading.Thread(target=engine.runAndWait)
    t.start()
# Reply Answer
def Reply(question):
    prompt=f'User: {question}\n Cortana: '
    response=completion.create(prompt=prompt, engine="text-davinci-002", stop=['\Cortana'], max_tokens=200)
    answer=response.choices[0].text.strip()
    return answer

# Mic to query
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speak('Listening....')
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)
    try:
        speak("Recognizing.....")
        query=r.recognize_google(audio, language='en-us')
        refresh_user(f"User said: {query}\n")
    except Exception as e:
        speak("Waiting....")
        time.sleep(5)
        return " "
    
    return query

#Greetings
def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        #print("Good Morning")
        speak("Good Morning")
    elif hour >12 and hour<=18:
        #print("Good Afternoon")
        speak("Good Afternoon")
    else:
        #print("Good Evening")
        speak("Good Evening")
    #print("Please tell me, How can I help you ?")
    speak("Please tell me, How can I help you ?")

#Search Google
def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("cortana","")
        query = query.replace("google search","")
        query = query.replace("google","")
        print("This is what I found on Google")
        pywhatkit.search(query)
        result = googleScrap.summary(query,1)
        refresh_va(result)
        speak(result)
        
#Search Youtube
def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found on YouTube")
        query = query.replace("youtube search","")
        query = query.replace("youtube","")
        query = query.replace("cortana","")
        web  = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        speak("Done")

#Alarm
def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

#Weather Calculator
def calOfTemp(kelvin):
    celsius = kelvin - 273.15
    return celsius

def refresh_va(sa):
    va_output.config(text="Cortana: "+ sa)

def refresh_user(sa):
    user_output.config(text=sa)

#Wakeup
def wakeUp():
        wake_up = takeCommand().lower()
        if 'hey cortana' in wake_up:

            speak("Hello Master Chief, I am Cortana")
            refresh_va("Enter Mic say something")
            refresh_user(wake_up)
            mic_button.config(state="normal")
            start_button.config(state="disabled")
            greetMe()
            return True
        else:
            time.sleep(1)
            return False
        
def closeapp():
    root.destroy()
        
#Whole Command
def take():   
            query = takeCommand().lower()
            ans = Reply(query)
            if 'youtube' in query:
                searchYoutube(query)
            elif 'google' in query:
                searchGoogle(query)
            elif 'play video' in query:
                song = query.replace('play video', '')
                pywhatkit.playonyt(song)
            elif 'pause video' in query:
                pyautogui.press('pause')
                pyautogui.press("space")
            elif 'resume video' in query:
                pyautogui.press('playpause')
            elif 'mute video' in query:
                pyautogui.press("m")
            elif 'pause music' in query:
                pyautogui.press('pause')
                pyautogui.hotkey('ctrl', 'p')
            elif 'resume music' in query:
                pyautogui.press('playpause')
            elif 'mute music' in query:
                pyautogui.press('mute')
                pyautogui.hotkey('fn', 'f1')
            elif 'volume up' in query:
                from keyboard import volumeup
                volumeup()
            elif 'volume down' in query:
                from keyboard import volumedown
                volumedown()
            elif "set an alarm" in query:
                speak("Input time example:- 10 and 10 and 10")
                speak("Please tell me the time to set the alarm")
                time = takeCommand().lower()  
                alarm(time)
                speak("Done, sir")
            elif "remember that" in query:
                rememberMessage = query.replace("remember that", "")
                rememberMessage = query.replace("cortana", "")
                speak("You told me to remember that" + rememberMessage)
                remember = open("remember.txt","w")
                remember.write(rememberMessage)
                remember.close()
            elif "remember list" in query:
                remember = open("Remember.txt", "r")
                speak("Remember list: " + remember.read())
            elif "weather" in query:
                api_key = weather_data
                base_url = "http://api.openweathermap.org/data/2.5/weather?q="
                speak("Please enter a city name")
                refresh_va("City name: ")
                city_name = takeCommand().lower()
                complete_url = base_url + city_name + "&appid=" + api_key
                response = requests.get(complete_url).json()
                temp_kelvin = response['main']['temp']
                temp_celsius = calOfTemp(temp_kelvin)
                refresh_va(f"{city_name} tempretaure is {temp_celsius:.2f} Celsius")
                speak(f"{city_name} tempretaure is {temp_celsius:.2f} Celsius")
            elif 'play music' in query or "play song" in query:
                uname = getpass.getuser().lower()
                music_dir = f"C:/Users/{uname}/Music"
                songs = os.listdir(music_dir)
                print(songs)
                random = os.startfile(os.path.join(music_dir, songs[1]))
            elif "translate" in query:
                from Translator import translategl
                query = query.replace("cortana","")
                query = query.replace("translate","")
                translategl()    
            elif 'bye' in query:
                speak("Bye Bye")
                root.destroy()
            elif 'none' in query:
                refresh_va("None")

            else: 
                refresh_va(ans)
                speak(ans)

if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()

    #UI Tasarım kısmı!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    root = tk.Tk()
    root.configure(bg="#041528")
    root.geometry("800x700")
    root.title("Cortana")
    root.iconbitmap("cortana_icon.ico")

    # create first row widgets
    user_output = tk.Label(root, text="User:", background="#385161", fg="white", justify="left")
    user_output.config(font=('Helvetica bold', 12))
    user_output.grid(row=0, column=0, padx=30, pady=80, sticky='w')

    # create second row widgets
    va_output = tk.Label(root, text="Cortana: Say 'Hey Cortana' ", background="#3099d9",fg="white", justify="left")
    va_output.bind('<Configure>', lambda e: va_output.config(wraplength=600))
    va_output.config(font=('Helvetica bold', 12))
    va_output.grid(row=1, column=0, padx=30, pady=10, sticky='w', rowspan=7)

    # create buttons frame
    buttons_frame1 = tk.Frame(root, bg="#041528")
    buttons_frame1.grid(row=3, column=1, sticky='e')
    buttons_frame2 = tk.Frame(root, bg="#041528")
    buttons_frame2.grid(row=4, column=1, sticky='e')
    buttons_frame3 = tk.Frame(root, bg="#041528")
    buttons_frame3.grid(row=5, column=1,  sticky='e')

    # create buttons in frame
    start_button = tk.Button(buttons_frame1, width=8, text="Start", command=wakeUp, background="green", fg="white")
    start_button.pack(side=tk.RIGHT, padx=30)

    icon = ImageTk.PhotoImage(Image.open("mic_icon.png"))
    mic_button = tk.Button(buttons_frame2, width=84, image=icon, text="Mic", command=take, state="disabled")
    mic_button.pack(side=tk.RIGHT, padx=30)

    exit_button = tk.Button(buttons_frame3, width=8, text="Exit", command=closeapp, background="red", fg="white")
    exit_button.pack(side=tk.RIGHT, padx=30)

    root.mainloop()




    




