# Linux Anfänger - Praktische Aufgaben

Nutze den **LINUX_ANFAENGER_GUIDE.md** um diese Aufgaben zu lösen!

---

## Level 1: Basics (Navigation & Dateien)

### Aufgabe 1.1: Verzeichnis strukturieren
1. Erstelle einen Ordner `projects`
2. Gehe in den Ordner
3. Erstelle 3 Textdateien: `report.txt`, `data.txt`, `notes.txt`
4. Zeige alle Dateien (mit `ls`)

**Hinweis:** `mkdir`, `cd`, `touch`, `ls`

---

### Aufgabe 1.2: Dateien kopieren
1. Erstelle einen `backup/` Ordner
2. Kopiere alle `.txt` Dateien dahin
3. Überprüfe, dass alle Kopien im backup/ sind

**Hinweis:** `mkdir`, `cp`, Wildcard `*.txt`

---

### Aufgabe 1.3: Dateien verschieben
1. Erstelle eine neue Datei: `temp.txt`
2. Verschiebe sie in den `backup/` Ordner
3. Prüfe mit `ls` dass sie weg ist

**Hinweis:** `touch`, `mv`, `ls`

---

## Level 2: Suchen & Filtern

### Aufgabe 2.1: find verwenden
1. Gehe in dein Home-Verzeichnis
2. Finde ALLE `.txt` Dateien in allen Unterordnern
3. Zeige nur die gefundenen Dateien

**Hinweis:** `find .`, `-name "*.txt"`, `-type f`

---

### Aufgabe 2.2: grep verwenden
1. Erstelle eine Datei mit mehreren Zeilen:
   ```
   Apple is red
   Banana is yellow
   Apple is green
   ```
2. Suche nach "Apple" in der Datei
3. Zähle wie viele Zeilen "Apple" enthalten

**Hinweis:** `echo`, Redirection `>`, `grep`, `-c` Flag

---

### Aufgabe 2.3: Kombinieren von Befehlen
1. Finde alle Dateien in einem Ordner
2. Filtere nur die `.txt` Dateien heraus
3. Zähle wie viele es sind

**Hinweis:** `find`, `grep`, Pipe `|`, `-c`

---

## Level 3: Text Processing

### Aufgabe 3.1: sed - Suchen & Ersetzen
1. Erstelle eine Datei `config.txt` mit:
   ```
   server=localhost
   port=8000
   debug=false
   ```
2. Ersetze `localhost` durch `192.168.1.1`
3. Überprüfe das Ergebnis mit `cat`

**Hinweis:** `echo`, `sed 's/alt/neu/'`, Redirection `>`

---

### Aufgabe 3.2: sed in-place Änderung
1. Nimm die `config.txt` von oben
2. Ändere `debug=false` zu `debug=true` DIREKT in der Datei
3. Überprüfe mit `cat` dass die Datei geändert wurde

**Hinweis:** `sed -i`, `-i` bedeutet "in-place"

---

### Aufgabe 3.3: awk - Spalten verarbeiten
1. Erstelle eine Datei `sales.txt`:
   ```
   Product Price Quantity
   Apple 2 10
   Banana 1 5
   Orange 3 8
   ```
2. Zeige nur die erste Spalte (Produkte)
3. Berechne die Summe der Quantities (3. Spalte)

**Hinweis:** `awk '{print $1}'`, `awk '{sum+=$3} END {print sum}'`

---

## Level 4: Batch-Operationen

### Aufgabe 4.1: Mehrere Dateien erstellen
1. Erstelle 10 Dateien in einem Schuss: `file1.txt` bis `file10.txt`
2. Zeige alle Dateien

**Hinweis:** Brace Expansion `{1..10}`

---

### Aufgabe 4.2: find -exec mit echo (Test)
1. Erstelle 5 Dateien: `doc1.pdf`, `doc2.pdf`, `report.txt`, `data.csv`, `config.ini`
2. Finde alle Dateien MIT Extension
3. Zeige sie an (TEST mit echo vorher!)
4. Lösche sie dann

**Hinweis:** `find . -name "*.*"`, `-exec`, `echo` zum Testen, `rm`

---

### Aufgabe 4.3: Batch umbenennen
1. Erstelle 3 Dateien: `photo1.jpg`, `photo2.jpg`, `photo3.jpg`
2. Benenne sie um zu: `photo1`, `photo2`, `photo3` (ohne .jpg)
3. Überprüfe das Ergebnis

**Hinweis:** `find -exec sh -c`, `${1%.*}` zum Extension entfernen

---

### Aufgabe 4.4: Mehrere Verzeichnisse durchsuchen
1. Erstelle diese Struktur:
   ```
   project/
   ├── src/
   │   ├── code.txt
   │   └── data.txt
   ├── backup/
   │   └── old.txt
   └── readme.md
   ```
2. Finde ALLE `.txt` Dateien in ALLEN Unterordnern
3. Lösche sie mit find -exec

**Hinweis:** `find . -name "*.txt"`, `-type f`, `-exec rm`

---

## Bonus: Komplexe Aufgaben

### Bonus 1: Logdatei-Analyse
1. Erstelle `log.txt` mit:
   ```
   2024-01-15 ERROR Failed login
   2024-01-15 INFO User created
   2024-01-16 ERROR Connection timeout
   2024-01-16 WARNING High memory
   2024-01-16 ERROR Failed backup
   ```
2. Zähle wie viele ERROR-Zeilen es gibt
3. Zeige nur die WARNING-Zeilen
4. Ersetze alle "ERROR" durch "CRITICAL"

**Hinweis:** `grep -c`, `grep`, `sed`

---

### Bonus 2: Datei-Statistik
1. Erstelle verschiedene Dateien (unterschiedliche Größen)
2. Finde alle Dateien größer als 100 Bytes
3. Zähle wie viele `.txt` Dateien es insgesamt gibt

**Hinweis:** `find`, `-size`, `grep -c`, Pipes

---

### Bonus 3: Backup-Script (manuell)
1. Erstelle einen `data/` Ordner mit mehreren Dateien
2. Erstelle einen `backups/` Ordner
3. Kopiere ALLE Dateien von `data/` nach `backups/data_BACKUP/`
4. Überprüfe dass alles kopiert wurde

**Hinweis:** `mkdir -p`, `cp -r`, `ls -R`

---

## Tipps zum Lösen

1. **Immer `pwd` nutzen** wenn du nicht weißt wo du bist
2. **Mit `echo` testen** bevor du `rm` oder `mv` nutzt
3. **Die Dokumentation verwenden** - Beispiele sind dort!
4. **Schritt für Schritt** - Erst kleine Tests, dann echte Befehle
5. **Tab zum Auto-complete** nutzen!

---

## Schwierigkeitsgrade

```
⭐ Level 1.1 - 1.3         = Anfänger (Basics)
⭐⭐ Level 2.1 - 2.3         = Anfänger+ (find/grep)
⭐⭐⭐ Level 3.1 - 3.3         = Intermediate (sed/awk)
⭐⭐⭐⭐ Level 4.1 - 4.4         = Advanced (Batch-Ops)
⭐⭐⭐⭐⭐ Bonus 1 - 3          = Expert (Kombination)
```

---

**Strategie zum Lernen:**
1. Mach Level 1 komplett (sollte 10-15 min sein)
2. Mach Level 2 komplett (20-30 min)
3. Mach Level 3 komplett (30-40 min)
4. Mach Level 4 komplett (40-60 min)
5. Optional: Bonus-Aufgaben

Insgesamt: ~2-3 Stunden für alle Aufgaben mit Pausen.

Viel Erfolg! 🚀
