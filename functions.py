import sys
import pyttsx3
import webbrowser
import speech_recognition as sr
from youtube_scraping import scrap_youtube
from mail_scraping import scrap_mail
from commands_list import commands
from config import receivers, data

engine = pyttsx3.init()
engine.setProperty('rate', 270)
r = sr.Recognizer()


def listen_a_command():
    """Function for listening"""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 0.5)
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


def check_receiver(receiver):
    """Function which checks values in dictionary"""
    for k, v in receivers.items():
        if receiver.lower() in v:
            return k
    else:
        unknown_value()
        return False


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
        if int(video_num) <= 0 or int(video_num) > 10:
            unknown_value()
            return False

    except sr.UnknownValueError:
        unknown_value()
        return False

    try:
        scrap_youtube(task, int(video_num))
    except ValueError:
        unknown_value()
        return False


def write_a_mail():
    """Function for write a letter by @mail.ru"""
    engine.say('Кому вы хотите написать письмо?')
    engine.runAndWait()
    try:
        receiver = listen_a_command()
        mail = check_receiver(receiver)
    except sr.UnknownValueError:
        unknown_value()
        return False
    engine.say('Скажите, что вы хотите написать')
    engine.runAndWait()
    try:
        text = listen_a_command()
    except sr.UnknownValueError:
        unknown_value()
        return False
    scrap_mail(data['login'], data['password'], mail, text)
