import random
import string
import tkinter as tk

class GeneratedPassword:
    
    # Intialize the specified word, character, and length of password.
    def __init__(self, length, word, character):
        
        self.length = length
        self.word = word
        self.character = character

    # Function checks the validity of a password
    def checkValidity(self):
        
        # If the specified password's total length is less than the total sum of the length of the character plus the word,
        # The password is invalid.
        if len(self.word) + len(self.character) > int(self.length):
            
            # Clear the entry boxes.
            givenLen.delete(0, tk.END)
            givenPhrase.delete(0, tk.END)
            givenChar.delete(0, tk.END)
            
            # Returns the message that the specifications are invalid, instead of a password.
            displayedMessage.config(text = "Invalid specifications")
            
            # Return false, which represents that function is invalid.
            return False
        
        else:
            
            # Return true, which represents that the function is valid (will do so if the specifications make sense and do not conflict with each other)
            return True

    # Method to create the password.
    def createPassword(self):
        
        # Password is initialized as an empty string.
        passw = ""
        
        # Using a for loop, add the specified character and word, as well as random characters.
        for i in range(int(self.length)):
            
            # If the remaining length of the password is greater than the length of the word,
            # and if the word is not yet in the password, there is a 50/50 chance that it will be added to the password
            # note that the 50% chance comes from the program randomly choosing between true and false for the value of insertWord.
            if (int(self.length) - i) > len(self.word) and self.word not in passw:
               
                # if insertWord is true, then the word will be added to the password.
                insertWord = random.choice([True, False])
                if insertWord:
                    passw = passw + self.word
           
            # If there is just enough space to add the word to the password, or if there is just enough space to add the word and the specified
            # character to the password (provided that neither the specified word or character has been added to the password yet), add the word.
            if ((int(self.length) - i) == len(self.word) and self.word not in passw) or ((int(self.length) - i) == len(self.word) + 1 and self.word not in passw and self.character not in passw):
                passw = passw + self.word
            
            # If there is more than one space of remaining space in the password and the specified character is not in the password,
            # there is a 50% chance that it will be added to the password.
            if (int(self.length) - i) > 1 and self.character not in passw:
                
                # Determine if character is added to password using same methodology as randomly deciding whether to add specified word.
                insertCharacter = random.choice([True, False])
                if insertCharacter:
                    passw = passw + self.character
                    
            # If there is just enough th add the character to the password, or if there is just enough space to add the word and the specified character to the password
            # (provided that neither the specified word or character has been added to the password yet), add the character.
            if ((int(self.length) - i) == 1 and self.character not in passw) or ((int(self.length) - i) == len(self.word) + 1 and self.character not in passw and self.word not in passw):
                passw = passw + self.character
                
            # If there is still space in the password, add a random character to the password (which can include any character that can be typed on a keyboard except for whitespace).
            if len(passw) < int(self.length):
                
                passw = passw + random.choice(string.ascii_letters + string.digits + string.punctuation)
            
        # Return the value of the password.
        return passw
      \
# This function validates and generates the password.
def validateGenerate(obtainedLen, obtainedWord, obtainedCharacter):
     
    # Create an instance of the class using values passed to the function (values of length, the specific word and the specific character)
    password = GeneratedPassword(obtainedLen, obtainedWord, obtainedCharacter)
    
    # If the password is valid (based on the boolean value returned from the function)
    if password.checkValidity():  
         
        # Execute the method to create the password, and display the password onto the GUI.
        passGen = password.createPassword()
        displayedMessage.config(text = passGen)
        
    else:
        
        # Otherwise, display a message stating that the specifications are invalid.
        displayedMessage.config(text = "Invalid specifications")

            
            
#==============================================================================
def main():

    global givenLen, givenPhrase, givenChar, root, displayedMessage
    
    root = tk.Tk()

    root.geometry("800x800")

    root.title("Password Generator")
    
    root.configure(bg = "sky blue")

    # Creates title to be displayed at the top of the window when the app is being run.
    name = tk.Label(root, text = "Password Generator", font = ("Times New Roman", 20))
    name.pack(pady = 20)
    
    # Create a label and textbox below it that prompts, and allows for user to enter length of password.
    tk.Label(root, text = "Enter length").pack(pady = 20)
    givenLen = tk.Entry(root)
    givenLen.pack()
        
    # Create a label and textbox below it that prompts, and allows for user to enter desired specific character to be included in password.
    tk.Label(root, text = "Enter phrase: ").pack(pady = 20)
    givenPhrase = tk.Entry(root)
    givenPhrase.pack()
        
    # Create a label and textbox below it that prompts, and allows for user to enter desired specific character to be inluded in password.
    tk.Label(root, text = "Enter character").pack(pady = 20)
    givenChar = tk.Entry(root)
    givenChar.pack()
        
    # Initialize the font and text of the displayed message.
    displayedMessage = tk.Label(root, text = "", font = ("Times New Roman", 20))
    displayedMessage.pack()

    # Initialize a button that has the text "Generate" on it, which allows the user to validate and generate a password based on the specified conditions.
    button = tk.Button(root, text="Generate", command = lambda: validateGenerate(givenLen.get(), givenPhrase.get(), givenChar.get()))
    button.pack()


    root.mainloop()

#==============================================================================
# Invoke the main function
if __name__ == "__main__":
    main()
#==============================================================================