---
tags: [работа, typo3]
---

# Content Blocks

Структура контент-элемента:

```
packages/content_element_<name>/
  Classes/
  Components/
    Element/<Name>/          ← переходник к TYPO3
    Molecule/<Name>Item/     ← переиспользуемая часть
  ContentBlocks/ContentElements/<name>/
    assets/icon.svg
    language/labels.xlf
    language/de.labels.xlf
    templates/frontend.fluid.html
    templates/backend-preview.fluid.html
    config.yaml
```

## Element vs Organism

> [!quote] Matthias
> Ein Content element hat z.B. immer eine `id="c{uid}"`, ein Organism nicht.

- **Element** — знает про TYPO3: `uid`, поля записи, якорь `id="c{uid}"`. Остаётся всегда.
- **Organism** — чистая презентация, ничего не знает про CMS. Выносить туда стоит, только если компонент нужен в нескольких местах.

## config.yaml

```yaml
name: andersundsehr/accordion
typeName: andersundsehr-accordion
title: andersundsehr/accordion
description: '...'
prefixFields: false        # → таблица называется accordion_items, без префикса
fields:
  - identifier: accordion_items
    type: Collection
    label: 'Accordion Items'
    fields:
      - identifier: accordion_title
        type: Text
        required: true
      - identifier: accordion_text
        type: Textarea
        enableRichtext: true
        richtextConfiguration: default
    maxitems: '10'
    minitems: '1'
```

- `labelField` по умолчанию = первое поле
- нет строки `group:` → элемент попадает в **«Typical page content»** (default). Так сделано у text, text-teaser, textmedia
- у тизера исторически `group: camino_teaser` — отдельная вкладка, скорее всего недосмотр

> [!important] Site Set — нет в документации
> Content Blocks создаёт для каждого элемента **Site Set** с именем `vendor/name`. Пока не добавишь его в `config/sites/main/config.yaml` → `dependencies`, элемент **не появится** в мастере «New Content».
> ```yaml
> dependencies:
>   - andersundsehr/teaser
>   - andersundsehr/accordion
> ```

## Переводы

Только для **бэкенда**: название элемента, описание, подписи полей. Контент на сайте вводит редактор.

- `labels.xlf` — английский, только `<source>`
- `de.labels.xlf` — `<source>` + `<target>`, в теге `<file>` добавляется `target-language="de"`
- нет `<target>` → TYPO3 показывает `<source>`
- подписи ядра («General», «Type») — из языкового пакета TYPO3, он в проекте не установлен, поэтому они английские

> [!warning] Генератор не чистит мусор
> При переименовании полей старые ключи остаются в `labels.xlf` (у меня накопилось 27 мёртвых). Удалять руками.
> То же с таблицами в БД: `andersundsehr_accordion_Collection_0` остался от удалённого Basic Headline.

Ссылки: [[andersundsehr]] · [[Fluid]] · [[KES-16 Акkordeon]]
