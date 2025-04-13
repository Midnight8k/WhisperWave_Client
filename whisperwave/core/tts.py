import asyncio
import edge_tts
import pygame


def text_to_speech(text, voice='pt-PT-RaquelNeural', filename='output.mp3'):
    """
    Convert text to speech using Edge TTS and save it as an MP3 file.
    This is a synchronous wrapper around the async edge_tts call.
    Parameters:
    text (str): The text to be converted to speech.
    voice (str): The voice to be used (default is Portuguese - Duarte).
    filename (str): The name of the output MP3 file (default is 'output.mp3').
    """
    async def run_tts():
        communicate = edge_tts.Communicate(text=text, voice=voice, rate="+15%")
        await communicate.save(filename)

    asyncio.run(run_tts())


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.9)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()