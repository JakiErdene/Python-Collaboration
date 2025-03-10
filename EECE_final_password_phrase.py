import random
import string

def generate_password(word: str, length: int = 12) -> str:
    if length < len(word) + 4:  # Ensure enough room for randomness
        raise ValueError("Password length must be at least 4 characters longer than the input word.")
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    
    # Generate random characters
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits + special_chars, k=length - len(word)))
    
    # Insert the word at a random position
    insert_pos = random.randint(0, len(random_chars))
    password = random_chars[:insert_pos] + word + random_chars[insert_pos:]
    
    return password

# Example usage
if __name__ == "__main__":
    user_word = input("Enter a word to include in your password: ")
    pass_length = int(input("Enter desired password length: "))
    
    try:
        password = generate_password(user_word, pass_length)
        print("Generated Password:", password)
    except ValueError as e:
        print("Error:", e)
