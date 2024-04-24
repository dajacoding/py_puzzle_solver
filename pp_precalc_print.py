import time

# gibt an, wieviele Teile auf das Spielfeld gelegt werden sollen; 1 - 12
testLaenge = 11

# gibt die Position des Sonderelements an; 0 - 9
positionSonderElement = 7

# Main
def funktionStart():    
    # startZeit = time.ctime(time.time())
    # print("Startzeit:  ", startZeit)
    loesung = listenPruefung(alleSonderelementPositionen[positionSonderElement])
    # schlussZeit = time.ctime(time.time())
    # print("Schlusszeit:", schlussZeit)

    # for l in range(int((len(loesung)) / 5)):        
    #     print(loesung[1 + l * 5 : 6 + l * 5])
    # print(int((len(loesung)) / 5))
    
    ausdruck(loesung)
   
    return loesung

def ausdruck(loesung):
    x = 1
    for teil in loesung:
        dateiname = 'Teil' + str(x)
        with open(dateiname+'.txt', 'w') as f:
            for line in teil:
                for l in line:
                    f.write(str(l))
                    f.write(' ')
                f.write('\n')
        x = x + 1
    return


# vorbereiten der Listen
def listenPruefung(sonderElement):    
    felder = koordinatenInReihen
    loesung = [elementAbgleich(sorted(sonderElement), felder)] # ANPASSUNG print() in funktionStart(): '1'

    teileInPositionen = []
    for i in range(len(allePuzzleElemente)):
        teilInPositionen = []
        for teil in [allePuzzleElemente[i], rotation(allePuzzleElemente[i]), rotation(rotation(allePuzzleElemente[i]))]:
            for feld in felder:
                temp = [koordinatenInListenform(feld, element) for element in teil]
                pos = [elementAbgleich(t, felder) for t in temp if elementAbgleich(t, felder) != None]
                if len(pos) == 5:
                    teilInPositionen.append(pos)
        teileInPositionen.append(teilInPositionen)  
    
    return teileInPositionen




#################################
###### Vorbereitender Part ######
##### Definition der Listen #####
################################# 



# Koordinaten - Pfad mit Felder - Liste abgleichen
def elementAbgleich(element, felder):
    for f, feld in enumerate(felder):
        if sorted(feld) == element: return f
    return None


# Pfad eines Elements kreieren
def koordinatenInListenform(pfad, element):
    unbereinigt = allesInEineListe(pfad, element)
    return vektorEinkuerzen(unbereinigt)


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


funktionStart()