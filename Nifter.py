import customtkinter as ctk
import yfinance as yf
import threading
import time

# Function to fetch the Nifty 50 index value
def get_nifty50():
    nifty = yf.Ticker("^NSEI")
    nifty_data = nifty.history(period="1d")
    return nifty_data['Close'].iloc[-1]

# Function to update the label with the current Nifty 50 value
def update_nifty_value(label):
    while True:
        try:
            nifty_value = get_nifty50()
            print(f"Fetched Nifty 50 Value: {nifty_value:.2f}")  # Debug print
            label.configure(text=f"Nifty 50: {nifty_value:.2f}")
        except Exception as e:
            print(f"Error: {e}")  # Print the error for debugging
            label.configure(text="Error fetching data")
        time.sleep(60)  # Update every 60 seconds

# Enable dragging for the window
def start_move(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def on_move(event):
    x = event.x_root - x_offset
    y = event.y_root - y_offset
    root.geometry(f'+{x}+{y}')

# Create the main window with customtkinter
def create_gui():
    global root
    ctk.set_appearance_mode("dark")  # Options: "dark", "light"
    ctk.set_default_color_theme("blue")  # Available themes: "blue", "green", "dark-blue"
    
    root = ctk.CTk()  # Initialize the main window
    root.overrideredirect(True)  # Remove title bar (frameless window)
    root.geometry("220x50")  # Adjust the window size
    root.attributes("-topmost", True)  # Keep the window always on top
    root.configure(bg="black")  # Set background color to ensure visibility

    # Bind mouse events for window dragging
    root.bind('<Button-1>', start_move)
    root.bind('<B1-Motion>', on_move)

    # Create a label to display the Nifty 50 value with larger, bold font and green color
    nifty_label = ctk.CTkLabel(root, text="Fetching...", font=("Calibry", 24, "bold"), text_color="#46f263", bg_color="black")  # Green font
    nifty_label.pack(pady=10)

    # Run the data fetch in a separate thread to avoid freezing the UI
    thread = threading.Thread(target=update_nifty_value, args=(nifty_label,))
    thread.daemon = True  # Close the thread when the app closes
    thread.start()

    # Start the GUI main loop
    root.mainloop()

# Run the app
if __name__ == "__main__":
    create_gui()
