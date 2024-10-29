import customtkinter as ctk
import yfinance as yf
import threading
import time
from tkinter import Menu, messagebox, font

# Function to fetch the current and previous day's Nifty 50 index value
# Function to fetch the current and previous day's Nifty 50 index value
def get_nifty50():
    nifty = yf.Ticker("^NSEI")
    nifty_data = nifty.history(period="5d")  # Get last 5 days' data to ensure we have at least two days' worth
    if len(nifty_data) < 2:
        raise ValueError("Insufficient data to calculate change")
    
    previous_close = nifty_data['Close'].iloc[-2]
    current_price = nifty_data['Close'].iloc[-1]
    return current_price, previous_close


# Function to update and scroll the label with the current Nifty 50 value
def update_nifty_value(label):
    while True:
        try:
            current_price, previous_close = get_nifty50()
            price_change = current_price - previous_close
            percentage_change = (price_change / previous_close) * 100

            color = "#46f263" if price_change >= 0 else "#ff5c5c"  # Green for positive, Red for negative
            sign = "+" if price_change >= 0 else "-"
            nifty_text = f" Nifty:{current_price:.2f}({sign}{abs(percentage_change):.2f}%)    "

            print(f"Fetched Nifty 50 Value:{current_price:.2f},Change:{price_change:.2f}({percentage_change:.2f}%)")  # Debug print

            # Scroll the text
            for i in range(len(nifty_text)):
                display_text = nifty_text[i:]+nifty_text[:i]  # Rotate the text
                label.configure(text=display_text, text_color=color)
                time.sleep(0.1)  # Adjust the speed of the scroll
        except Exception as e:
            print(f"Error: {e}")  # Print the error for debugging
            label.configure(text="Error fetching data", text_color="white")
        time.sleep(120)  # Update every 120 seconds

# Enable dragging for the window
def start_move(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def on_move(event):
    x = event.x_root - x_offset
    y = event.y_root - y_offset
    root.geometry(f'+{x}+{y}')

# Function to show confirmation dialog and close the app
def confirm_close():
    response = messagebox.askokcancel("Confirmation", "Do you really want to close the app?")
    if response:
        root.quit()

# Function to create the right-click menu
def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

# Create the main window with customtkinter
def create_gui():
    global root, context_menu
    ctk.set_appearance_mode("dark")  # Options: "dark", "light"
    ctk.set_default_color_theme("blue")  # Available themes: "blue", "green", "dark-blue"
    
    root = ctk.CTk()  # Initialize the main window
    root.overrideredirect(True)  # Remove title bar (frameless window)

    # Calculate height of the text based on font size
    text_font = ("Terminal", 22, "bold")
    font_height = font.Font(family="Terminal", size=22, weight="bold").metrics("linespace")
    window_height = font_height + 2  # Set window height to text height + 2 pixels
    root.geometry(f"260x{window_height}")  # Set the window size to fit the text
    root.attributes("-topmost", True)  # Keep the window always on top
    root.configure(bg="black")  # Set background color to ensure visibility

    # Bind mouse events for window dragging
    root.bind('<Button-1>', start_move)
    root.bind('<B1-Motion>', on_move)

    # Create a label to display the Nifty 50 value with larger, bold font
    nifty_label = ctk.CTkLabel(root, text="Fetching...", font=text_font, text_color="white", bg_color="black")
    nifty_label.pack(side="top", fill="both", expand=True, pady=0, padx=0)

    # Run the data fetch and scroll in a separate thread to avoid freezing the UI
    thread = threading.Thread(target=update_nifty_value, args=(nifty_label,))
    thread.daemon = True  # Close the thread when the app closes
    thread.start()

    # Create right-click context menu
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Close", command=confirm_close)

    # Bind right-click to show context menu
    root.bind("<Button-3>", show_context_menu)

    # Start the GUI main loop
    root.mainloop()

# Run the app
if __name__ == "__main__":
    create_gui()
