

# gibt an, wieviele Teile auf das Spielfeld gelegt werden sollen; 1 - 12
testLaenge = 3

# gibt die Position des Sonderelements an; 0 - 9
positionSonderElement = 7



# pruefen mittels Listen
def listenPruefung(sonderelement):    
    teile = listeMoeglicherPuzzleElemente()
    felder = alleKoordinaten
    belegteFelder = unbelegteFelder()
    belegteFelder[elementAbgleich(sorted(sonderelement if type(sonderelement) != int else [sonderelement]), felder)] = -1

    return feldUndTeil(felder, teile, belegteFelder)


# Abfrage nach jeder Feld - Teil - Kombination
def feldUndTeil(felder, teile, belegteFelder):
    for f, feld in enumerate(felder): 
        if type(belegteFelder[f]) == int: continue 
        for teilnummer, teil in enumerate(teile):
            if teilVorhanden(gleichesTeil(teilnummer), belegteFelder): continue
            temp = listenAbgleich(feld, teilnummer, teil, felder, belegteFelder)
            if temp != None:
                belegteFelder = temp
                if len(belegteFelder[-1]) >= testLaenge:
                    return belegteFelder  
                belegteFelder = feldUndTeil(felder, teile, belegteFelder)   
                if len(belegteFelder[-1]) >= testLaenge:
                    return belegteFelder  
    return rueckbauBelegteFelder(belegteFelder)


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
    for deleteTeilnummer in belegteFelder[-1][-1]: belegteFelder[deleteTeilnummer] = "a" 
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
        if sorted(feld) == element:
            return f
    return None


# Pfad eines Elements kreieren
def koordinatenInListenform(pfad, element):
    unbereinigt = allesInEineListe(pfad, element)
    bereinigt = vektorEinkuerzen(unbereinigt)
    return bereinigt


# Filtern nach moeglichen Einkuerzungen
def vektorEinkuerzen(vektor):
    temp = sorted(list(filter(lambda a: a != 0, vektor)))         
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
    return sorted(list(filter(lambda a: a != 0, temp)))


# nimmt verschieden formatierte Vektoren und generiert einen   
def allesInEineListe(pfad, element):
    if type(pfad) == int: pfad = [pfad]
    if type(element) == int: element = [element]
    return sorted(pfad + element)


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


# erzeuge boolsche Liste in der Konzeption des Feldaufbaus
def unbelegteFelder():  
    liste = []  
    for a in alleKoordinaten:
        liste.append("a")
    liste.append([])
    return liste


# Sammlung aller Teile in allen Rotationen
def listeMoeglicherPuzzleElemente():
    liste = allePuzzleElemente
    listeRotation1 = []
    for element in liste:
        listeRotation1.append(rotation(element))
    listeRotation2 = []
    for element in listeRotation1:
        listeRotation2.append(rotation(element))
    liste += listeRotation1
    liste += listeRotation2    
    return liste


# alle kuerzbaren Pfad - Vektoren
def moeglicheKombinationen(a, b):
    x = sorted((a, b))
    if x == (1, 4):
      return 0
    elif x == (2, 5):
      return 0
    elif x ==  (3, 6):
      return 0
    elif x ==  (1, 3):
      return 2
    elif x ==  (2, 4):
      return 3
    elif x ==  (3, 5):
      return 4
    elif x ==  (4, 6):
      return 5
    elif x ==  (1, 5):
      return 6
    elif x ==  (2, 6):
      return 1
    else:
      return a, b        


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

                              
loesung = listenPruefung(alleSonderelementPositionen[positionSonderElement])
print(loesung)
