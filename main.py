import requests
import json
import pyttsx3
import pyaudio
import vosk

# транслируем текст в речь
# проинициализируем переменные

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'ru')

for voice in voices:
    # print(voice.name)

    if voice.name == 'Microsoft Irina Desktop - Russian':
        tts.setProperty('voice', voice.id)

    model = vosk.Model('vosk-model-small-ru-0.4')
    record = vosk.KaldiRecognizer(model, 16000)
    pa = pyaudio.PyAudio()

    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=8000)
    stream.start_stream()


    def speak(say):
        tts.say(say)
        tts.runAndWait()


    def listen():
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(record.Result())
                if answer['text']:
                    yield answer['text']

    # выше — основа для голосового помощника

## настроим голосовой помощник для работы с Lorem ipsum

print('start')
lorem = ''

for text in listen():
    if text == 'создать':
        url = 'https://loripsum.net/api/10/short/headers'
        lorem = requests.get(url)
        print(lorem)
        lorem = lorem.text
        if lorem:
            speak('данные созданы')
    elif text == 'сохранить':  # сохранить текст как html
        if lorem:
            with open('lorem.html', 'w') as f:
                f.write(
                    '<!DOCTYPE html> \n <html lang="en"> \n <head> \n\t <meta charset="UTF-8"> \n\t <meta http-equiv="X-UA-Compatible" content="IE=edge"> \n\t   <meta name="viewport" content="width=device-width, initial-scale=1.0"> \n\t   <title>Document</title> \n</head> \n<body> \n \t')
                f.write(lorem)
                f.write('/n </body> \n</html>')
                speak('записано')
        else:
            speak('вы не сгенерировали текст')
    elif text == 'текст':  # сохранить текст как txt
        if lorem:
            with open('lorem.txt', 'w') as f:
                f.write(lorem)
                speak('записано')
        else:
            speak('вы не сгенерировали текст')
    else:
        print(text)