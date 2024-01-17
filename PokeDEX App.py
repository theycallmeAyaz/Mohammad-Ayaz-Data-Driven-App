import tkinter as tk
from tkinter import messagebox
import os

def HEIGHT() -> int:
    return 600
def WIDTH() -> int:
    return 800

#Open the Pokedex application and close the current window
def open_pokedex():
    messagebox.showinfo("Instructions", "To Search for a Pokémon,\n Enter the Pokémon's Name or Dex Number!\n Format:'Pokemon'-Mega (if Necessary)")
    root.destroy()
    os.system('pokedex-main.py')

root = tk.Tk()
# Prevent window from being resized
root.resizable(False, False)
# Application title and icon
root.title("Start Window")
root.iconbitmap('pkdex_icon.ico')
# Application dimensions
canvas = tk.Canvas(root, height=HEIGHT(), width=WIDTH())
canvas.pack()

# Application background
background_image = tk.PhotoImage(file='logo.png')  
# Substitute with your image file(is a png so added the blue bg as background)
background_label = tk.Label(root, image=background_image,background='#D7F7FF')
background_label.place(relheight=1, relwidth=1)

# Open Pokedex button
open_button = tk.Button(root, text="Open Pokedex", command=open_pokedex)
open_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

root.mainloop()
