import pyttsx3
import speech_recognition as sr
from functions import request_error, listen_a_command, check_command
engine = pyttsx3.init()


def main():
    query = listen_a_command()
    check_command(query)


if __name__ == '__main__':
    while True:
        try:
            main()
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            request_error()
        engine.runAndWait()
