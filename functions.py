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


def ask_question(question):
    """Function for asking a question"""
    engine.say(question)
    engine.runAndWait()


def listen_a_command() -> str:
    """Function for listening"""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 0.5)
        audio: sr.AudioData = r.listen(source)
    return r.recognize_google(audio, language='ru')


def check_command(query: str):
    """Function which checks values in dictionary"""
    for k, v in commands.items():
        if query.lower() in v:
            globals()[k]()
            break
    else:
        unknown_value()


def check_receiver(receiver) -> str | bool:
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
    ask_question('Я не поняла что ты сказал!')


def request_error():
    """Function which calls when RequestError"""
    ask_question('Произошла ошибка в запросе!')


def open_browser():
    """Functions for opening browser"""
    webbrowser.open('https://www.google.ru/', new=2, autoraise=True)
    ask_question('Браузер открыт!')


def open_youtube() -> bool:
    """Function for playing youtube video"""
    ask_question('Какое видео вы хотите посмотреть?')

    try:
        task: str = listen_a_command()
    except sr.UnknownValueError:
        unknown_value()
        return False

    ask_question('Назовите номер видео от одного до десяти:')

    try:
        video_num: str = listen_a_command()
        is_correct_number: bool = int(video_num) in range(0, 11)

        if not is_correct_number:
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


def write_a_mail() -> bool:
    """Function for write a letter by @mail.ru"""
    ask_question('Кому вы хотите написать письмо?')

    try:
        receiver: str = listen_a_command()
        mail: str = check_receiver(receiver)
    except sr.UnknownValueError:
        unknown_value()
        return False

    ask_question('Скажите, что вы хотите написать')

    try:
        text: str = listen_a_command()
    except sr.UnknownValueError:
        unknown_value()
        return False

    scrap_mail(data, mail, text)
