import pygame
import pygame.gfxdraw
import math
import random

pygame.init()

# globale Variablen
kantenlaenge = 18
hoehe = math.sqrt(kantenlaenge**2 - (kantenlaenge / 2)**2)
farbeSpielfeldrahmen = (30, 30, 70)
positionSpielfeld = 450, 150

# Sammlung aller Puzzle - Elemente
allePuzzleElemente = [[0, 3, 5, 1, [1, 1]],
                      [0, 5, 6, 2, [2, 3]],
                      [0, 4, 2, 1, [1, 6]],
                      [0, 5, 6, 3, [3, 4]],
                      [0, 3, 1, 6, [6, 5]],
                      [0, 2, 3, 5, [5, 6]],
                      [0, 1, 6, 3, [3, 3]],
                      [0, 2, 1, 6, [6, 6]],
                      [0, 5, 4, 3, [3, 3]],
                      [0, 3, [3, 3], 5, [5, 6]],
                      [0, 6, [6, 6], 3, [3, 2]],
                      [0, 6, [6, 6], 4, [4, 4]]                      
                     ]

# Positionen fuer das Sonderelement
alleSonderelementPositionen = [(0),
                               (5),
                               (3, 3, 3),
                               (2, 2),
                               (2, 2, 1),
                               (2, 1, 1, 1),
                               (6, 1, 1, 1),
                               (4, 4, 4),
                               (6, 5, 5),
                               (4, 5, 5, 5)
                              ]


# Rotiere ein Element um 120 Grad im Uhrzeigersinn
def rotation(element):    
        liste = []
        for e in element:
            if type(e) == int:
                if e != 0:
                    liste.append(rotationsFaktor(e))
                else:
                    liste.append(0)
            else:
                l = []
                for ee in e:
                   l.append(rotationsFaktor(ee))
                liste.append(l)
        return liste


# Hilfsfunktion fuer rotation()
def rotationsFaktor(rf):
    temp = rf + 2
    if temp > 6:
        temp -= 6
    return temp


# lege Position fuer Sonderelement fest
def positioniereSonderelement(ausgabeoberflaeche, position, farbe):
    tripplehex(ausgabeoberflaeche, pfadZuZiel(alleSonderelementPositionen[position], spielfeldzentrum()), farbe)

def positioniereElement(ausgabeoberflaeche, position, farbe):
    tripplehex(ausgabeoberflaeche, pfadZuZiel(position, spielfeldzentrum()), farbe)


# Filtere Pfad, gib Zielkoordinaten zurück
def pfadZuZiel(element, zentrum):
    if type(element) == int:
            z = koordinatenErmittlen(element, zentrum)
    else:
        z = zentrum
        for e in element:
            z = koordinatenErmittlen(e, z)
    return z

# zeichne erlaubte Positionen fuer Sonderelement
def erstelleSonderelementPunkt(ausgabeoberflaeche, positionsMatrix):
    zentrum = spielfeldzentrum()
    for element in positionsMatrix:
        z = pfadZuZiel(element, zentrum)
        pygame.draw.circle(ausgabeoberflaeche, (200, 170, 30), z, 5)


# ermitteln des Spielfeldzentrums
def spielfeldzentrum():
    z = positionSpielfeld
    for i in range(5):
        z = koordinatenErmittlen(6, z)        
    return z


# erzeugen des Spielfeldes
def spielfeldrahmen(ausgabeoberflaeche):
    neuePosition = positionSpielfeld
    richtungNachbar = 5
    for i in range(6):
        for j in range(5):
            neuePosition = koordinatenErmittlen(richtungNachbar, neuePosition)
            tripplehex(ausgabeoberflaeche, neuePosition, farbeSpielfeldrahmen)
        richtungNachbar += 1
        if richtungNachbar > 6:
            richtungNachbar = 1


# zusammensetzen der der Puzzle Elemente aus Grundbausteinen
def zusammenbauPuzzleElement(elementStruktur, ausgabeoberflaeche, punkt):
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    for element in elementStruktur:
        if type(element) == int:
             tripplehex(ausgabeoberflaeche, koordinatenErmittlen(element, punkt), (r, g, b))
        else:
             tripplehex(ausgabeoberflaeche, koordinatenErmittlen(element[1], koordinatenErmittlen(element[0], punkt)), (r, g, b))    


# Koordinaten durch 3 - fache Koordinatenverschiebung ermitteln 
def koordinatenErmittlen(position, punkt):
    match position:
        case 0:
            return punkt
        case 1:
            return dreifachAufruf(punkt, koordinaten1)
        case 2:
            return dreifachAufruf(punkt, koordinaten2)
        case 3:
            return dreifachAufruf(punkt, koordinaten3)
        case 4:
            return dreifachAufruf(punkt, koordinaten4)
        case 5:
            return dreifachAufruf(punkt, koordinaten5)
        case _:
            return dreifachAufruf(punkt, koordinaten6)


# 3 - fachverschiebung
def dreifachAufruf(punkt, funktion):
    p = funktion(punkt)
    p = funktion(p)
    return funktion(p)


# zeichnen des Grundbausteins
def tripplehex(ausgabeoberflaeche, punkt, farbe):
    hex(ausgabeoberflaeche, koordinaten2(punkt), farbe)
    hex(ausgabeoberflaeche, koordinaten4(punkt), farbe)
    hex(ausgabeoberflaeche, koordinaten6(punkt), farbe)


# zeichnen eines Hexagons
def hex(ausgabeoberflaeche, punkt, farbe):   
    koordinaten = [koordinaten1(punkt),
                   koordinaten2(punkt), 
                   koordinaten3(punkt),
                   koordinaten4(punkt),
                   koordinaten5(punkt), 
                   koordinaten6(punkt)]
    pygame.gfxdraw.filled_polygon(ausgabeoberflaeche, koordinaten, farbe)


# Positionsermittlung in 6 verschiedene Richtungen (links - unten beginnend, im Uhrzeigersinn)
def koordinaten1(punkt):
    return (punkt[0] - hoehe , punkt[1] + kantenlaenge / 2)

def koordinaten2(punkt):
    return (punkt[0] - hoehe , punkt[1] - kantenlaenge / 2)

def koordinaten3(punkt):
    return (punkt[0], punkt[1] - kantenlaenge)

def koordinaten4(punkt):
    return (punkt[0] + hoehe , punkt[1] - kantenlaenge / 2)

def koordinaten5(punkt):
    return (punkt[0] + hoehe , punkt[1] + kantenlaenge / 2)

def koordinaten6(punkt):
    return (punkt[0], punkt[1] + kantenlaenge)