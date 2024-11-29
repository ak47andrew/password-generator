import tkinter as tk
from tkinter import filedialog
from passwgen import main
import sys
if sys.platform == 'win32':
    import msvcrt
else:
    import tty, termios


def wait_key():
    """Wait for a key press on both Windows and Linux."""
    if sys.platform == 'win32':
        msvcrt.getch()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def generate_password():
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select a file for password generation",
        filetypes=[
            ("All files", "*.*"),
        ]
    )

    if file_path:
        try:
            # Call the main function with selected file
            # Using default length of 20, no URI, and non-silent mode
            password = main(
                path=file_path,
                uri="",
                length=20,
                silent=False
            )
            
            print("\nGenerated password:", password)
            print("\nPress any key to exit...")
            wait_key()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("\nPress any key to exit...")
            wait_key()
    else:
        print("No file selected. Exiting...")
        print("\nPress any key to exit...")
        wait_key()

if __name__ == "__main__":
    generate_password()
