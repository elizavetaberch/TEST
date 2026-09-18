# Linux Command-Line Learning Progress

## Session: Batch File Renaming with find + exec

### Command Learned
```bash
find . -type f -name "*.*" -exec sh -c 'mv "$1" "${1%.*}"' _ {} \;
```

### Breaking It Down
- `find . -type f -name "*.*"` — Find all files with extensions
- `-exec sh -c '...' _ {} \;` — Execute a shell command for each file
- `"$1"` — The current filename (in double quotes to allow spaces)
- `"${1%.*}"` — Remove extension using string trimming pattern
  - `${var%pattern}` removes trailing pattern from variable
  - `%.*` means "remove everything from last dot onwards"

### Example
```
Before: animi.doc, libero.xls, report.txt
After:  animi, libero, report
```

### Key Insight: Testing Before Running
Always test with `echo` first:
```bash
# Test version
find . -type f -name "*.*" -exec sh -c 'echo mv "$1" "${1%.*}"' _ {} \;

# Then run actual command
find . -type f -name "*.*" -exec sh -c 'mv "$1" "${1%.*}"' _ {} \;
```

### Quote Handling
```bash
'mv "$1" "${1%.*}"'
^                 ^
└─ Single quotes wrap entire program for sh
   "$1"  ← Double quotes protect variables
   "${1%.*}"  ← Double quotes protect parameter expansion
```

## Commands Practiced So Far
- Basic navigation: cd, pwd, ls
- File operations: cp, mv, rm, rm -r
- Text processing: cat, head, tail, grep, sed, tr, awk
- Searching: find with -type, -name, -exec, -maxdepth
- Permissions: chmod with symbolic notation
- Redirection: >, >>, |
- Symbolic links: ln -s
- Advanced: find -exec with sh -c for batch operations
