import time

# gibt an, wieviele Teile auf das Spielfeld gelegt werden sollen; 1 - 12
testLaenge = 11

# gibt die Position des Sonderelements an; 0 - 9
positionSonderElement = 7

def funktionStart():    
    print("Startzeit:  ", time.ctime(time.time()))
    loesung = listenPruefung(alleSonderelementPositionen[positionSonderElement])
    print("Schlusszeit:", time.ctime(time.time()))
    print(loesung.index(None))
    print(loesung)
    return loesung


# pruefen mittels Listen
def listenPruefung(sonderElement):    
    teile = listeMoeglicherPuzzleElemente()
    # felder = alleKoordinaten
    felder = koordinatenInReihen
    belegteFelder = unbelegteFelder()
    belegteFelder[elementAbgleich(sorted(sonderElement if type(sonderElement) != int else [sonderElement]), felder)] = -1

    return feldUndTeil(felder, teile, belegteFelder)


# Abfrage nach jeder Feld - Teil - Kombination
def feldUndTeil(felder, teile, belegteFelder):

    # if not reihenBelegt(belegteFelder):
    #     return rueckbauBelegteFelder(belegteFelder)

    for f, feld in enumerate(felder):         
        if belegteFelder[f] != None: continue 
        for teilnummer, teil in enumerate(teile):            
            if teilVorhanden(gleichesTeil(teilnummer), belegteFelder): continue
            temp = listenAbgleich(feld, teilnummer, teil, felder, belegteFelder)
            if temp != None:
                belegteFelder = temp
                if ende(belegteFelder): return belegteFelder                
                belegteFelder = feldUndTeil(felder, teile, belegteFelder)   
                if ende(belegteFelder): return belegteFelder                
    return rueckbauBelegteFelder(belegteFelder)
    

# Pruefung auf befuellte Reihen
def reihenBelegt(belegteFelder):
    noneIndex = belegteFelder.index(None)
    # reihenLaenge = [5, 6, 7, 8, 9, 8, 7, 6, 5]
    reihenLaengeAddiert = [5, 11, 18, 26, 35, 43, 50, 56, 61]
    # anzahlBelegteFelder = len([b for b in belegteFelder[:-1] if b != None])
    rl = 0
    for e, r in enumerate(reihenLaengeAddiert):
        if r > noneIndex:
            rl = e - 3
            break
    if rl >= 0:
        for b in belegteFelder[:reihenLaengeAddiert[rl]]:
            if b == None:
                return False
    return True


# prueft auf testLaenge
def ende(belegteFelder):
    if len(belegteFelder[-1]) >= testLaenge:
        return True
    return False


# pruefen von Einzel - Teilen in Element - Unterteilung
def listenAbgleich(feld, teilnummer, teil, felder, belegteFelder):
    temp = [koordinatenInListenform(feld, element) for element in teil]
    pos = [elementAbgleich(t, felder) for t in temp if elementAbgleich(t, felder) != None]    
    if len(pos) == 5:
        if belegtAbgleich(pos, belegteFelder):
            belegteFelder[-1].append(pos)  
            for p in pos:                   
                belegteFelder[p] = teilnummer  
            return belegteFelder
    return None


# reduziert belegteFelder[-1] um 1; loescht Eintragung in belegteFelder
def rueckbauBelegteFelder(belegteFelder):
    for deleteTeilnummer in belegteFelder[-1][-1]: belegteFelder[deleteTeilnummer] = None 
    del belegteFelder[-1][-1]
    return belegteFelder


# gibt die Listen - Positionen des gleichen Teils in verschiedenen Rotationen zurueck  
def gleichesTeil(teilnummer):
    return [teilnummer, (teilnummer + 12) % 36, (teilnummer + 24) % 36]


# gibt True zurueck, wenn ein Teil bereits in belegteFelder - Liste steht
def teilVorhanden(teil3, belegteFelder):   
    for t in teil3:
        if t in set(belegteFelder[:-1]):
            return True
    return False


# gibt True zurueck, wenn jedes Element eines Teiles auf ein freies Feld passbar ist
def belegtAbgleich(teilPosListe, belegteFelder):
    for f in teilPosListe:
        if type(belegteFelder[f]) == int:
            return False
    return True 


# Koordinaten - Pfad mit Felder - Liste abgleichen
def elementAbgleich(element, felder):
    for f, feld in enumerate(felder):
        if sorted(feld) == element: return f
    return None


# Pfad eines Elements kreieren
def koordinatenInListenform(pfad, element):
    unbereinigt = allesInEineListe(pfad, element)
    bereinigt = vektorEinkuerzen(unbereinigt)
    return bereinigt


# Filtern nach moeglichen Einkuerzungen
def vektorEinkuerzen(vektor):
    temp = sorted([v for v in vektor if v != 0])      
    for e, u in enumerate(temp):
        i = e + 1 if e + 1 < len(temp) else 0
        v = temp[i]
        mk = moeglicheKombinationen(u, v)
        if (u, v) != mk:
            temp[e] = mk
            del temp[i]
            if len(temp) > 1:
                temp = vektorEinkuerzen(temp) 
                break
            if len(temp) == 1:
                return temp
    if len(temp) == 0:
        return [0]            
    return temp


# nimmt verschieden formatierte Vektoren und generiert einen   
def allesInEineListe(pfad, element):
    if type(pfad) == int: pfad = [pfad]
    if type(element) == int: element = [element]
    return pfad + element

# alle kuerzbaren Pfad - Vektoren
def moeglicheKombinationen(a, b):
    match sorted((a, b)):
        case (1, 4):
            return 0
        case (2, 5):
            return 0
        case (3, 6):
            return 0
        case (1, 3):
            return 2
        case (2, 4):
            return 3
        case (3, 5):
            return 4
        case (4, 6):
            return 5
        case (1, 5):
            return 6
        case (2, 6):
            return 1
        case _:
            return a, b        


#################################
###### Vorbereitender Part ######
##### Definition der Listen #####
################################# 

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

# Liste aller Positionen (vom Zentrum ausgehende Sortierung) 
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

# rotiert ein Element um 120 Grad im Uhrzeigersinn
def rotation(element):    
        return [(rotationsFaktor(elem) if elem != 0 else 0)
                if type(elem) == int else
                ([rotationsFaktor(e) for e in elem])
                for elem in element]

# Hilfsfunktion fuer rotation()
def rotationsFaktor(rf):
    return rf + 2 if rf <= 4 else rf - 4

# erzeuge boolsche Liste in der Konzeption des Feldaufbaus
def unbelegteFelder():  
    liste = [None for a in alleKoordinaten] 
    liste.append([])
    return liste

# Sammlung aller Teile in allen Rotationen
def listeMoeglicherPuzzleElemente():
    listeRotation1 = [rotation(element) for element in allePuzzleElemente]
    listeRotation2 = [rotation(element) for element in listeRotation1]
    return allePuzzleElemente + listeRotation1 + listeRotation2

funktionStart()