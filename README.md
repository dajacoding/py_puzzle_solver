# py_puzzle_solver

## Problem

- Es sind 12 Puzzleteile gegeben, die zu einem Sechseck sortiert werden müssen
- $183^{12}$ Kombinationen, was etwa $1.4\cdot10^{27}$ entspricht
- Via BruteForce dauert die Berechnung auf meinem Server etwa 5 mrd Jahre

## Lösung

- Optimierung der Berechnungen
- Filterung des Datensatzes
- Berechnungsdauer 100 Tage

## Dokumentation

https://davidjann.de/puz_fin.html

## Anmerkung

- *dist* enthält ein für Windows kompiliertes Programm, das die Darstellung, nach dem Bereitstellen von 3 `u64`-Lösungselementen, erzeugt. Der Ordner enthält *_loesung.txt*, in der exemplarisch 5 Lösungs-Einträge hinterlegt sind.
- Die Ordner *python* und *rust* enthalten die jeweiligen Programmteile
