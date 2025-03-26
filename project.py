from dotenv import load_dotenv
load_dotenv()
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import os
from ttkthemes import ThemedTk
from openai import OpenAI

class IndianCultureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Indian Culture Explorer")
        self.root.geometry("800x600")

        # Set theme
        self.root.set_theme("elegance")

        # Colors
        self.bg_color = "#FFF5E6"  # Light cream
        self.accent_color = "#FF6B6B"  # Warm red
        self.text_color = "#2C3E50"  # Dark blue-grey

        self.root.configure(bg=self.bg_color)

        self.setup_gui()

        # Initialize OpenAI client for Grok
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1",
        )

    def setup_gui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.title_label = ttk.Label(
            self.header_frame,
            text="Indian Culture Explorer",
            font=("Helvetica", 24, "bold"),
            foreground=self.accent_color
        )
        self.title_label.pack()

        self.subtitle_label = ttk.Label(
            self.header_frame,
            text="Explore the rich heritage and traditions of India",
            font=("Helvetica", 12),
            foreground=self.text_color
        )
        self.subtitle_label.pack()

        # Chat area
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg="white",
            height=20
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.config(state=tk.DISABLED)

        # Input area
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(10, 0))

        self.query_entry = ttk.Entry(
            self.input_frame,
            font=("Helvetica", 11)
        )
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.send_button = ttk.Button(
            self.input_frame,
            text="Ask",
            command=self.send_query,
            style="Accent.TButton"
        )
        self.send_button.pack(side=tk.RIGHT)

        # Bind Enter key to send query
        self.query_entry.bind("<Return>", lambda e: self.send_query())

        # Style configuration
        style = ttk.Style()
        style.configure(
            "Accent.TButton",
            background=self.accent_color,
            foreground="white",
            padding=10
        )

    def send_query(self):
        query = self.query_entry.get().strip()
        if not query:
            return

        # Clear input
        self.query_entry.delete(0, tk.END)

        # Add user message to chat
        self.add_message("You", query)

        try:
            # Use the initialized OpenAI client for Grok
            completion = self.client.chat.completions.create(
                model="grok-2-1212",  # Update to grok-1
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in Indian culture, traditions, and heritage."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
            )

            response_text = completion.choices[0].message.content

            self.add_message("Assistant", response_text)

        except Exception as e:
            self.add_message("System", f"Error: {str(e)}")

    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")

        # Format message with sender and timestamp
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"

        # Add message to display
        self.chat_display.insert(tk.END, formatted_message)

        # Color code based on sender
        tag_name = f"message_{timestamp}"
        self.chat_display.tag_add(tag_name, f"end-{len(formatted_message) + 1}c", "end-1c")

        if sender == "You":
            self.chat_display.tag_config(tag_name, foreground="#2980b9")  # Blue
        elif sender == "Assistant":
            self.chat_display.tag_config(tag_name, foreground="#27ae60")  # Green
        else:
            self.chat_display.tag_config(tag_name, foreground="#c0392b")  # Red

        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = ThemedTk(theme="elegance")
    app = IndianCultureApp(root)
    root.mainloop()