import random
import string
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta

password_history = []
password_reccomend = []
current_password = ""
password_created_time = None
password_expiry_minutes = 1  # Expiry time in minutes

class GeneratedPassword:
    def __init__(self, length, phrases, characters, exclude):
        self.length = length
        self.phrases = [p.strip() for p in phrases.split(",") if p.strip()] if use_phrases.get() else []
        self.characters = [c.strip() for c in characters.split(",") if c.strip()] if use_characters.get() else []
        self.exclude = set(exclude) if use_exclude.get() else set()

    def checkValidity(self):
        if self.length.isdigit():
            self.length = int(self.length)
        else:
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            excludeChars.delete(0, tk.END)
            displayedMessage.config(text="Invalid length")
            return False

        total_phrase_len = sum(len(p) for p in self.phrases)
        total_char_len = sum(len(c) for c in self.characters)
        if total_phrase_len + total_char_len > self.length:
            displayedMessage.config(text="Combined phrase/character length too long")
            return False

        if self.length > 25:
            displayedMessage.config(text="Max length for password is 25")
            return False

        for char in self.characters:
            if len(char) != 1:
                displayedMessage.config(text="Each character must be a single character")
                return False

        return True

    def createPassword(self):
        passw = ""
        used_phrases = set()
        used_chars = set()
        pool = ''.join(c for c in string.ascii_letters + string.digits + string.punctuation if c not in self.exclude)

        while len(passw) < self.length:
            choice = random.choice(["phrase", "char", "random"])
            if choice == "phrase" and self.phrases:
                unused = [p for p in self.phrases if p not in used_phrases]
                if unused:
                    phrase = random.choice(unused)
                    if len(passw) + len(phrase) <= self.length:
                        passw += phrase
                        used_phrases.add(phrase)
            elif choice == "char" and self.characters:
                unused = [c for c in self.characters if c not in used_chars and c not in self.exclude]
                if unused:
                    ch = random.choice(unused)
                    if len(passw) + 1 <= self.length:
                        passw += ch
                        used_chars.add(ch)
            elif choice == "random" and pool:
                passw += random.choice(pool)

            if len(passw) > self.length:
                passw = passw[:self.length]

        return passw

def validateGenerate(length, phrases, characters):
    global current_password, password_created_time
    exclude = excludeChars.get()
    password = GeneratedPassword(length, phrases, characters, exclude)
    if password.checkValidity():
        passGen = password.createPassword()
        passRec = password.createPassword()
        current_password = passGen
        password_created_time = datetime.now()
        displayedMessage.config(text=passGen)
        password_history.append(passGen)
        password_reccomend.append(passRec)
        adjustButton.config(state=tk.NORMAL)
        saveButton.config(state=tk.NORMAL)
        previous.config(text=", ".join(password_history[-5:]))
        reccomend.config(text=", ".join(password_reccomend[-5:]))
        checkStrength(passGen)

def checkStrength(pw):
    hasChar = any(c in string.punctuation for c in pw)
    if len(pw) < 10 and hasChar:
        strengthSuggestion.config(text="Weak Password, too short (less than 10 characters).")
    elif not hasChar and len(pw) >= 10:
        strengthSuggestion.config(text="Weak Password, no special characters.")
    elif len(pw) < 10 and not hasChar:
        strengthSuggestion.config(text="Weak Password, too short and no special characters.")
    else:
        strengthSuggestion.config(text="Strong Password.")

def showAdjustmentFields():
    adjustFrame.pack(pady=10)

def applyAdjustments():
    global current_password
    exclude_chars = adjustExcludeEntry.get()
    add_chars = adjustAddEntry.get()
    adjusted_password = ''.join(ch for ch in current_password if ch not in exclude_chars)
    if len(current_password) <= 25:
        adjusted_password += add_chars
    current_password = adjusted_password[:25]
    displayedMessage.config(text=current_password)
    checkStrength(current_password)

def resetAll():
    global current_password, password_created_time
    givenLen.delete(0, tk.END)
    givenPhrase.delete(0, tk.END)
    givenChar.delete(0, tk.END)
    excludeChars.delete(0, tk.END)
    displayedMessage.config(text="")
    adjustExcludeEntry.delete(0, tk.END)
    adjustAddEntry.delete(0, tk.END)
    current_password = ""
    password_created_time = None
    adjustButton.config(state=tk.DISABLED)
    saveButton.config(state=tk.DISABLED)
    ageLabel.config(text="")
    adjustFrame.pack_forget()
    use_phrases.set(True)
    use_characters.set(True)
    use_exclude.set(True)

def savePasswordToFile():
    if current_password:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")],
                                                title="Save Password As")
        if filepath:
            with open(filepath, "w") as file:
                file.write(current_password)

def updatePasswordAge():
    if password_created_time:
        now = datetime.now()
        age = now - password_created_time
        minutes, seconds = divmod(age.total_seconds(), 60)
        if age > timedelta(minutes=password_expiry_minutes):
            ageLabel.config(text="Password expired — generate a new one!", fg="red")
            saveButton.config(state=tk.DISABLED)
        else:
            ageLabel.config(text=f"Password age: {int(minutes)}m {int(seconds)}s", fg="green")
            saveButton.config(state=tk.NORMAL)
    root.after(1000, updatePasswordAge)

def main():
    global givenLen, givenPhrase, givenChar, root, displayedMessage, adjustButton, previous
    global adjustFrame, adjustExcludeEntry, adjustAddEntry, strengthSuggestion, reccomend, password, saveButton, ageLabel, excludeChars
    global use_phrases, use_characters, use_exclude

    root = tk.Tk()
    root.geometry("1000x1500")
    root.title("Password Generator")
    root.configure(bg="sky blue")

    use_phrases = tk.BooleanVar(value=True)
    use_characters = tk.BooleanVar(value=True)
    use_exclude = tk.BooleanVar(value=True)

    tk.Label(root, text="Password Generator", font=("Times New Roman", 20)).pack(pady=20)
    tk.Label(root, text="Enter total length").pack(pady=5)
    givenLen = tk.Entry(root)
    givenLen.pack()

    tk.Checkbutton(root, text="Include specific phrases", variable=use_phrases, bg="sky blue").pack()
    tk.Label(root, text="Enter phrases (comma-separated):").pack(pady=5)
    givenPhrase = tk.Entry(root)
    givenPhrase.pack()

    tk.Checkbutton(root, text="Include specific characters", variable=use_characters, bg="sky blue").pack()
    tk.Label(root, text="Enter characters (comma-separated):").pack(pady=5)
    givenChar = tk.Entry(root)
    givenChar.pack()

    tk.Checkbutton(root, text="Exclude specific characters", variable=use_exclude, bg="sky blue").pack()
    tk.Label(root, text="Exclude characters (comma-separated):").pack(pady=5)
    excludeChars = tk.Entry(root)
    excludeChars.pack()

    displayedMessage = tk.Label(root, text="", font=("Times New Roman", 20))
    displayedMessage.pack(pady=20)

    ageLabel = tk.Label(root, text="", font=("Arial", 12))
    ageLabel.pack(pady=5)

    strengthSuggestion = tk.Label(root, text="")
    strengthSuggestion.pack(pady=5)

    tk.Button(root, text="Generate", 
              command=lambda: validateGenerate(givenLen.get(), givenPhrase.get(), givenChar.get())).pack(pady=10)

    tk.Label(root, text="Previous passwords:").pack(pady=5)
    previous = tk.Label(root, text = "")
    previous.pack()

    tk.Label(root, text="Password reccomendations based on previous specifications:").pack(pady=5)
    reccomend = tk.Label(root, text = "")
    reccomend.pack()

    adjustButton = tk.Button(root, text="Adjust Password", command=showAdjustmentFields, state=tk.DISABLED)
    adjustButton.pack(pady=10)

    saveButton = tk.Button(root, text="Download Password", command=savePasswordToFile, state=tk.DISABLED)
    saveButton.pack(pady=10)

    tk.Button(root, text="Reset", command=resetAll).pack(pady=10)

    adjustFrame = tk.Frame(root, bg="sky blue")
    tk.Label(adjustFrame, text="Characters to exclude:").pack(side="left", padx=5)
    adjustExcludeEntry = tk.Entry(adjustFrame)
    adjustExcludeEntry.pack(side="left", padx=5)

    tk.Label(adjustFrame, text="Characters to add:").pack(side="left", padx=5)
    adjustAddEntry = tk.Entry(adjustFrame)
    adjustAddEntry.pack(side="left", padx=5)

    tk.Button(adjustFrame, text="Apply Adjustments", command=applyAdjustments).pack(pady=10)

    updatePasswordAge()
    root.mainloop()

if __name__ == "__main__":
    main()