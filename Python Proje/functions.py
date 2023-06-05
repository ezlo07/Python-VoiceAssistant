import openai, pyttsx3, webbrowser, pywhatkit, speech_recognition as sr
import pyautogui, os, datetime, requests, getpass, time
from api_key import api_data
from api_key import weather_data
import tkinter as tk

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",170)


def speak(text):
    engine.say(text)
    engine.runAndWait()