import tkinter as tk
from tkinter import scrolledtext, ttk
import traceback
from .logger import logger
from .settings import SettingsManager
from .controller import AssistantController

class VoiceAssistantGUI:
    def __init__(self, root, settings_manager: SettingsManager):
        self.root = root
        self.settings = settings_manager
        self.root.title("🎙️ Voice Assistant (MVC)")
        
        # Center the window
        window_width = 500
        window_height = 650
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # Force window to front
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        root.focus_force()

        # Initialize Controller
        self.controller = AssistantController(self.settings, self.update_status)
        self.controller.set_chat_callback(self.append_chat)

        # --- UI Elements ---
        
        # Chat History Area
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # Settings Frame
        settings_frame = tk.Frame(root)
        settings_frame.pack(pady=5, fill=tk.X, padx=20)
        
        tk.Label(settings_frame, text="Voice Accent:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.accents = list(self.controller.accents_map.keys())
        self.accent_var = tk.StringVar(value=self.settings.get("accent", "🇺🇸 US English"))
        self.accent_combo = ttk.Combobox(settings_frame, textvariable=self.accent_var, 
                                         values=self.accents, state="readonly", width=20)
        self.accent_combo.pack(side=tk.LEFT, padx=10)
        self.accent_combo.bind("<<ComboboxSelected>>", self.on_accent_change)

        # Status Label
        self.status_label = tk.Label(root, text="Ready", font=("Arial", 10, "italic"), fg="gray")
        self.status_label.pack(pady=5)

        # Control Button
        self.start_button = tk.Button(root, text="Start Listening", command=self.toggle_listening, 
                                      font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", height=2)
        self.start_button.pack(padx=10, pady=10, fill=tk.X)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_accent_change(self, event):
        new_accent = self.accent_var.get()
        self.settings.set("accent", new_accent)
        logger.info(f"Accent changed to: {new_accent}")

    def toggle_listening(self):
        if not self.controller.is_running:
            # Start
            self.start_button.config(text="Stop Listening", bg="#f44336") # Red
            self.controller.start_listening()
        else:
            # Stop
            self.start_button.config(text="Stopping...", state=tk.DISABLED)
            self.controller.stop_listening()
            # The controller thread will exit and call update_status, but we might need to reset button manually if it hangs?
            # Actually, let's rely on the controller loop finishing to reset UI?
            # No, the controller loop runs in a thread. When it finishes, we need to reset UI.
            # But the controller doesn't have a "finished" callback other than update_status.
            # Let's add a check in update_status or just reset immediately?
            # Better: The controller loop will break, and we can reset UI then.
            # But we need to know when it breaks.
            # For now, let's just wait a bit or let the user click again?
            # Actually, the controller loop calls update_status.
            # We can check self.controller.is_running in a loop or just reset button when we get a "Ready" status?
            self.root.after(1000, self.check_stopped)

    def check_stopped(self):
        if not self.controller.is_running:
             self.start_button.config(text="Start Listening", bg="#4CAF50", state=tk.NORMAL)
             self.update_status("Ready", "gray")
        else:
             self.root.after(500, self.check_stopped)

    def update_status(self, text, color="gray"):
        # Ensure thread safety for Tkinter
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))

    def append_chat(self, sender, message):
        self.root.after(0, lambda: self._append_chat_safe(sender, message))

    def _append_chat_safe(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def on_close(self):
        self.controller.stop_listening()
        self.root.destroy()
