import random
import string
import tkinter as tk

# Global variables to store the history of generated passwords and the current password.
password_history = []
current_password = ""

class GeneratedPassword:
    
    def __init__(self, length, word, character):
        self.length = int(length)
        self.word = word
        self.character = character

    def checkValidity(self):
        # If the combined length of the phrase and character exceeds the desired length,
        # clear the entries and show an error.
        if len(self.word) + len(self.character) > self.length:
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            displayedMessage.config(text="Invalid specifications")
            return False
        return True

    def createPassword(self):
        passw = ""
        # Build the password until reaching the desired length.
        for i in range(self.length):
            # Try to insert the phrase if there's enough space and it hasn't been added.
            if (self.length - len(passw)) > len(self.word) and self.word not in passw:
                if random.choice([True, False]):
                    passw += self.word
            if (self.length - len(passw)) == len(self.word) and self.word not in passw:
                passw += self.word
            # Try to insert the specified character with a 50/50 chance if there's space.
            if (self.length - len(passw)) > 1 and self.character not in passw:
                if random.choice([True, False]):
                    passw += self.character
            if (self.length - len(passw)) == 1 and self.character not in passw:
                passw += self.character
            # Fill remaining space with a random character from the full pool.
            if len(passw) < self.length:
                passw += random.choice(string.ascii_letters + string.digits + string.punctuation)
            # If the password accidentally exceeds the length, trim it.
            if len(passw) > self.length:
                passw = passw[:self.length]
        return passw

def validateGenerate(obtainedLen, obtainedWord, obtainedCharacter):
    global current_password
    password = GeneratedPassword(obtainedLen, obtainedWord, obtainedCharacter)
    
    if password.checkValidity():
        passGen = password.createPassword()
        current_password = passGen
        displayedMessage.config(text=passGen)
        password_history.append(passGen)
        # Enable the adjust button now that a password has been generated.
        adjustButton.config(state=tk.NORMAL)
    else:
        displayedMessage.config(text="Invalid specifications")

def showAdjustmentFields():
    # Pack the adjustment frame (if not already visible).
    adjustFrame.pack(pady=10)

def applyAdjustments():
    global current_password
    exclude_chars = adjustExcludeEntry.get()
    add_chars = adjustAddEntry.get()
    # Remove any occurrences of the excluded characters from the current password.
    adjusted_password = ''.join(ch for ch in current_password if ch not in exclude_chars)
    # Append the additional characters.
    adjusted_password += add_chars
    current_password = adjusted_password
    displayedMessage.config(text=current_password)

def resetAll():
    global current_password
    # Clear all input fields.
    givenLen.delete(0, tk.END)
    givenPhrase.delete(0, tk.END)
    givenChar.delete(0, tk.END)
    # Clear the displayed password.
    displayedMessage.config(text="")
    # Clear adjustment fields.
    adjustExcludeEntry.delete(0, tk.END)
    adjustAddEntry.delete(0, tk.END)
    # Reset current password and disable adjust button.
    current_password = ""
    adjustButton.config(state=tk.DISABLED)
    # Hide the adjustment frame if visible.
    adjustFrame.pack_forget()

def main():
    global givenLen, givenPhrase, givenChar, root, displayedMessage, adjustButton
    global adjustFrame, adjustExcludeEntry, adjustAddEntry
    
    root = tk.Tk()
    root.geometry("800x800")
    root.title("Password Generator")
    root.configure(bg="sky blue")
    
    name = tk.Label(root, text="Password Generator", font=("Times New Roman", 20))
    name.pack(pady=20)
    
    tk.Label(root, text="Enter length").pack(pady=10)
    givenLen = tk.Entry(root)
    givenLen.pack()
    
    tk.Label(root, text="Enter phrase:").pack(pady=10)
    givenPhrase = tk.Entry(root)
    givenPhrase.pack()
    
    tk.Label(root, text="Enter character").pack(pady=10)
    givenChar = tk.Entry(root)
    givenChar.pack()
    
    displayedMessage = tk.Label(root, text="", font=("Times New Roman", 20))
    displayedMessage.pack(pady=20)
    
    generateButton = tk.Button(root, text="Generate", 
                               command=lambda: validateGenerate(givenLen.get(), givenPhrase.get(), givenChar.get()))
    generateButton.pack(pady=10)
    
    # Button to adjust the generated password (disabled until a password is generated).
    adjustButton = tk.Button(root, text="Adjust Password", command=showAdjustmentFields, state=tk.DISABLED)
    adjustButton.pack(pady=10)
    
    # Reset button clears all fields.
    resetButton = tk.Button(root, text="Reset", command=resetAll)
    resetButton.pack(pady=10)
    
    # Adjustment frame added below the main window elements.
    adjustFrame = tk.Frame(root, bg="sky blue")
    tk.Label(adjustFrame, text="Characters to exclude:").pack(pady=5)
    adjustExcludeEntry = tk.Entry(adjustFrame)
    adjustExcludeEntry.pack(pady=5)
    
    tk.Label(adjustFrame, text="Characters to add:").pack(pady=5)
    adjustAddEntry = tk.Entry(adjustFrame)
    adjustAddEntry.pack(pady=5)
    
    applyButton = tk.Button(adjustFrame, text="Apply Adjustments", command=applyAdjustments)
    applyButton.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
