# py_puzzle_solver
zusammenfassende Datei fuer essenzielle Programmlogik: py_puzzle.py
erste Optimierung von py_puzzle ist py_puzzle_precalc.py (Vorberechnung möglicher Positionen je Teil => Listenabgleich auf doppelte Feldbelegung)

- neue Iterationsbedingung durch reihengestuetzte Initiierung der Felderliste (nur in py_puzzle.py)
- diverse Funktionen kuerzbar
- diverse Auslagerung in Funktionen vermeidbar

# das Problem

theoretische (36x61)^12 = 1.2x10^40 Kombinationen
- bruteforce - Methode
  - funktioniert; starker Optimierungsbedarf
  - zeitlicher Aufwand enorm
  -> Alternative finden
