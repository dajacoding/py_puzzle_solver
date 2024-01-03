import pygame
import pygame.gfxdraw
import myPieces
import myBruteforce
import myLogic

# Initialize Pygame
pygame.init()

# Set up the window dimensions
width = 900
height = 900

# Create the window
window = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption("Puzzle Solver")



loesung = myBruteforce.listenPruefung(myPieces.alleSonderelementPositionen[0])
print(loesung)

# Game loop
running = True

while running:
    window.fill((0,0,0))

    # Spielfeld - Rahmen
    myPieces.spielfeldrahmen(window)

    # Testzeugs  
        

    for i in range(len(loesung) - 1):  
        farbe = None
        if type(loesung[i]) == int:
            temp = loesung[i] % 12  
            farbe = (temp * 15 + 45, temp * 10 + 65, temp * 5 + 100) 
        if type(loesung[i]) != int:
            farbe = (10, 10, 10)
        elif loesung[i] < 0:
            farbe = (200, 250, 50)
        myPieces.positioniereElement(window, myLogic.alleKoordinaten[i], farbe)



    # Sonderelement
    #myPieces.positioniereSonderelement(window, positionSonderelement, (200, 250, 50))    
    # moegliche Positionen fuer das Sonderelement
    #myPieces.erstelleSonderelementPunkt(window, myPieces.alleSonderelementPositionen)

    # Refresh Ausgabe    
    pygame.display.flip()

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
