---
tags: [работа, окружение]
---

# Проект keskin

Клиент — кровельная фирма (Dachdecker, `keskin-bedachungen.de`). Тематика FAQ и контента: Dachsanierung, Flachdach, Sturmschäden.

- Папка: `~/www/project/keskin`
- DDEV-проект: `tetris-test`
- URL: `https://tetris-test.ddev.site`
- Репозиторий: Bitbucket, `andersundsehr/project`
- TYPO3 **14.3.7**

## Команды

```bash
ddev start                      # поднять окружение
ddev composer i                 # зависимости + updateschema + extension setup
ddev yarn install
ddev vite build                 # собрать фронт (ОБЯЗАТЕЛЬНО после новых Tailwind-классов)
ddev vite                       # dev-сервер
ddev typo3 cache:flush
ddev typo3 extension:setup      # если добавил/переименовал поля
ddev playwright test            # тесты
ddev exec vendor/bin/grumphp run  # линтеры (13 задач)
ddev mysql -e "show tables like '%accordion%'"
```

> [!warning] Порядок при проверке
> `git add -A` → потом `grumphp run`. GrumPHP берёт файлы **из индекса**, не с диска. Если удалил файл и не добавил удаление — ругнётся на несуществующий файл.

## Структура пакетов

```
packages/
  aus_project/              общие компоненты (Atom/Molecule/Design)
  components/
  content_element_teaser/
  content_element_text/
  content_element_text_teaser/
  content_element_accordion/   ← мой
  grids/
```

## Генераторы (EXT:aus_make)

```bash
ddev typo3 make:content-element-extension <kebab-name>   # make:cee
ddev typo3 make:fluid-component <extension_key> Molecule/Name   # make:fc
```

- extension_key — это **snake_case имя папки**, не имя компонента
- вставка в терминал может добавить мусор `[200~` — лучше печатать руками

## Tailwind

- v4, собирается через Vite
- **фронтенд**: классы без префикса (`flex`, `px-5`)
- **бэкенд**: с префиксом `tw:` (`tw:flex`)
- ⚠️ в backend-preview моего пакета `tw:`-классы **не применяются вообще** → [[Открытые вопросы]]

Ссылки: [[andersundsehr]] · [[Git workflow]]
