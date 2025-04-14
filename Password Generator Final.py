import random
import string
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime, timedelta

''' Variables to initialize the lists where reccomended and previous passwords are held.
Background color, whether it is in dark mode (boolean variable set to false), and maximum password age
before expiration is initialized. 
'''
password_history = []
password_reccomend = []
current_password = ""
password_created_time = None
password_expiry_minutes = 1
is_dark_mode = False
current_bg_color = "#F0F4F8"

# This function toggles dark mode.
def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

# Function allows for the GUI to switch between dark and light mode.
def apply_theme():
    
    # Uses if-else statements to switch modes (dark/light).
    global current_bg_color
    style.theme_use("clam")
    bg = "#282828" if is_dark_mode else "#EDE8D0"
    fg = "#FFFFFF" if is_dark_mode else "#000000"
    entry_bg = "#1E1E1E" if is_dark_mode else "#FFFFFF"
    button_bg = "#333333" if is_dark_mode else "#E0E0E0"
    button_fg = "#FFFFFF" if is_dark_mode else "#000000"
    current_bg_color = bg

    # Changes appearance of buttons/entries/labels when switching modes.
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

# This class takes the traits into account to make a password that may/may not be generated (depending on the viability of the specifications.)
class GeneratedPassword:
    
    # Initializes traits of the password as entered by the user: length, phrases/characters to be included, and characters to be excluded.
    def __init__(self, length, phrases, characters, exclude):
        self.length = int(length) if length.isdigit() else 0
        self.phrases = [p.strip() for p in phrases.split(",") if p.strip()] if use_phrases.get() else []
        self.characters = [c.strip() for c in characters.split(",") if c.strip()] if use_characters.get() else []
        self.exclude = set(exclude) if use_exclude.get() else set()

    # Checks if the password is valid, and displays the appropriate message if it is not.
    def is_valid(self):
        
        # Checks if the entered length is more than 25 (not allowed)
        if self.length == 0 or self.length > 25:
            displayedMessage.config(text="Invalid password length")
            return False
        
        # Checks if the combined length of the specified phrases and characters are more than the specified length.
        if sum(len(p) for p in self.phrases) + sum(len(c) for c in self.characters) > self.length:
            displayedMessage.config(text="Phrases and characters too long")
            return False
        
        # Checks if the user enters more than one character (without separating them with a comma)
        if any(len(c) != 1 for c in self.characters):
            displayedMessage.config(text="Each character must be one character long")
            return False
        return True

    # This method generates the password.
    def generate(self):
        result = ""
        used_phrases, used_chars = set(), set()
        pool = ''.join(c for c in string.ascii_letters + string.digits + string.punctuation if c not in self.exclude)

        # While the length of the password is less than the specified length, run through the loop.
        while len(result) < self.length:
            
            # Randomly choose between concactenating the phrase, character, or a random character to the password.
            choice = random.choice(["phrase", "char", "random"])
            
            # If it is randomly chosen to concactenate a phrase, and if the phrase is not used, add it to the password.
            if choice == "phrase" and self.phrases:
                unused = [p for p in self.phrases if p not in used_phrases]
                if unused:
                    p = random.choice(unused)
                    if len(result) + len(p) <= self.length:
                        result += p
                        used_phrases.add(p)
                        
            # If it is randomly chosen to concactenate a phrase, and if the phrase is not used, add it to the password.          
            elif choice == "char" and self.characters:
                unused = [c for c in self.characters if c not in used_chars and c not in self.exclude]
                if unused and len(result) + 1 <= self.length:
                    c = random.choice(unused)
                    result += c
                    used_chars.add(c)
                    
            # If it is randomly chosen to concatenate a random character, add the character to the password.
            elif choice == "random" and pool:
                result += random.choice(pool)
                
            # If the generated password accidentally exceeds the length, trim it so that it the length of the password is the same as
            # the one that the user specified.
            if len(result) > self.length:
                result = result[:self.length]
        
        # Return the password.
        return result

def generate_password():
    global current_password, password_created_time
    
    # Create an instance of the class GeneratedPassword using the specifictions the user provided.
    password_obj = GeneratedPassword(givenLen.get(), givenPhrase.get(), givenChar.get(), excludeChars.get())
    
    # If the password is valid, generate two passwords (one of which will serves as the reccomended password the user will be able to see later as a reccomendation).
    if password_obj.is_valid():
        pw1 = password_obj.generate()
        pw2 = password_obj.generate()
        current_password = pw1
        password_created_time = datetime.now()
        
        # Show the generated password.
        displayedMessage.config(text=pw1)
        
        # Save the generated password.
        password_history.append(pw1)
        
        # Save the second password in a list where the reccomended passwords are saved.
        password_reccomend.append(pw2)
        
        adjustButton.config(state=tk.NORMAL)
        saveButton.config(state=tk.NORMAL)
        
        # Show the previous five passwords generated, and password reccomendations based on the previous five passwords.
        previous.config(text=", ".join(password_history[-5:]))
        reccomend.config(text=", ".join(password_reccomend[-5:]))
        
        # Check the strength of the current generated password.
        check_strength(pw1)

# This function checks the strength of the password, displays strength and reason behind why its weak (if the password is weak)
# Weak if less than ten characters and/or no special characters. Otherwise it's a strong password.
def check_strength(pw):
    has_special = any(c in string.punctuation for c in pw)
    if len(pw) < 10 and has_special:
        msg = "Weak: less than 10 characters"
    elif not has_special and len(pw) >= 10:
        msg = "Weak: no special chars"
    elif len(pw) < 10 and not has_special:
        msg = "Very weak: less than 10 characters and no special characters"
    else:
        msg = "Strong Password"
    strengthSuggestion.config(text=msg)

def show_adjust_fields():
    adjustFrame.grid()

# Allows user to apply adjusments to the password based on what characters the user has specified to include/exclude.
def apply_adjustments():
    global current_password
    exclude = adjustExcludeEntry.get()
    add = adjustAddEntry.get()
    new_pw = ''.join(c for c in current_password if c not in exclude)
    new_pw += add
    current_password = new_pw[:25]
    displayedMessage.config(text=current_password)
    check_strength(current_password)

# Resets all entry fields.
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
    strengthSuggestion.config(text="")
    adjustFrame.grid_remove()
    use_phrases.set(True)
    use_characters.set(True)
    use_exclude.set(True)

# Allows user to download and save the password on their computer.
def save_password():
    if current_password:
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, "w") as f:
                f.write(current_password)

# Updates the age of the password: using a timer (which will be displayed), indicate the age of the password since its generation.
# The password has expired if it has been more than 1 minute since its generation.
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

    # Entry boxes where user will enter length
    ttk.Label(main_frame, text="Length (must be no more than 25):").grid(row=1, column=0, sticky="e")
    givenLen = ttk.Entry(main_frame, width=40)
    givenLen.grid(row=1, column=1, pady = 10)

    # Entry boxes where user will enter phrases
    ttk.Checkbutton(main_frame, text="Include phrases", variable=use_phrases).grid(row=2, column=0, columnspan=2, sticky="w")
    ttk.Label(main_frame, text="Phrases (comma-separated):").grid(row=3, column=0, sticky="e")
    givenPhrase = ttk.Entry(main_frame, width=40)
    givenPhrase.grid(row=3, column=1, pady = 10)

    # Entry boxes where user will enter characters
    ttk.Checkbutton(main_frame, text="Include characters", variable=use_characters).grid(row=4, column=0, columnspan=2, sticky="w")
    ttk.Label(main_frame, text="Characters (comma-separated):").grid(row=5, column=0, sticky="e")
    givenChar = ttk.Entry(main_frame, width=40)
    givenChar.grid(row=5, column=1, pady = 10)

    # Entry boxes where user will enter characters to exclude
    ttk.Checkbutton(main_frame, text="Exclude characters", variable=use_exclude).grid(row=6, column=0, columnspan=2, sticky="w")
    ttk.Label(main_frame, text="Exclude (comma-separated):").grid(row=7, column=0, sticky="e")
    excludeChars = ttk.Entry(main_frame, width=40)
    excludeChars.grid(row=7, column=1, pady = 10)

    # Initializes label where generated password will show
    displayedMessage = ttk.Label(main_frame, text="", font=('Segoe UI', 14, 'bold'))
    displayedMessage.grid(row=8, column=0, columnspan=2, pady=10)

    # Label displaying age
    ageLabel = tk.Label(main_frame, text="", font=('Segoe UI', 11), bg=current_bg_color)
    ageLabel.grid(row=9, column=0, columnspan=2)

    # Label displaying strength
    strengthSuggestion = ttk.Label(main_frame, text="", foreground="#D72638")
    strengthSuggestion.grid(row=10, column=0, columnspan=2, pady=5)

    # Button that will be used to generate the password
    ttk.Button(main_frame, text="Generate Password", command=generate_password).grid(row=11, column=0, columnspan=2, pady=10)

    # Labels that show the previously generated password (last 5)
    ttk.Label(main_frame, text="Previous passwords:").grid(row=12, column=0, sticky="e")
    previous = ttk.Label(main_frame, text="")
    previous.grid(row=12, column=1, sticky="w")

    # Labels that show the reccomended passwords (based on last 5 specifications)
    ttk.Label(main_frame, text="Recommended passwords:").grid(row=13, column=0, sticky="e")
    reccomend = ttk.Label(main_frame, text="")
    reccomend.grid(row=13, column=1, sticky="w")

    # Button that opens up entry fields where user can enter specifications as to which characters they would like to exclude/add on to the generated password
    adjustButton = ttk.Button(main_frame, text="Adjust Password", style="Adjust.TButton", command=show_adjust_fields, state=tk.DISABLED)
    adjustButton.grid(row=14, column=0, columnspan=2, pady=5)

    # Button to save the password.
    saveButton = ttk.Button(main_frame, text="Save Password", style="Save.TButton", command=save_password, state=tk.DISABLED)
    saveButton.grid(row=15, column=0, columnspan=2)
    
    # Button that clears all entry fields.
    ttk.Button(main_frame, text="Reset All", command=reset_all).grid(row=16, column=0, columnspan=2, pady=10)

    # Entry field where user enters which characters to exclude (while adjusting the generated password)
    adjustFrame = ttk.Frame(main_frame)
    ttk.Label(adjustFrame, text="Characters to exclude:").grid(row=0, column=0)
    adjustExcludeEntry = ttk.Entry(adjustFrame)
    adjustExcludeEntry.grid(row=0, column=1, pady = 10)

    # Entry field where user enters which characters to add (while adjusting the generated password)
    ttk.Label(adjustFrame, text="Characters to add:").grid(row=1, column=0)
    adjustAddEntry = ttk.Entry(adjustFrame)
    adjustAddEntry.grid(row=1, column=1, pady = 10)

    # Button to apply adjustments
    ttk.Button(adjustFrame, text="Apply Adjustments", command=apply_adjustments).grid(row=2, column=0, columnspan=2)
    adjustFrame.grid(row=17, column=0, columnspan=2)
    adjustFrame.grid_remove()

    update_age()
    root.mainloop()

if __name__ == "__main__":
    main()
