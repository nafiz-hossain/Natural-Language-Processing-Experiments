import pyautogui as pya
import pyperclip
import openai
import datetime
import time

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = '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'

def is_valid_api_key(api_key):
    """
    Checks if the provided API key is valid.
    """
    try:
        openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt="Test", max_tokens=5, api_key=api_key)
        return True
    except openai.error.AuthenticationError as e:
        print(f"Authentication error when checking API key validity: {e}")
        return False

def copy_clipboard():
    """
    Copies the current content of the clipboard and returns it.
    """
    pya.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Add a brief pause for stability
    return pyperclip.paste()

def paste_text(text):
    """
    Simulates pasting the given text using keyboard shortcut.
    """
    pyperclip.copy(text)  # Copy the text to clipboard
    pya.hotkey('ctrl', 'v')  # Simulate paste action

def rephrase_sentence(sentence):
    """
    Rephrases the given sentence using the GPT-3 model.
    """
    try:
        # Set the parameters for the GPT-3 API call
        prompt = f"Rephrase the following sentence:\n\"{sentence}\""

        # Make the API call
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.7,
            max_tokens=100
        )

        # Extract the rephrased sentence from the API response
        rephrased_sentence = response.choices[0].text.strip()

        return rephrased_sentence
    except Exception as e:
        with open("rephrase_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp}: An error occurred during rephrasing: {e}\n")
        return None

# Check if the API key is valid
if not is_valid_api_key(openai.api_key):
    with open("rephrase_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp}: Invalid API key\n")
    print("Invalid API key.")
    exit()

# Hardcoded input sentence for testing purposes
input_sentence = copy_clipboard()

print(f"Input Sentence: {input_sentence}")  # Print input for debugging purposes

# Call the rephrase_sentence function
rephrased_result = rephrase_sentence(input_sentence)

if rephrased_result:
    # Display the results
    print(f"\nOriginal Sentence: {input_sentence}")
    print(f"Rephrased Sentence: {rephrased_result}")

    # Paste the rephrased sentence into the current window
    paste_text(rephrased_result)

    # Notify the user that the rephrased sentence has been pasted
    print("Rephrased sentence has been pasted into the current window.")

    # Write input and output sentences in a single line in the log file
    with open("rephrase_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp}: Input: {input_sentence} - Output: {rephrased_result}\n")
else:
    with open("rephrase_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp}: Failed to rephrase the sentence.\n")
    print("Failed to rephrase the sentence.")
