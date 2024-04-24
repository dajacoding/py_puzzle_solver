# py_puzzle_solver

zusammenfassende Datei fuer essenzielle Programmlogik: pp_precalc_print.py
- ausgabe von 12 txt dateien
  - alle moeglichen koordinaten von je einem teil in einer datei
  - aufabau einer Zeile: '12 3 45 6 7'
  - anzahl der zeilen je datei ca. 84 - 108

# das Problem

theoretische (36x61)^12 = 1.2x10^40 Kombinationen
- bruteforce - Methode
  - funktioniert; starker Optimierungsbedarf
  - zeitlicher Aufwand enorm
  -> Alternative finden
- bei Vorcalculation aller Koordinaten:
  - 641.805.762.426.921.958.440.960 Moeglichkeiten
  -> 6.4x10^23
