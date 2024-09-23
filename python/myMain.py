import pygame
import pygame.gfxdraw
import myPieces
import myLogic
import subprocess
import os
import tkinter as tk
from tkinter import messagebox

nums = []

def submit():
    try:
        nums.append(int(entry1.get()))
        nums.append(int(entry2.get()))
        nums.append(int(entry3.get()))
        root.destroy()
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie nur ganze Zahlen ein.")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Zahleneingabe")

# Eingabefelder erstellen
tk.Label(root, text="Zahl 1:").grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Zahl 2:").grid(row=1, column=0, padx=5, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Zahl 3:").grid(row=2, column=0, padx=5, pady=5)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1, padx=5, pady=5)

# Absenden-Button erstellen
submit_button = tk.Button(root, text="Absenden", command=submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# Hauptschleife starten
root.mainloop()

current_dir = os.path.dirname(os.path.abspath(__file__))
puzzle_path = os.path.join(current_dir, "puzzle")
process = subprocess.Popen([puzzle_path, str(nums[0]), str(nums[1]), str(nums[2])]
                           , stdout=subprocess.PIPE
                           , stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

loesung = []
for line in stdout.decode("utf-8").split('\n')[:-1]:
    l = line.strip('[]')
    int_array = list(int(num) for num in l.split(','))
    loesung.append(int_array)

# Initialize Pygame
pygame.init()

# Set up the window dimensions
width = 900
height = 900

# Create the window
window = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption("Puzzle Solver")

# Game loop
running = True

while running:
    window.fill((0,0,0))

    # Spielfeld - Rahmen
    myPieces.spielfeldrahmen(window)
    for i, l in enumerate(loesung):          
        farbe = (i * 15 + 45, i * 10 + 65, i * 5 + 100) 
        for j in loesung[i]:
            myPieces.positioniereElement(window, myLogic.koordinatenInReihen[j], farbe)

    # Refresh Ausgabe    
    pygame.display.flip()

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
