
import speech_recognition as sr
import subprocess

def main():
    """Runs the voice commander in a loop."""
    r = sr.Recognizer()
    # Adjust for ambient noise once at the start
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source)
        print("Ready to listen.")

    while True:
        with sr.Microphone() as source:
            print("\nSay something!")
            try:
                # listen for the first phrase and extract it into audio data
                audio = r.listen(source)
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                continue

        try:
            # Recognize speech using Google Web Speech API
            text = r.recognize_google(audio)
            print(f"You said: {text}")

            # Check for exit command
            if text.lower().strip() in ['exit', 'quit', 'stop']:
                print("Exiting voice commander.")
                break

            # Copy the text to the clipboard using copyq
            subprocess.run(['copyq', 'add', text], check=True)
            print("Text copied to clipboard.")

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        except FileNotFoundError:
            print("Error: 'copyq' command not found. Please make sure it's installed and in your PATH.")
            # If copyq is essential, we should probably exit.
            break
        except subprocess.CalledProcessError:
            print("Error: Failed to copy text to clipboard using 'copyq'.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
