import myLogic
import time

testLaenge = 11


# pruefen mittels Listen
def listenPruefung(sonderelement):    
    teile = myLogic.listeMoeglicherPuzzleElemente()
    felder = myLogic.alleKoordinaten
    belegteFelder = myLogic.unbelegteFelder()
    belegteFelder[elementAbgleich(sorted(sonderelement if type(sonderelement) != int else [sonderelement]), felder)] = -1

    return feldUndTeil(felder, teile, belegteFelder, 0)


# Abfrage nach jeder Feld - Teil - Kombination
def feldUndTeil(felder, teile, belegteFelder, z):
    for f, feld in enumerate(felder): 
        if type(belegteFelder[f]) == int: continue 
        for teilnummer, teil in enumerate(teile):
            if teilVorhanden(gleichesTeil(teilnummer), belegteFelder): continue

            # Gibt die Veränderungszeit der ersten 3 gelegeten Teile wieder
            if z < 3:
                print(z, f, teilnummer, time.ctime(time.time()))

            temp = listenAbgleich(feld, teilnummer, teil, felder, belegteFelder)
            if temp != None:
                belegteFelder = temp
                if len(belegteFelder[-1]) >= testLaenge:
                    return belegteFelder  
                belegteFelder = feldUndTeil(felder, teile, belegteFelder, z + 1)   
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


# alle kuerzbaren Pfad - Vektoren
def moeglicheKombinationen(a, b):
    x = sorted((a, b))
    match x:
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
        

# nimmt verschieden formatierte Vektoren und generiert einen   
def allesInEineListe(pfad, element):
    if type(pfad) == int: pfad = [pfad]
    if type(element) == int: element = [element]
    return sorted(pfad + element)




############################################################################
### eventuell spaeter ### Ansaetze / Ideen ### muss ueberarbeitet werden ### 
############################################################################




# returned liste mit der Haeufikeitsverteilung der Vektor - Teile
def indexiereListe(liste, typeListe):
    temp = []
    for e in range(len(typeListe)):
        zaehler = 0
        for l in liste:
            if l == e:
                zaehler += 1
        temp.append(zaehler)
    return temp


# kuerzen des Pfades um entgegengesetzte Schritte
def koordinatenKuerzung(pfad):
    temp = pfad
    for m, p in enumerate(pfad):
        for n, f in enumerate(pfad):
            if p - f == 3 and f != 0:
                if m > n:
                    del temp[m]
                del temp[n]
                if m < n:
                    del temp[m]
                if len(temp) == 0:
                    temp.append(0)
                break
    return temp
                
# Umwege des Pfades kuerzen
def koordinatenDirekt(pfad):
    temp = pfad
    if len(set(temp)) >= 3:
        if max(temp) - min(temp) == 2 and min(temp) != 0:
            temp[temp.index(min(temp))] += 1
            del temp[temp.index(max(temp))]
            return temp
        if max(temp) - min(temp) == 5 and min(temp) != 0:
            if min(temp) == 1:
                temp[temp.index(max(temp))] += 1
                del temp[temp.index(min(temp))]
            else:
                temp[temp.index(min(temp))] += 1
                del temp[temp.index(max(temp))]
            return temp
    return temp



# iteriert durch Felder und initiiert Teil - Abgleich
def allgemeineAbfrage(teile, felder, belegteFelder, startFeld):
    len_felder = len(felder)
    for f in range(len_felder):
        f_startFeld = f + startFeld
        feldnummer = (f_startFeld if f_startFeld < len_felder else f_startFeld - len_felder)  
        for t, teil in enumerate(teile):
            belegteFelder = listenAbgleich(felder[feldnummer], t, teil, felder, belegteFelder)
    return belegteFelder


# pruefen auf doppeltes Teil
def nichtDoppeltesTeil(teilnummer, belegteFelder):
    t3 = gleichesTeil(teilnummer)
    for e, i in enumerate(set(belegteFelder[:-1])):
        for t in t3:            
            if t == belegteFelder[e]:
                return False
    return True