---
tags: [работа, процесс, typo3]
---

# TYPO3 обновление — рабочий процесс

Моя собственная шпаргалка. Шаги общие, но **детали отличаются от проекта к проекту** — ветки, имена деплой-окружений, ревьюеры. Всегда сверяйся с конкретным репозиторием.

## 0. Тикет

- тикет приходит сам (Jira) или задачу говорят устно → **завести тикет себе**
- тикета нет вообще → в репозитории обычно есть заглушка: `SB-0`, `VRS-0`, `AUS-0`
- поставить **In Progress**

Тип апдейта смотри в тикете — от него зависит префикс коммита:
- `Standard Update` → `[UPDATE]`
- `Security Update` → `[SECURITY]`

## 1. Подготовка репозитория

```bash
cd ~/www/project/<проект>
git status                 # чисто? чужие правки → git stash push -m "..."
git switch main            # ⚠️ где-то main, где-то master
git pull
git switch -c VRS-502-typo3-update-13.4.36
```

> [!warning] Проверяй имя главной ветки
> `git branch -a | head` или `remotes/origin/HEAD -> origin/???`
> SWG и vrs → `master`, sprungbrett → `main`.

> [!danger] Незакоммиченные чужие правки
> Они **не принадлежат ветке** и едут за тобой при любом `git switch`. Увидел лишние файлы в `git status` — разберись **до** апдейта, иначе они попадут в коммит.
> `git diff <файл>` → содержательное в stash, пробелы в `git restore`.
> Невидимые отличия: `git diff | cat -A`.

## 2. Обновление

```bash
ddev composer update       # коротко: ddev composer u
```

Необязательно, но по конвенции (так делают в SWG): поднять руками закреплённые констрейнты в `composer.json`, `^13.4.35` → `^13.4.36`. Свободные (`">=13.4.20"`, `"^13"`) не трогать.

```bash
sed -i 's/\^13\.4\.35/^13.4.36/g' composer.json
git diff composer.json     # проверить глазами
```

> [!note] PhpStorm показывает две версии
> `"typo3/cms-core": "^13.4.35"  v13.4.36`
> Слева — констрейнт из `composer.json`, справа серым — что **реально установлено** по `composer.lock`. Это инлей-подсказка, а не рассинхрон. `^13.4.35` разрешает 13.4.36, поэтому composer обновит и без правки json.

## 3. Проверки

```bash
ddev grumphp run                        # где-то: ddev exec vendor/bin/grumphp run
```

Потом открыть **локальный фронт и бэкенд**. URL брать из `ddev describe`, а не придумывать — в мультисайт-проектах адрес, который ddev печатает при старте, может не работать.

Если локальная база пустая («No site configuration found») — `ddev sync-testing`.

## 4. Коммит

```bash
git add -A
git status                 # ожидаем composer.json + composer.lock, иногда config/system/settings.php
git commit -m "[UPDATE] VRS-502 typo3 update v13.4.36"
git push -u origin VRS-502-typo3-update-13.4.36
```

> [!tip] Третий файл — это нормально
> `config/system/settings.php` меняется, когда TYPO3 синхронизирует конфигурацию расширений: новые ключи дописываются с дефолтами, исчезнувшие вычищаются. Посмотреть `git diff`, понять причину и **написать её в описании PR**.

## 5. Testing

```bash
git switch testing         # иногда integration
git pull                   # ⚠️ сначала подтянуть, если testing отстал
git merge VRS-502-typo3-update-13.4.36
git push
```

Мерж в `testing` запускает деплой на интеграционный сервер. Это внутренняя среда, клиент её не видит.

> [!warning] Мусор в testing
> Если на testing висят посторонние файлы — сначала влить в testing актуальный main/master, и только потом своё.

Дальше:
- пайплайн зелёный?
- фронт на Testing открывается?
- бэкенд открывается, редактирование и RTE работают?
- что ещё специфично для проекта: поиск (Solr), формы, бронирование

Прерываешься на другой день → поставить тикету **Internal Testing**.

## 6. Production

Только после зелёного Testing. Merge в `main`/`master` = **деплой на живой сайт клиента**.

- PR из своей ветки в `main`/`master`
- ревьюер: в моих проектах почти всегда **Johannes Sommer**
- после мержа — снова проверить фронт и бэк, уже на проде
- тикет → **In Review Production**, zugewiesene Person: Johannes

> [!important] Кнопку Merge на master не жать молча
> Пока нет апрува и пока не уверен в процессе — спросить. В тикетах VRS прямо написано: протестировать на Testing самому, и тогда можно деплоить. В других проектах такой фразы может не быть.

---

## Грабли, на которые уже наступал

**`env: 'php': No such file or directory` при коммите**
Локальный git-хук зовёт php на хосте, а php живёт только в ddev. GrumPHP прогнать вручную (`ddev grumphp run`), закоммитить с `--no-verify`, сказать команде.

**`Undefined constant Vaimo\ComposerPatches\Patch\Definition::APPLICABLE`**
`vaimo/composer-patches` обновляет сам себя в ходе того же запуска: старый код в памяти, новые файлы на диске. Лечится повторным `ddev composer install`. Если не помогло — пин на старую версию и сообщить команде.

> [!caution] Удалять `composer.lock` — почти всегда неправильно
> Лок фиксирует точные версии **всех** пакетов. Удалил → composer пересчитает всё с нуля, и в коммит поедут сотни несвязанных изменений. Это не «починка», а другой объём работы. Сначала повторный `install`, разбор ошибки, и только в крайнем случае — осознанно и с объяснением в PR.

**`git push` без коммита** → `Everything up-to-date`, и на сервер ничего не уехало. Всегда проверять `git log --oneline -2` после коммита.

**Ветка отстала от main, пока работал** → `git merge main` в свою ветку, не rebase.

## Что отличается между проектами

| | главная ветка | Testing | Production |
|---|---|---|---|
| SWG | `master` | `testing` | merge в `master` |
| Sprungbrett | `main` | `testing` | merge в `main` |
| vrs | `master` | `testing` | merge в `master` |

Проверять всегда: `sed -n '1,60p' bitbucket-pipelines.yml`

Ссылки: [[andersundsehr]] · [[Git workflow]] · [[Открытые вопросы]]
