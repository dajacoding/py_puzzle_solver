import myPieces


# Liste aller Positionen
alleKoordinaten = [[0], [1], [2], [3], [4], [5], [6], 
                   [1, 1], [1, 2], 
                   [2, 2], [2, 3], 
                   [3, 3], [3, 4], 
                   [4, 4], [4, 5], 
                   [5, 5], [5, 6], 
                   [6, 6], [6, 1],
                   [1, 1, 6], [1, 1, 1], [1, 1, 2], 
                   [2, 2, 1], [2, 2, 2], [2, 2, 3], 
                   [3, 3, 2], [3, 3, 3], [3, 3, 4],
                   [4, 4, 3], [4, 4, 4], [4, 4, 5],
                   [5, 5, 4], [5, 5, 5], [5, 5, 6],
                   [6, 6, 5], [6, 6, 6], [6, 6, 1],
                   [1, 1, 1, 6], [1, 1, 1, 1], [1, 1, 1, 2], 
                   [1, 1, 2, 2],
                   [2, 2, 2, 1], [2, 2, 2, 2], [2, 2, 2, 3],
                   [2, 2, 3, 3],
                   [3, 3, 3, 2], [3, 3, 3, 3], [3, 3, 3, 4], 
                   [3, 3, 4, 4],
                   [4, 4, 4, 3], [4, 4, 4, 4], [4, 4, 4, 5],
                   [4, 4, 5, 5],
                   [5, 5, 5, 4], [5, 5, 5, 5], [5, 5, 5, 6],
                   [5, 5, 6, 6],
                   [6, 6, 6, 5], [6, 6, 6, 6], [6, 6, 6, 1],
                   [6, 6, 1, 1] 
                  ]

# Liste aller Positionen (Sortierung in Reihen)
koordinatenInReihen =[[6, 6, 6, 6], [6, 6, 6, 1], [6, 6, 1, 1], [6, 1, 1, 1], [1, 1, 1, 1],
                      [6, 6, 6, 5], [6, 6, 6], [6, 6, 1], [6, 1, 1], [1, 1, 1], [1, 1, 1, 2],
                      [6, 6, 5, 5], [6, 6, 5], [6, 6], [6, 1], [1, 1], [1, 1, 2], [1, 1, 2, 2],
                      [6, 5, 5, 5], [6, 5, 5], [6, 5], [6], [1], [1, 2], [1, 2, 2], [1, 2, 2, 2],
                      [5, 5, 5, 5], [5, 5, 5], [5, 5], [5], [0], [2], [2, 2], [2, 2, 2], [2, 2, 2, 2],
                      [4, 5, 5, 5], [4, 5, 5], [4, 5], [4], [3], [3, 2], [3, 2, 2], [3, 2, 2, 2],
                      [4, 4, 5, 5], [4, 4, 5], [4, 4], [4, 3], [3, 3], [3, 3, 2], [3, 3, 2, 2],
                      [4, 4, 4, 5], [4, 4, 4], [4, 4, 3], [4, 3, 3], [3, 3, 3], [3, 3, 3, 2],
                      [4, 4, 4, 4], [4, 4, 4, 3], [4, 4, 3, 3], [4, 3, 3, 3], [3, 3, 3, 3]
                     ]

# erzeuge boolsche Liste in der Konzeption des Feldaufbaus
def unbelegteFelder():  
    liste = []  
    for a in alleKoordinaten:
        liste.append("a")
    liste.append([])
    return liste

# Sammlung aller Teile in allen Rotationen
def listeMoeglicherPuzzleElemente():
    liste = myPieces.allePuzzleElemente
    listeRotation1 = []
    for element in liste:
        listeRotation1.append(myPieces.rotation(element))
    listeRotation2 = []
    for element in listeRotation1:
        listeRotation2.append(myPieces.rotation(element))
    liste += listeRotation1
    liste += listeRotation2    
    return liste
