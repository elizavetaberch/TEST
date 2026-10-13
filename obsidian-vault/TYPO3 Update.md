---
tags: [arbeit, prozess, typo3]
---

# TYPO3 Update — Ablauf

Meine eigene Spickzettel-Notiz. Die Schritte sind überall gleich, **die Details nicht**: Branch-Namen, Deploy-Umgebungen, Reviewer. Immer im jeweiligen Repo nachsehen.

## 0. Ticket

- Ticket kommt aus Jira, oder mündlich → **selbst eins anlegen**
- gar kein Ticket möglich → im Repo gibt es Platzhalter: `SB-0`, `VRS-0`, `AUS-0`
- Status auf **In Progress**

Commit-Präfix: tatsächlich benutzt wurde `[SECURITY]`, auch wenn im Ticket `Standard Update` stand. In der History gibt es beides (`[UPDATE]`, `[SECURITY]`, `[TASK]`) — im Zweifel schauen, was im Repo üblich ist.

## 1. Repo vorbereiten

```bash
cd ~/www/project/<projekt>
git status
grep '"typo3/cms-core"' composer.json          # von welcher Version aus?
git log --all --oneline -i --grep="update" -15 # wie hat man das hier zuletzt gemacht?
```

```bash
git checkout master        # ⚠️ mal master, mal main
git pull
git checkout -b VRS-502-composer-update
```

> [!warning] Hauptbranch prüfen
> `git branch -a | head` → `remotes/origin/HEAD -> origin/???`
> SWG und vrs → `master`, Sprungbrett → `main`.

> [!danger] Fremde uncommittete Änderungen
> Die gehören **keinem Branch** und wandern bei jedem `git switch` mit. Vor dem Update klären, sonst landen sie im Update-Commit.
> ```bash
> git diff <datei>
> git diff | cat -A        # macht Leerzeichen und unsichtbare Zeichen sichtbar
> git stash                # wegpacken, später: git stash pop
> ```

## 2. Update

```bash
ddev composer update       # kurz: ddev composer u
```

Optional, aber in SWG so üblich: die gepinnten Constraints in `composer.json` von Hand hochziehen (`^13.4.35` → `^13.4.36`). Lose Constraints (`">=13.4.20"`, `"^13"`) nicht anfassen.

> [!note] PhpStorm zeigt zwei Versionen
> `"typo3/cms-core": "^13.4.35"  v13.4.36`
> Links der Constraint aus der `composer.json`, rechts grau die **tatsächlich installierte** Version aus der `composer.lock`. Das ist ein Inlay-Hint, kein Fehler. `^13.4.35` erlaubt 13.4.36, deshalb updatet Composer auch ohne Änderung an der json.

## 3. Prüfen

```bash
ddev exec vendor/bin/grumphp run     # in manchen Projekten: ddev grumphp run
```

Änderungen anschauen, bevor irgendwas committet wird:

```bash
git status --short
git diff --stat
git diff -- composer.json
git diff --check            # Whitespace-Fehler
```

Lokal Frontend und Backend aufmachen. URLs aus `ddev describe` holen, nicht raten — bei Multi-Site-Projekten stimmt die URL, die ddev beim Start ausgibt, oft nicht.

```bash
ddev describe
ddev typo3 site:list                     # welche Sites gibt es und unter welcher Domain?
ddev typo3 cache:flush ; ddev typo3 site:list
```

Wenn ddev sich komisch verhält:

```bash
ddev stop && ddev start
ddev composer i
```

Leere lokale DB („No site configuration found") → `ddev sync-testing`.

## 4. Commit

```bash
git checkout config/system/settings.php   # ⚠️ siehe Kasten
git status
git add -A
git status
git commit -m "[SECURITY] VRS-502 typo3 updated to version 13.4.36"
git push --set-upstream origin VRS-502-composer-update
```

> [!important] `config/system/settings.php`
> TYPO3 schreibt beim Update die Extension-Konfiguration neu: neue Keys kommen mit Default dazu, verschwundene fliegen raus.
> In **vrs** haben wir die Datei mit `git checkout config/system/settings.php` verworfen — sie gehört dort nicht in den Update-Commit.
> In **SWG** war die Änderung dagegen inhaltlich sinnvoll und kam mit rein (`reduce_duplicate_content` neu, `vhs` entfernt).
> → Also nicht blind: `git diff` anschauen und entscheiden.

> [!tip] `git push` ohne Commit
> gibt `Everything up-to-date` aus und schickt **nichts**. Nach jedem Commit prüfen:
> ```bash
> git log --oneline -2
> ```

## 5. Testing

```bash
git checkout testing
git pull                              # zuerst ziehen, falls testing hinterherhinkt
git merge VRS-502-composer-update
ddev composer i                       # Lock nach dem Merge neu auflösen
git status
git add composer.lock
git commit
git push
```

> [!note] Warum `ddev composer i` nach dem Merge
> Beim Merge treffen zwei `composer.lock` aufeinander. Ein `install` schreibt die Datei konsistent neu — die muss dann mit committet werden.

Der Merge nach `testing` deployt auf den Integrationsserver. Interne Umgebung, der Kunde sieht sie nicht.

> [!warning] Fremde Dateien auf testing
> Hängen auf `testing` Dateien, die nicht zum Update gehören: erst den aktuellen main/master nach `testing` mergen, dann den eigenen Branch.

Danach prüfen:
- Pipeline grün?
- Frontend auf Testing?
- Backend, Seitenbaum, RTE?
- projektspezifisch: Suche (Solr), Formulare, Reservierung

Wenn hier Schluss für heute ist → Ticket auf **Internal Testing**.

## Merge-Regel

> [!important] Auf dem Branch stehen, der sich ändern soll
> ```bash
> git checkout <WOHIN>
> git merge <WAS>
> ```
> Nach dem Merge bleibt man auf dem Branch, auf dem man stand.

| Ich will | Ich stehe auf | Befehl | Danach stehe ich auf |
|---|---|---|---|
| frischen master **in meinen Branch** holen | meinem Branch | `git merge origin/master` | meinem Branch |
| meinen Branch **nach testing** | `testing` | `git merge FAU-1934-composer-update` | `testing` |
| meinen Branch **nach master** (lokal, nur mit Erlaubnis) | `master` | `git merge FAU-1934-composer-update` | `master` |

Ist master weitergelaufen?

```bash
git fetch
git log --oneline <mein-branch>..origin/master    # leer = alles aktuell
```

## 6. Production

Erst nach grünem Testing. Merge nach `main`/`master` = **Deploy auf die Live-Seite des Kunden**.

- vorher prüfen, ob master weitergelaufen ist (siehe Merge-Regel), ggf. `git merge origin/master` + `git push`
- PR vom eigenen Branch nach `main`/`master` — Bitbucket merged auf dem Server, lokal steht man dafür nicht auf master
- im PR rechts prüfen: nur die erwarteten Dateien (meist 2). Mehr → master in testing/Branch fehlt
- Reviewer: bei meinen Projekten fast immer **Johannes Sommer**
- nach dem Merge Frontend und Backend auf Production nachschauen
- lokal nachziehen: `git checkout master && git pull`
- Ticket → **In Review Production**, zugewiesene Person: Johannes

> [!important] Merge-Button nicht still drücken
> Im VRS-Ticket steht ausdrücklich: selbst auf Testing prüfen, dann darf auf Production deployt werden. In anderen Projekten steht das nicht — dann vorher fragen.

---

## Fallen, in die ich schon getappt bin

**`env: 'php': No such file or directory` beim Commit**
Der lokale Git-Hook ruft php auf dem Host auf, php läuft aber nur im ddev-Container. GrumPHP manuell laufen lassen, dann `git commit --no-verify`, und dem Team Bescheid geben.

**`Undefined constant Vaimo\ComposerPatches\Patch\Definition::APPLICABLE`**
`vaimo/composer-patches` updatet sich im selben Lauf selbst: alter Code im Speicher, neue Dateien auf der Platte. Ein zweites `ddev composer i` räumt das auf.

> [!caution] `composer.lock` löschen ist fast immer falsch
> Der Lock hält die exakten Versionen **aller** Pakete fest. Gelöscht → Composer rechnet alles neu, und im Commit landen hunderte unzusammenhängender Änderungen. Das ist keine Reparatur, das ist ein anderer Umfang. Erst `ddev composer i`, Fehler lesen, und nur bewusst und mit Erklärung im PR anders.

**Branch ist hinter main zurückgefallen** → `git merge main` in den eigenen Branch, kein Rebase.

## Was sich je Projekt unterscheidet

| Projekt | Hauptbranch | Testing | Production |
|---|---|---|---|
| SWG | `master` | `testing` | Merge nach `master` |
| Sprungbrett | `main` | `testing` | Merge nach `main` |
| vrs | `master` | `testing` | Merge nach `master` |
| Faulhaber | `master` | `testing` → Env **Test**: `test.faulhaber.wwwserver.net` | PR nach `master` |

> [!note] Faulhaber
> Testing-URL steht im Pipeline-Log, Schritt *Deploy to Testing*, Zeile `rsync … /srv/www/faulhaber/test.faulhaber.wwwserver.net/`.
> Browser-Login (htaccess): Bitwarden → **Faulhaber htaccess (für alle Systeme, mailpit)**. Nicht „DAM Test" — das ist ein anderes System.
> Bitbucket-Environment **Integration** ist seit Mai verwaist — **Test** ist das richtige.

> [!note] Testing sieht anders aus als Live
> Merge synchronisiert **Code**, nicht **Inhalt**. Seiten, Slider, Texte liegen in der DB und in `fileadmin` — jede Umgebung hat ihre eigene. Auf Testing prüfen, **ob es funktioniert**, nicht ob es gleich aussieht. Und beim Vergleichen auf die gleiche Sprache achten (`/de/` vs `/en/`).

Immer nachsehen:

```bash
sed -n '1,60p' bitbucket-pipelines.yml
```

Links: [[andersundsehr]] · [[Git workflow]] · [[Открытые вопросы]]
