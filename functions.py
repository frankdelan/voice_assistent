import sys
import pyttsx3
import webbrowser
import speech_recognition as sr
from youtube_scraping import scrap
from commands_list import commands

engine = pyttsx3.init()
engine.setProperty('rate', 270)
r = sr.Recognizer()


def listen_a_command():
    """Function for listening"""
    with sr.Microphone() as source:
        audio = r.listen(source)
    return r.recognize_google(audio, language='ru')


def check_command(query):
    """Function which checks values in dictionary"""
    for k, v in commands.items():
        if query.lower() in v:
            globals()[k]()
            break
    else:
        unknown_value()

def close_assistent():
    """Close program"""
    sys.exit()

def unknown_value():
    """Undefined phrase"""
    engine.say('Я не поняла что ты сказал!')


def request_error():
    """Function which calls when RequestError"""
    engine.say('Произошла ошибка в запросе!')


def open_browser():
    """Functions for browser's opening"""
    webbrowser.open('https://www.google.ru/', new=2, autoraise=True)
    engine.say('Браузер открыт!')


def open_youtube():
    """Function for playing youtube video"""
    engine.say('Какое видео вы хотите посмотреть?')
    engine.runAndWait()
    try:
        task = listen_a_command()
    except sr.UnknownValueError:
        unknown_value()
        return False
    engine.say('Назовите номер видео от одного до десяти:')
    engine.runAndWait()
    try:
        video_num = listen_a_command()
    except sr.UnknownValueError:
        unknown_value()
        return False
    scrap(task, int(video_num))
