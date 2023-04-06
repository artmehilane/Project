import tkinter as tk
from PIL import ImageTk, Image

# Create the main window
root = tk.Tk()
root.title("Hello World")

# Create a label with the "Hello!" text
hello_label = tk.Label(root, text="Hello!")
hello_label.pack()

# Load the logo image file
logo_image = Image.open("photos/logo.png")
logo_image = logo_image.resize((200, 200))
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a canvas to hold the logo
logo_canvas = tk.Canvas(root, width=800, height=400)
logo_canvas.pack()
logo_canvas.create_image(100, 100, image=logo_photo)

# Create a button with the "to menu" text
menu_button = tk.Button(root, text="to menu")
menu_button.pack()

# Start the main event loop
root.mainloop()