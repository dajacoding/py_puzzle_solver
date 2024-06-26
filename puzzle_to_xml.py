# Programm zum Ausdruck von einer XML Datei, 
# deren Inhalt Koordinatensaetze je Puzzleteil sind
# Aufbau:
#<teile>
#    <teil>
#        <typ>teil1</typ>
#        <id>1</id>
#        <koords>
#            <k1>1</k1>
#            <k2>6</k2>
#            <k3>11</k3>
#            <k4>12</k4>
#            <k5>20</k5>
#        </koords>
#    </teil>
#    [...]
#    <teil>
#        <typ>teil12</typ>
#        <id>87</id>
#        <koords>
#            <k1>47</k1>
#            <k2>48</k2>
#            <k3>49</k3>
#            <k4>53</k4>
#            <k5>58</k5>
#        </koords>
#    </teil>
#</teile>


# Main
def funktionStart():    
    loesung = listenPruefung()
    ausdruck(loesung)   
    return loesung


# schreiben der Koordinaten in eine XML Datei
def ausdruck(loesung):
    x = 1
    sAnfang = '<teile>\n'
    sEnde = '</teile>\n'
    sGesamt = sAnfang    
    for teil in loesung:
        z = 1
        for line in teil:
            sMitte = '    <teil>\n'
            sMitte += '        <typ>teil' + str(x) + '</typ>\n'
            sMitte += '        <id>' + str(z) + '</id>\n'
            sMitte += '        <koords>\n'
            for k in range(5):
                sMitte += '            <k' + str(k + 1) + '>'
                sMitte += str(sorted(line)[k])
                sMitte += '</k' + str(k + 1) + '>\n'
            sMitte += '        </koords>\n'
            sMitte += '    </teil>\n'
            sGesamt += sMitte
            z += 1
        x += 1
    sGesamt += sEnde 
    with open('teile_koords.xml','w') as var:
        var.write(sGesamt)
    return    

# vorbereiten der Listen
def listenPruefung():    
    felder = koordinatenInReihen
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
