from gtts import gTTS
import pygame


def text_to_speech(text, lang='pt', filename='output.mp3'):
    """
    Convert text to speech and save it as an MP3 file.

    Parameters:
    text (str): The text to be converted to speech.
    lang (str): The language in which the text will be spoken (default is Portuguese).
    filename (str): The name of the output MP3 file (default is 'output.mp3').
    """

    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(filename)

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.9)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()