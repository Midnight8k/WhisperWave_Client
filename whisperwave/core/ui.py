import customtkinter as ctk
from whisperwave.core import http
import threading
from whisperwave.core.consumer import Consumer
from whisperwave.core.tts import play_audio, text_to_speech
import time


class Ui:

    def __init__(self):
        # Initialize the main window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.current_message = ""
        self.base_path = "http://localhost:2000"

        self.app = ctk.CTk()

    def _play_thread(self):
        if self.current_message == "The queue is Empty!":
            return
        text_to_speech(self.current_message)
        play_audio("output.mp3")

    """
    Temporary thread that runs every second to get all message and count them.
    """
    def _count_thread(self):
        while True:
            http_req = http.RequestHandler(f"{self.base_path}/get_all_messages")
            self.label_number_of_messages.configure(text=http_req.get().get("TotalMessages"))

            # TODO: This is a temporary fix for viewing the messages in the queue. When Rabbit were implemented remove this.
            time.sleep(1)

    def next_action(self):
        """
        Button action to display the next message in the queue. This function gets the latest message.

        return: void
        """
        http_req = http.RequestHandler(f"{self.base_path}/get_latest_message")
        self.current_message = http_req.get().get("Message")
        self.label_message.configure(text=self.current_message)

    def play_action(self):
        """
        Button action to play the message that is being displayed.

        return:void
        """
        thread = threading.Thread(target=self._play_thread)
        thread.start()
        
    def skip_action(self):
        # TODO: Include logic for skipping the message.
        self.label_message.configure(text="Skipped!")

    def consume(self):
        try:
            queue = "tts"
            print(f'Consuming: {queue}')
    
            consumer = Consumer()
            consumer.set_queue(queue)
            consumer.consume_queue()
        except:
            pass

    def draw_interface(self):
        self.app.title("Whisper Wave")
        self.app.geometry("300x400")

        # Create a label
        self.label_message = ctk.CTkLabel(self.app, text="Welcome!")
 
        # Create label
        self.label_number_of_messages = ctk.CTkLabel(self.app, text="0")
        
        self.label_message.pack(pady=10)
        self.label_number_of_messages.pack(pady=10)

        # Create Play and Skip buttons
        self.next_button = ctk.CTkButton(self.app, text="Next", command=self.next_action)
        self.play_button = ctk.CTkButton(self.app, text="Play", command=self.play_action)
        self.skip_button = ctk.CTkButton(self.app, text="Skip", command=self.skip_action)

        self.next_button.pack(pady=10)
        self.play_button.pack(pady=10)
        self.skip_button.pack(pady=10)

        # Start the temporary thread
        thread = threading.Thread(target=self._count_thread)
        thread.start()

        consumer_thread = threading.Thread(target=self.consume)
        consumer_thread.start()

        # Run the application
        self.app.mainloop()

