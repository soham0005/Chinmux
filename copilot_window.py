import tkinter as tk
from tkinter import *
import ttkbootstrap as ttkb
import subprocess
import sys
import os


# sudo apt-get install python3-tk


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import the AIAgent class from chatbot.py
from chatbot import AIAgent

class ModernInteractiveChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chinmux For Linux")
        master.geometry("1000x800")
        
        # Initialize the AI agent
        self.ai_agent = AIAgent()
        
        # Use a modern style
        self.style = ttkb.Style("darkly")
        
        # Custom styles for messages
        self.style.configure("User.TLabel", background="#007bff", foreground="white", font=("Helvetica", 10))
        self.style.configure("Agent.TLabel", background="#6c757d", foreground="white", font=("Helvetica", 10))
        self.style.configure("AgentName.TLabel", foreground="#17a2b8", font=("Helvetica", 9, "bold"))

        self.messages = []

        # Main frame
        self.main_frame = ttkb.Frame(master)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Chat canvas
        self.canvas = ttkb.Canvas(self.main_frame, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar for canvas
        self.scrollbar = ttkb.Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame inside canvas for messages
        self.message_frame = ttkb.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.message_frame, anchor=NW)

        # Suggestion frame
        self.suggestion_frame = ttkb.Frame(self.message_frame)
        self.suggestion_frame.pack(expand=True, fill='both', pady=20)

        # Create buttons with modern design
        buttons = [
            ("Introduce the AI Agent", "🖌"),
            ("Text inviting friend to wedding", "✉"),
            ("Python script for daily email reports", "💻"),
            ("Suggest a recipe based on a photo of my fridge", "👁")
        ]

        for text, icon in buttons:
            button = ttkb.Button(self.suggestion_frame, text=f"{icon} {text}", 
                                 bootstyle="outline-info", command=lambda t=text: self.use_suggestion(t))
            button.pack(pady=5, padx=20, fill='x')
            # Add hover effect
            button.bind("<Enter>", lambda e, b=button: b.configure(bootstyle="info"))
            button.bind("<Leave>", lambda e, b=button: b.configure(bootstyle="outline-info"))

        # Input frame
        input_frame = ttkb.Frame(master)
        input_frame.pack(side='bottom', fill='x', padx=20, pady=20)

        # Input field with modern styling
        self.input_field = ttkb.Entry(input_frame, bootstyle="info")
        self.input_field.pack(side='left', expand=True, fill='x', ipady=5)
        self.input_field.bind('<Return>', self.send_message)

        # Send button with icon
        send_button = ttkb.Button(input_frame, text="Send", bootstyle="info", width=10, command=self.send_message)
        send_button.pack(side='right', padx=(5, 0))

        self.message_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.frame_width)

        # Enable mousewheel scrolling for Windows and MacOS
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # For Linux
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Bind the canvas to update scroll region when it's resized
        self.canvas.bind('<Configure>', self._configure_canvas)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:  # scroll down
            self.canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:  # scroll up
            self.canvas.yview_scroll(-1, "units")

    def _configure_canvas(self, event):
        if self.message_frame.winfo_reqwidth() != event.width:
            # Update the width of the frame to fit the canvas
            self.canvas.itemconfigure(self.canvas_window, width=event.width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def use_suggestion(self, suggestion):
        self.input_field.delete(0, 'end')
        self.input_field.insert(0, suggestion)
        self.send_message()

    def send_message(self, event=None):
        user_message = self.input_field.get().strip()
        if user_message:
            if self.suggestion_frame.winfo_viewable():
                self.suggestion_frame.pack_forget()
            self.add_message("You", user_message, True)
            self.input_field.delete(0, 'end')
            self.show_loader()
            # Process the message and get AI response
            self.master.after(100, self.process_and_respond)

    def show_loader(self):
        self.loader_frame = ttkb.Frame(self.message_frame)
        self.loader_frame.pack(pady=10, padx=20, anchor='w', fill='x')
        self.loader = ttkb.Label(self.loader_frame, text="AI is thinking...", bootstyle="info")
        self.loader.pack(side='left')
        self.master.update_idletasks()
        self.smooth_scroll_to_bottom()

    def hide_loader(self):
        if hasattr(self, 'loader_frame'):
            self.loader_frame.destroy()

    def process_and_respond(self):
        user_message = self.messages[-1]["content"]  # Get the last user message
        response = self.ai_agent.get_response(user_message)
        self.hide_loader()
        self.add_message("Agent", response, False)

    def add_message(self, sender, content, is_user):
        message_frame = ttkb.Frame(self.message_frame, style="TFrame")
        
        if is_user:
            message_bubble = ttkb.Label(message_frame, text=content, wraplength=400, 
                                        justify='left', style="User.TLabel",
                                        padding=(10, 5))
            message_bubble.pack(side='right')
        else:
            agent_frame = ttkb.Frame(message_frame, style="TFrame")
            agent_frame.pack(side='left', anchor='nw')
            
            sender_label = ttkb.Label(agent_frame, text=sender, style="AgentName.TLabel")
            sender_label.pack(side='top', anchor='w', padx=(0, 5), pady=(0, 2))
            
            message_bubble = ttkb.Label(agent_frame, text=content, wraplength=400,
                                        justify='left', style="Agent.TLabel",
                                        padding=(10, 5))
            message_bubble.pack(side='top', anchor='w')

        # Animate the message appearance
        self.animate_message(message_frame, is_user)

        self.messages.append({"sender": sender, "content": content})
        self.master.update_idletasks()
        self.smooth_scroll_to_bottom()

    def animate_message(self, widget, is_user):
        # Hide the widget initially
        widget.pack_forget()
        # Start animation
        self.fade_in_widget(widget, 0, is_user)

    def fade_in_widget(self, widget, alpha, is_user):
        if alpha < 1:
            alpha += 0.1
            widget.pack(pady=10, padx=20, anchor='e' if is_user else 'w', fill='x')
            widget.update()
            widget.after(50, self.fade_in_widget, widget, alpha, is_user)
        else:
            widget.pack(pady=10, padx=20, anchor='e' if is_user else 'w', fill='x')

    def smooth_scroll_to_bottom(self):
        def animate_scroll():
            current_position = self.canvas.yview()[1]
            if current_position < 1.0:
                self.canvas.yview_moveto(current_position + 0.05)
                self.master.after(10, animate_scroll)
            else:
                self.canvas.yview_moveto(1.0)

        self.master.after(0, animate_scroll)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    try:
        root = ttkb.Window()
        app = ModernInteractiveChatGUI(root)
        print("Chatwindow opened")
        app.run()
    except subprocess.CalledProcessError:
        print("Something went wrong")
    except Exception as e:
        print(f"An error occurred: {e}")