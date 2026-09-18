# Linux für Anfänger - Offline Guide

## Grundkonzepte

### Command Struktur
```
command [options] [arguments]
ls       -la      /home
```

### Wichtige Verzeichnisse
```
/home      - Benutzer Home-Verzeichnisse
/tmp       - Temporäre Dateien
.          - Aktuelles Verzeichnis
..         - Übergeordnetes Verzeichnis
~          - Dein Home (/home/username)
```

---

## Navigation (cd, ls, pwd)

```bash
pwd                    # Wo bin ich? (Print Working Directory)
ls                     # Dateien anzeigen
ls -l                  # Detaillierte Liste
ls -la                 # Mit versteckten Dateien (die mit .)
ls -R                  # Rekursiv (Unterordner auch)

cd /path/to/dir        # In Verzeichnis gehen
cd ..                  # Ein Verzeichnis hoch
cd ~                   # Nach Hause (Home-Verzeichnis)
cd -                   # Zum letzten Verzeichnis
```

---

## Dateien & Verzeichnisse

### Erstellen
```bash
touch file.txt         # Leere Datei erstellen
touch file{1..5}.txt   # file1.txt bis file5.txt (Brace Expansion!)
mkdir myfolder         # Verzeichnis erstellen
mkdir -p a/b/c         # Mit Eltern-Ordnern (-p = parents)
```

### Kopieren
```bash
cp file1.txt file2.txt           # Datei kopieren
cp -r folder1 folder2            # Ordner kopieren (rekursiv)
cp *.txt backup/                 # Alle .txt Dateien kopieren
```

### Verschieben/Umbenennen
```bash
mv file1.txt file2.txt           # Umbenennen
mv file.txt /path/to/folder/     # Verschieben
mv *.txt backup/                 # Alle Dateien verschieben
```

### Löschen
```bash
rm file.txt                      # Datei löschen
rm -r folder/                    # Ordner löschen (rekursiv!)
rm *.txt                         # Alle .txt Dateien löschen
```

**ACHTUNG:** `rm` löscht PERMANENT - kein Papierkorb!

---

## Dateiinhalt anschauen

```bash
cat file.txt                     # Ganze Datei anzeigen
head file.txt                    # Erste 10 Zeilen
head -n 5 file.txt              # Erste 5 Zeilen
tail file.txt                    # Letzte 10 Zeilen
tail -n 5 file.txt              # Letzte 5 Zeilen
```

---

## Suchen

### find - Nach Dateien suchen
```bash
find . -name "*.txt"             # Alle .txt Dateien
find . -type f -name "*.txt"     # Nur Dateien (f), keine Ordner
find . -type d -name "*backup*"  # Nur Ordner (d)
find . -name "*.*"               # Alle Dateien mit Extension
find . -type f -maxdepth 2       # Nur 2 Ebenen tief
```

### grep - Im Inhalt suchen
```bash
grep "searchword" file.txt       # Zeilen mit searchword finden
grep -n "word" file.txt          # Mit Zeilennummern
grep -c "word" file.txt          # Nur Anzahl zählen
grep -i "word" file.txt          # Case-insensitive (auch Word, WORD)
```

---

## Wildcards & Patterns

```bash
*.txt              # Alle Dateien mit .txt Endung
test?              # test1, test2, aber nicht test10 (nur 1 Zeichen)
test[1-3]          # test1, test2, test3
test{1..5}         # test1 bis test5 (Brace Expansion)
[abc]*             # Dateien die mit a, b oder c anfangen
```

---

## Pipes & Redirection

### Redirection (Umleitung)
```bash
command > file.txt              # Output in Datei schreiben (überschreiben)
command >> file.txt             # Output anhängen (nicht überschreiben)
command < file.txt              # Input aus Datei lesen
```

### Pipes (|)
```bash
cat file.txt | grep "word"       # Inhalt durchsuchen
cat file.txt | head -n 5         # Nur erste 5 Zeilen
ls -la | grep ".txt"             # Nur .txt Dateien in ls-Output
```

---

## Text Verarbeitung

### sed - Suchen & Ersetzen
```bash
sed 's/alt/neu/' file.txt        # Ersetze "alt" durch "neu"
sed 's/alt/neu/g' file.txt       # Alle Vorkommen ersetzen (g=global)
sed -i 's/alt/neu/g' file.txt    # In-place Änderung (verändet Datei direkt)
```

### awk - Spalten verarbeiten
```bash
awk '{print $1}' file.txt        # Erste Spalte drucken
awk '{print $1, $3}' file.txt    # Spalte 1 und 3
awk '{sum+=$1} END {print sum}' file.txt   # Erste Spalte addieren
```

### tr - Zeichen ersetzen
```bash
echo "hello" | tr 'a-z' 'A-Z'    # Lowercase zu Uppercase
tr '\n' ' ' < file.txt           # Newlines zu Spaces
```

---

## Dateiberechtigungen (chmod)

### Basis-Konzept
```
-rwxr-xr-x
^owner group others
r = read (4)
w = write (2)
x = execute (1)
```

### Ändern mit Symbolen
```bash
chmod u+x file.txt              # Owner: execute hinzufügen
chmod g+w file.txt              # Group: write hinzufügen
chmod o-r file.txt              # Others: read entfernen
chmod a+r file.txt              # Alle: read hinzufügen
chmod 755 file.txt              # rwxr-xr-x (numerisch)
chmod 644 file.txt              # rw-r--r-- (typisch für Dateien)
```

---

## Batch-Operationen (find -exec)

### Pattern: Befehle auf mehrere Dateien anwenden
```bash
# Alle .txt Dateien löschen
find . -name "*.txt" -exec rm {} \;

# Alle .txt Dateien anzeigen (mit Echo als Test)
find . -name "*.txt" -exec echo {} \;

# Alle .doc Dateien umbenennen (Extension entfernen)
find . -type f -name "*.*" -exec sh -c 'mv "$1" "${1%.*}"' _ {} \;
```

### Erklärung der find -exec Syntax
```bash
find . -name "*.txt" -exec sh -c 'COMMAND_HERE' _ {} \;
                                              ^^
                                        Dateiname ersetzen hier
                                        
'mv "$1" "${1%.*}"'
  ^^^^   ^^^^^^^^^
  alte    neue
  Datei   Datei
  
${1%.*}  = Variable $1 mit Endung entfernen
           % bedeutet: von RECHTS entfernen
           .* bedeutet: punkt + beliebige Zeichen
```

---

## Nützliche Shortcuts

```bash
↑ / ↓              # Befehlsverlauf durchgehen
Ctrl+A             # Anfang der Zeile
Ctrl+E             # Ende der Zeile
Ctrl+U             # Ganze Zeile löschen
Ctrl+C             # Befehl abbrechen
Ctrl+R             # Befehl aus Geschichte suchen
Tab                # Auto-complete (Dateinamen, Befehle)
```

---

## Häufige Fehler & Lösungen

### Fehler 1: `ls: cannot access 'file.txt': No such file or directory`
**Problem:** Datei existiert nicht oder falscher Pfad
**Lösung:** `pwd` und `ls` verwenden, um zu checken wo du bist

### Fehler 2: `rm: cannot remove 'folder': Is a directory`
**Problem:** Du versuchst Ordner mit `rm` zu löschen
**Lösung:** `rm -r folder` (mit -r für rekursiv)

### Fehler 3: `grep: No such file or directory`
**Problem:** grep ist nicht für Befehle, sondern für Dateiinhalt!
**Lösung:** `grep "word" file.txt` (nicht `grep "word"`)
**Richtig:** `find . -name "*.txt" | grep "word"` (mit pipe)

### Fehler 4: `Unterminated quoted string`
**Problem:** Anführungszeichen nicht ausgewogen
**Lösung:** Prüfe ob jedes ' oder " geschlossen ist

### Fehler 5: Command mit find funktioniert nicht
**Problem:** find -exec braucht `sh -c` für komplexe Befehle
**Lösung:** `find . -exec sh -c 'COMMAND_HERE' _ {} \;`

---

## Lern-Strategie

### Level 1 (Basics)
- ✅ cd, ls, pwd
- ✅ touch, mkdir, cp, mv, rm
- ✅ cat, head, tail
- ✅ grep (nach Text suchen)

### Level 2 (Intermediate)
- ✅ find (Dateien suchen)
- ✅ Wildcards: *.txt, test{1..5}
- ✅ Pipes: | 
- ✅ sed: Suchen & Ersetzen

### Level 3 (Advanced)
- ✅ find -exec sh -c (Batch-Operationen)
- ✅ awk (Spalten-Verarbeitung)
- ✅ chmod (Berechtigungen)
- ✅ Variable Expansion: ${var%pattern}

---

## Praktische Übungen

### Übung 1: Ordner strukturieren
```bash
mkdir project && cd project
touch file{1..5}.txt
mkdir backup
cp *.txt backup/
ls backup/
```

### Übung 2: Dateien filtern
```bash
find . -name "*.txt" | grep -v backup
find . -type f -name "*1*"
```

### Übung 3: Text ersetzen
```bash
echo "hello world" > test.txt
sed 's/world/Linux/' test.txt
sed -i 's/world/Linux/' test.txt    # Datei ändern
cat test.txt
```

### Übung 4: Batch-Operation
```bash
touch report.doc data.xls config.ini
find . -name "*.*" -exec sh -c 'echo mv "$1" "${1%.*}"' _ {} \;
find . -name "*.*" -exec sh -c 'mv "$1" "${1%.*}"' _ {} \;
ls
```

---

## Ressourcen zum Weiterlesen

- **Bashcrawl:** Browser-basiertes Dungeon-Abenteuer
- **Command Line Murders:** Kriminalfall mit Linux lösen
- **OverTheWire Bandit:** Progressive SSH-Challenges
- **Linux Survival:** Quiz + praktische Übungen

---

## Wichtigste Regeln

1. **Immer `pwd` nutzen wenn du verwirrt bist** - Wissen wo du bist!
2. **Mit `echo` testen vor `mv` oder `rm`** - Sicher ist sicher!
3. **Wildcards verstehen: `*.txt` = alle .txt Dateien**
4. **Pipes verbinden Befehle: output eines Befehls = input des nächsten**
5. **find vs grep:** find = Dateien suchen, grep = Inhalt suchen

---

**Letzte Update:** 2026-09-18
**Version:** 1.0 für Anfänger

Viel Erfolg! 🚀
