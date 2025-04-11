import random
import string
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime, timedelta

# Global variables
password_history = []
password_reccomend = []
current_password = ""
password_created_time = None
password_expiry_minutes = 1
is_dark_mode = False
current_bg_color = "#F0F4F8"

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

def apply_theme():
    global current_bg_color
    style.theme_use("clam")
    bg = "#282828" if is_dark_mode else "#EDE8D0"
    fg = "#FFFFFF" if is_dark_mode else "#000000"
    entry_bg = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    button_bg = "#333333" if is_dark_mode else "#E0E0E0"
    button_fg = "#FFFFFF" if is_dark_mode else "#000000"
    current_bg_color = bg

    root.configure(bg=bg)
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TCheckbutton", background=bg, foreground=fg)
    style.configure("TButton", background=button_bg, foreground=button_fg)
    style.configure("TEntry", fieldbackground=entry_bg, foreground=fg, insertcolor=fg)

     # Custom styles for Adjust and Save buttons
    style.configure("Adjust.TButton", background=button_bg, foreground=button_fg)
    style.configure("Save.TButton", background=button_bg, foreground=button_fg)

    style.map("Adjust.TButton",
              background=[("active", "#444444" if is_dark_mode else "#D6D6D6")],
              foreground=[("active", "#FFFFFF" if is_dark_mode else "#000000")])

    style.map("Save.TButton",
              background=[("active", "#555555" if is_dark_mode else "#CCCCCC")],
              foreground=[("active", "#FFFFFF" if is_dark_mode else "#000000")])

    try:
        current_text = ageLabel.cget("text").lower()
        ageLabel.config(bg=current_bg_color, fg="red" if "expired" in current_text else "green")
    except:
        pass

class GeneratedPassword:
    def __init__(self, length, phrases, characters, exclude):
        self.length = int(length) if length.isdigit() else 0
        self.phrases = [p.strip() for p in phrases.split(",") if p.strip()] if use_phrases.get() else []
        self.characters = [c.strip() for c in characters.split(",") if c.strip()] if use_characters.get() else []
        self.exclude = set(exclude) if use_exclude.get() else set()

    def is_valid(self):
        if self.length == 0 or self.length > 25:
            displayedMessage.config(text="Invalid password length")
            return False
        if sum(len(p) for p in self.phrases) + sum(len(c) for c in self.characters) > self.length:
            displayedMessage.config(text="Phrases and characters too long")
            return False
        if any(len(c) != 1 for c in self.characters):
            displayedMessage.config(text="Each character must be one character long")
            return False
        return True

    def generate(self):
        result = ""
        used_phrases, used_chars = set(), set()
        pool = ''.join(c for c in string.ascii_letters + string.digits + string.punctuation if c not in self.exclude)

        while len(result) < self.length:
            choice = random.choice(["phrase", "char", "random"])
            if choice == "phrase" and self.phrases:
                unused = [p for p in self.phrases if p not in used_phrases]
                if unused:
                    p = random.choice(unused)
                    if len(result) + len(p) <= self.length:
                        result += p
                        used_phrases.add(p)
            elif choice == "char" and self.characters:
                unused = [c for c in self.characters if c not in used_chars and c not in self.exclude]
                if unused and len(result) + 1 <= self.length:
                    c = random.choice(unused)
                    result += c
                    used_chars.add(c)
            elif choice == "random" and pool:
                result += random.choice(pool)

            if len(result) > self.length:
                result = result[:self.length]
        return result

def generate_password():
    global current_password, password_created_time
    password_obj = GeneratedPassword(givenLen.get(), givenPhrase.get(), givenChar.get(), excludeChars.get())
    if password_obj.is_valid():
        pw1 = password_obj.generate()
        pw2 = password_obj.generate()
        current_password = pw1
        password_created_time = datetime.now()
        displayedMessage.config(text=pw1)
        password_history.append(pw1)
        password_reccomend.append(pw2)
        adjustButton.config(state=tk.NORMAL)
        saveButton.config(state=tk.NORMAL)
        previous.config(text=", ".join(password_history[-5:]))
        reccomend.config(text=", ".join(password_reccomend[-5:]))
        check_strength(pw1)

def check_strength(pw):
    has_special = any(c in string.punctuation for c in pw)
    if len(pw) < 10 and has_special:
        msg = "Weak: too short"
    elif not has_special and len(pw) >= 10:
        msg = "Weak: no special chars"
    elif len(pw) < 10:
        msg = "Very Weak"
    else:
        msg = "Strong Password"
    strengthSuggestion.config(text=msg)

def show_adjust_fields():
    adjustFrame.grid()

def apply_adjustments():
    global current_password
    exclude = adjustExcludeEntry.get()
    add = adjustAddEntry.get()
    new_pw = ''.join(c for c in current_password if c not in exclude)
    new_pw += add
    current_password = new_pw[:25]
    displayedMessage.config(text=current_password)
    check_strength(current_password)

def reset_all():
    global current_password, password_created_time
    for entry in [givenLen, givenPhrase, givenChar, excludeChars, adjustExcludeEntry, adjustAddEntry]:
        entry.delete(0, tk.END)
    displayedMessage.config(text="")
    current_password = ""
    password_created_time = None
    adjustButton.config(state=tk.DISABLED)
    saveButton.config(state=tk.DISABLED)
    ageLabel.config(text="", bg=current_bg_color, fg="black")
    adjustFrame.grid_remove()
    use_phrases.set(True)
    use_characters.set(True)
    use_exclude.set(True)

def save_password():
    if current_password:
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, "w") as f:
                f.write(current_password)

def update_age():
    if password_created_time:
        delta = datetime.now() - password_created_time
        mins, secs = divmod(delta.total_seconds(), 60)
        if delta > timedelta(minutes=password_expiry_minutes):
            ageLabel.config(text="Password expired — generate new one!", fg="red", bg=current_bg_color)
            saveButton.config(state=tk.DISABLED)
        else:
            ageLabel.config(text=f"Password age: {int(mins)}m {int(secs)}s", fg="green", bg=current_bg_color)
    root.after(1000, update_age)

def main():
    global root, style, givenLen, givenPhrase, givenChar, excludeChars
    global displayedMessage, adjustButton, saveButton, strengthSuggestion
    global adjustFrame, adjustExcludeEntry, adjustAddEntry
    global previous, reccomend, ageLabel
    global use_phrases, use_characters, use_exclude

    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("620x900")
    style = ttk.Style()

    use_phrases = tk.BooleanVar(value=True)
    use_characters = tk.BooleanVar(value=True)
    use_exclude = tk.BooleanVar(value=True)

    apply_theme()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)

    # UI layout
    ttk.Label(main_frame, text="🔐 Password Generator", font=('Segoe UI', 20)).grid(row=0, column=0, sticky="w")
    ttk.Button(main_frame, text="🌙 Toggle Dark Mode", command=toggle_dark_mode).grid(row=0, column=1, sticky="e")

    ttk.Label(main_frame, text="Length:").grid(row=1, column=0, sticky="e")
    givenLen = ttk.Entry(main_frame, width=40)
    givenLen.grid(row=1, column=1, pady = 10)

    ttk.Checkbutton(main_frame, text="Include phrases", variable=use_phrases).grid(row=2, column=0, columnspan=2, sticky="w")
    ttk.Label(main_frame, text="Phrases (comma-separated):").grid(row=3, column=0, sticky="e")
    givenPhrase = ttk.Entry(main_frame, width=40)
    givenPhrase.grid(row=3, column=1, pady = 10)

    ttk.Checkbutton(main_frame, text="Include characters", variable=use_characters).grid(row=4, column=0, columnspan=2, sticky="w")
    ttk.Label(main_frame, text="Characters (comma-separated):").grid(row=5, column=0, sticky="e")
    givenChar = ttk.Entry(main_frame, width=40)
    givenChar.grid(row=5, column=1, pady = 10)

    ttk.Checkbutton(main_frame, text="Exclude characters", variable=use_exclude).grid(row=6, column=0, columnspan=2, sticky="w")
    ttk.Label(main_frame, text="Exclude (comma-separated):").grid(row=7, column=0, sticky="e")
    excludeChars = ttk.Entry(main_frame, width=40)
    excludeChars.grid(row=7, column=1, pady = 10)

    displayedMessage = ttk.Label(main_frame, text="", font=('Segoe UI', 14, 'bold'))
    displayedMessage.grid(row=8, column=0, columnspan=2, pady=10)

    ageLabel = tk.Label(main_frame, text="", font=('Segoe UI', 11), bg=current_bg_color)
    ageLabel.grid(row=9, column=0, columnspan=2)

    strengthSuggestion = ttk.Label(main_frame, text="", foreground="#D72638")
    strengthSuggestion.grid(row=10, column=0, columnspan=2, pady=5)

    ttk.Button(main_frame, text="Generate Password", command=generate_password).grid(row=11, column=0, columnspan=2, pady=10)

    ttk.Label(main_frame, text="Previous passwords:").grid(row=12, column=0, sticky="e")
    previous = ttk.Label(main_frame, text="")
    previous.grid(row=12, column=1, sticky="w")

    ttk.Label(main_frame, text="Recommended passwords:").grid(row=13, column=0, sticky="e")
    reccomend = ttk.Label(main_frame, text="")
    reccomend.grid(row=13, column=1, sticky="w")

    adjustButton = ttk.Button(main_frame, text="Adjust Password", style="Adjust.TButton", command=show_adjust_fields, state=tk.DISABLED)
    adjustButton.grid(row=14, column=0, columnspan=2, pady=5)

    saveButton = ttk.Button(main_frame, text="Save Password", style="Save.TButton", command=save_password, state=tk.DISABLED)
    saveButton.grid(row=15, column=0, columnspan=2)

    ttk.Button(main_frame, text="Reset All", command=reset_all).grid(row=16, column=0, columnspan=2, pady=10)

    adjustFrame = ttk.Frame(main_frame)
    ttk.Label(adjustFrame, text="Characters to exclude:").grid(row=0, column=0)
    adjustExcludeEntry = ttk.Entry(adjustFrame)
    adjustExcludeEntry.grid(row=0, column=1, pady = 10)

    ttk.Label(adjustFrame, text="Characters to add:").grid(row=1, column=0)
    adjustAddEntry = ttk.Entry(adjustFrame)
    adjustAddEntry.grid(row=1, column=1, pady = 10)

    ttk.Button(adjustFrame, text="Apply Adjustments", command=apply_adjustments).grid(row=2, column=0, columnspan=2)
    adjustFrame.grid(row=17, column=0, columnspan=2)
    adjustFrame.grid_remove()

    update_age()
    root.mainloop()

if __name__ == "__main__":
    main()
