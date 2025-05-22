'''
Этот модуль планировался и даже использовался (в первом уроке) для создания аудио-файла .mp3 из файла .txt.
Однако, в итоге я от него отказался в пользу синтеза речи в Clipchamp
'''

from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import time
import os


def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('.', ".\\'ъ").replace(',', ",\\'ъ") # Заменяем апострофы на специальный маркер ударения
    print(text)
    return text


def save_audio(audio_data, folder_path, filename):
    output_file = os.path.join(folder_path, f"{filename}.mp3")
    audio_data.export(output_file, format="mp3")
    print(f"Аудиофайл сохранен как {output_file}")


def speak(text, lang='ru', volume_increase_db=10, folder_path=None, filename=None):
    # Создание аудио
    tts = gTTS(text=text, lang=lang, slow=False)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Загрузка и изменение громкости
    audio = AudioSegment.from_mp3(mp3_fp)
    louder_audio = audio + volume_increase_db

    if folder_path and filename:
        save_audio(louder_audio, folder_path, filename)

    # # Преобразование в numpy array
    # samples = np.array(louder_audio.get_array_of_samples())

    # # Воспроизведение
    # sd.play(samples, louder_audio.frame_rate)
    # sd.wait()


if __name__ == "__main__":
    # Чтение текста из файла
    file_path = r'lesson_1\lesson_1.txt'  # укажите путь к вашему текстовому файлу
    text = read_text_from_file(file_path)

    # Озвучивание и сохранение аудиофайла
    folder_path = r'lesson_1'  # укажите путь к папке, куда хотите сохранить аудиофайл
    filename = 'lesson_1'       # укажите имя аудиофайла без расширения
    speak(text, filename=filename, folder_path=folder_path)