# py_puzzle_solver

zusammenfassende Datei fuer essenzielle Programmlogik: pp_precalc_print.py
- Ausgabe von 12 txt Dateien
  - alle moeglichen koordinaten von je einem Teil in einer Datei
  - Aufbau einer Zeile: '12 3 45 6 7', entspricht einen Teil an einer Position
  - Anzahl der Zeilen je Datei ca. 84 - 108

# das Problem

theoretische (36x61)^12 = 1.2x10^40 Kombinationen
- bruteforce - Methode
  - funktioniert; starker Optimierungsbedarf
  - zeitlicher Aufwand enorm -> Alternative finden
- bei Vorcalculation aller Koordinaten:
  - 641.805.762.426.921.958.440.960 Moeglichkeiten -> 6.4x10^23
