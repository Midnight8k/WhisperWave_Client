import pika

from whisperwave.core.tts import play_audio
from whisperwave.core.tts import text_to_speech


def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    try:
        if message:
            text_to_speech(message)
            play_audio('output.mp3')
    except:
        pass


class Consumer:
    connection = None
    channel = None
    queue = None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()

    def set_queue(self, queue):
        self.queue = queue

    def consume_queue(self):
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        print("Waiting for messages...")
        self.channel.start_consuming()
