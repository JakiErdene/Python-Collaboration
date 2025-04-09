import random
import string
import tkinter as tk

# Global variables to store the history of generated passwords and the current password, as well as
# password reccomendations.
password_history = []
password_reccomend = []
current_password = ""

class GeneratedPassword:
    
    def __init__(self, length, word, character):
        self.length = length
        self.word = word
        self.character = character

    def checkValidity(self):
        # If the entered length is not an integer, clear entries and display message stating that it must
        # be such.
        if self.length.isdigit():
            self.length = int(self.length)
        else:
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            displayedMessage.config(text="Length must be an integer")
            return False
        
        # If the combined length of the phrase and character exceeds the desired length,
        # clear the entries and show an error.
        if len(self.word) + len(self.character) > self.length:
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            displayedMessage.config(text="Invalid specifications")
            return False
        
            # If the specified length is more than 25 (25 character limit), clear entries and show a
            # message stating that the length exceeds the limit.
        elif self.length > 25:
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            displayedMessage.config(text="Max length for password is 25")
            return False
        
        # If the user entered multiple characters when specifying a singular character to be in the generator,
        # clear entries and show a message stating that the character must have a length of 1.
        elif len(self.character) > 1:
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            displayedMessage.config(text="Character can only have a length of 1")
            return False
        
        else:    
            return True

    def createPassword(self):
        # Initialize password to be an empty string.
        passw = ""
        
        # Build the password until reaching the desired length.
        for i in range(self.length):
        
            # Try to insert the phrase if there's enough space and it hasn't been added. 50/50 chance it will be added.
            if (self.length - len(passw)) > len(self.word) and self.word not in passw:
                # Choice variable represents whether or not the program chooses to insert the specified element.
                choice = random.choice([True, False])
                if choice:
                    passw += self.word
                    
            # If there is just enough space for the word left in the generated password, add it in, or the
            # specified word and the character (and neither have been added), concatenate the word and then the character,
            # or concactenate the character and the word.
            if ((self.length - len(passw)) == len(self.word) and self.word not in passw) or ((self.length) - i == len(self.word) + 1 and self.word not in passw and self.character not in passw):
                choice = random.choice([True, False])
                if choice:
                    # The program can either choose to concactenate the word to the character first.
                    passw += self.word + self.character
                else:
                    # Or the other way around, concatenate character first and then word.
                    passw += self.character + self.word
            
            # Try to insert the specified character with a 50/50 chance if there's space.
            if ((self.length - len(passw)) > 1 and self.character not in passw):
                choice = random.choice([True, False])
                if choice:
                    passw += self.character
                    
            # If there is just enough space for the character left in the generated password, add it in, or
            #specified word and the character (and neither have been added), add the character in.
            if ((self.length - len(passw)) == 1 and self.character not in passw)  or (((self.length) - i) == len(self.word) + 1 and self.character not in passw and self.word not in passw):
                passw += self.character
                
            # Fill remaining space with a random character from the full pool.
            if len(passw) < self.length:
                passw += random.choice(string.ascii_letters + string.digits + string.punctuation)
                
            # If the password accidentally exceeds the length, trim it.
            if len(passw) > self.length:
                passw = passw[:self.length]
                
        # Prints password out to the console for debugging purposes.  
        # First password generated is the one that is shown to the user, second password generated
        # is the one that is reccomended to the user based on previous specifications.
        print(passw)
        
        return passw

def validateGenerate(obtainedLen, obtainedWord, obtainedCharacter):
    global current_password
    password = GeneratedPassword(obtainedLen, obtainedWord, obtainedCharacter)
    if password.checkValidity():
        global current_password
        # Create two instances of randomly generated password (based on user input)
        passGen = password.createPassword()
        passRec = password.createPassword()
        
        current_password = passGen
        
        # Show the password, add it to a list of passwords that have previously been generated.
        displayedMessage.config(text=passGen)
        password_history.append(passGen)
        
        # Add the other password generated (but now shown) to a list of passwords that follow the same specifications
        # the user has provided at one instance of generation, so that it can serve as a reccomneded password based on
        # what the user has previously specified for the password.
        password_reccomend.append(passRec)
        
        # Enable the adjust button now that a password has been generated.
        adjustButton.config(state=tk.NORMAL)
        
        # List previously the last 5 generated passwords, and reccomended passwords based on the 5 previous specifications.
        previous.config(text=", ".join(password_history[-5:]))
        reccomend.config(text=", ".join(password_reccomend[-5:]))
        
        # Check the strength of the password.
        checkStrength(passGen)
    
def checkStrength(pw):
        # Checks each character in the password to see if there is at least 1 special character.
        # hasChar, which keeps track if there is a special character in password, is initialized to false.
        hasChar = False
        for i in pw:
            if i in string.punctuation:
                hasChar=True
                break
        # Displays message as to whether or not password is weak based on amount of characters and whether there
        # are special characters.
        if len(pw)<10 and hasChar:
            strengthSuggestion.config(text="Weak Password, too short (less than 10 characters).")
            # Print statement for debugging purposes.
            print("checkStrength: Weak Password, too short (less than 10 characters).")
        elif hasChar==False and len(pw)>=10:
            strengthSuggestion.config(text="Weak Password, no special characters.")
            # Print statement for debugging purposes
            print("checkStrength: Weak Password, no special characters.")
        elif len(pw)<10 and hasChar==False:
            strengthSuggestion.config(text="Weak Password, too short (less than 10 characters), and no special characters.")
            # Print statement for debugging purposes.
            print("checkStrength: Weak Password, too short (less than 10 characters), and no special characters.")
        else:
            strengthSuggestion.config(text="Strong Password.")
            # Print statement for debugging purposes.
            print("checkStrength: Password is strong, has special character and has length of more than 10.")

def showAdjustmentFields():
    # Pack the adjustment frame (if not already visible).
    adjustFrame.pack(pady=10)

def applyAdjustments():
    global current_password
    exclude_chars = adjustExcludeEntry.get()
    add_chars = adjustAddEntry.get()
    # Remove any occurrences of the excluded characters from the current password.
    adjusted_password = ''.join(ch for ch in current_password if ch not in exclude_chars)
    if len(current_password) <= 25:
        # Print Statement for debugging purposes:
        print("Password after modification:", current_password)
        # Append the additional characters.
        adjusted_password += add_chars
    current_password = adjusted_password
    displayedMessage.config(text=current_password)
    checkStrength(current_password)
    
    

def resetAll():
    global current_password
    # Clear all input fields.
    givenLen.delete(0, tk.END)
    givenPhrase.delete(0, tk.END)
    givenChar.delete(0, tk.END)
    print("All input fields have been cleared")
    # Clear the displayed password.
    displayedMessage.config(text="")
    print("No displayed password")
    # Clear adjustment fields.
    adjustExcludeEntry.delete(0, tk.END)
    adjustAddEntry.delete(0, tk.END)
    print("Blank adjustment fields.")
    # Reset current password and disable adjust button.
    current_password = ""
    adjustButton.config(state=tk.DISABLED)
    print("Current password:", current_password)
    print("Adjust button disabled.")
    # Hide the adjustment frame if visible.
    adjustFrame.pack_forget()
    # Print statement for debugging purposes.
    
    

def main():
    global givenLen, givenPhrase, givenChar, root, displayedMessage, adjustButton, previous
    global adjustFrame, adjustExcludeEntry, adjustAddEntry, strengthSuggestion, reccomend, password
    
    root = tk.Tk()
    root.geometry("900x900")
    root.title("Password Generator")
    root.configure(bg="sky blue")
    
    name = tk.Label(root, text="Password Generator", font=("Times New Roman", 20))
    name.pack(pady=20)
    
    tk.Label(root, text="Enter length").pack(pady=5)
    givenLen = tk.Entry(root)
    givenLen.pack()
    
    tk.Label(root, text="Enter phrase:").pack(pady=5)
    givenPhrase = tk.Entry(root)
    givenPhrase.pack()
    
    tk.Label(root, text="Enter character:").pack(pady=5)
    givenChar = tk.Entry(root)
    givenChar.pack()
    
    displayedMessage = tk.Label(root, text="", font=("Times New Roman", 20))
    displayedMessage.pack(pady=20)
    
    # Displays message based on strength of the password.
    strengthSuggestion = tk.Label(root, text="")
    strengthSuggestion.pack(pady=5)
    
    generateButton = tk.Button(root, text="Generate", 
                               command=lambda: validateGenerate(givenLen.get(), givenPhrase.get(), givenChar.get()))
    generateButton.pack(pady=10)
    
    tk.Label(root, text="Previous passwords:").pack(pady=5)
    # Displays the five prevoius passwords that the user has generated.
    previous = tk.Label(root, text = "")
    previous.pack()
    
    tk.Label(root, text="Password reccomendations based on previous specifications:").pack(pady=5)
    # Displays the ten reccomendations for passwords based on the previous five specifications the user has provided.
    reccomend = tk.Label(root, text = "")
    reccomend.pack()
    
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
