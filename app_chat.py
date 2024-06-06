import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import wikipedia
import os
import cv2
import numpy as np

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with our Companion")
        self.root.geometry("800x900")
        self.root.configure(bg='#2c3e50')

        # Define paths for saving images and videos
        self.image_directory = os.path.join(os.getcwd(), "images")
        self.video_directory = os.path.join(os.getcwd(), "videos")

        # Ensure directories exist
        os.makedirs(self.image_directory, exist_ok=True)
        os.makedirs(self.video_directory, exist_ok=True)

        self.heading_frame = tk.Frame(root, bg='#34495e', pady=10)
        self.heading_frame.pack(fill=tk.X)
        self.heading_label = tk.Label(self.heading_frame, text="Chat with our Companion", font=("Helvetica", 24, "bold"), fg='#ecf0f1', bg='#34495e')
        self.heading_label.pack()

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='#ecf0f1', fg='#2c3e50', font=("Helvetica", 12), padx=10, pady=10)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input_frame = tk.Frame(root, bg='#2c3e50')
        self.user_input_frame.pack(padx=10, pady=10, fill=tk.X)

        self.user_input = tk.Entry(self.user_input_frame, font=("Helvetica", 14), bg='#ecf0f1', fg='#2c3e50', relief=tk.GROOVE, bd=2)
        self.user_input.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.user_input_frame, text="Send", command=self.send_message, font=("Helvetica", 14, "bold"), bg='#3498db', fg='#ecf0f1', activebackground='#2980b9', relief=tk.RAISED, bd=2)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.add_message("Bot", "Hello! Let's chat.\nYou can type 'bye', 'exit', or 'end' to stop the conversation.")

    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.lower() in ['bye', 'exit', 'end']:
            self.add_message("Bot", "Goodbye! Have a great day!")
            self.root.after(2000, self.root.destroy)  # Close the window after 2 seconds
            return

        self.add_message("You", user_message)
        self.user_input.delete(0, tk.END)

        response, image_path, video_path = self.get_bot_response(user_message)
        self.add_message("Bot", response)

        if image_path:
            self.show_image(image_path)
        if video_path:
            self.show_video(video_path)

    def get_bot_response(self, message):
        # Fetch information from Wikipedia based on the user's input
        try:
            wiki_summary = wikipedia.summary(message, sentences=2)
        except wikipedia.exceptions.DisambiguationError:
            # If Wikipedia disambiguation error occurs, provide a general message
            wiki_summary = "It seems there are multiple possibilities. Can you be more specific?"
        except wikipedia.exceptions.PageError:
            # If Wikipedia page error occurs, provide a general message
            wiki_summary = "Sorry, I couldn't find any information on that topic."

        # Generate an image with the user's input text
        image_path = self.generate_image(message)

        # Generate a video with the user's input text
        video_path = self.generate_video(message)

        return wiki_summary, image_path, video_path

    def generate_image(self, message):
        # Create an image with the user's input text
        image_path = os.path.join(self.image_directory, f"{message}.png")
        img = Image.new('RGB', (400, 200), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 20)
        d.text((10, 10), message, fill=(0, 0, 0), font=font)
        img.save(image_path)
        return image_path

    def generate_video(self, message):
        # Create a simple video with the user's input text
        video_path = os.path.join(self.video_directory, f"{message}.avi")
        
        width, height = 640, 480
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, 1.0, (width, height))
        
        for _ in range(10):
            frame = np.zeros((height, width, 3), np.uint8)
            cv2.putText(frame, message, (50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            out.write(frame)
        
        out.release()
        return video_path

    def show_image(self, image_path):
        if not os.path.exists(image_path):
            messagebox.showerror("Error", "Image not found!")
            return

        image_window = tk.Toplevel(self.root)
        image_window.title("Generated Image")
        img = ImageTk.PhotoImage(Image.open(image_path))
        panel = tk.Label(image_window, image=img)
        panel.image = img
        panel.pack()

    def show_video(self, video_path):
        if not os.path.exists(video_path):
            messagebox.showerror("Error", "Video not found!")
            return

        messagebox.showinfo("Video Generated", f"Video saved at: {video_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
