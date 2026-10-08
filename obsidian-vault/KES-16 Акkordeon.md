---
tags: [работа, тикет]
статус: в ревью
---

# KES-16 — Akkordeon / FAQ Element

Ветка `KES-16-akkordeon` · Jira: «Akkordeon / FAQ Element»

## Что это

Контент-элемент FAQ: список записей, у каждой заголовок (вопрос) и RTE-текст (ответ). Дизайн — серые плашки стопкой, шеврон справа. Контейнер/max-width пока игнорируем, элемент на всю ширину.

## Решения

- **Нативный `<details>`/`<summary>`** вместо ARIA-паттерна → [[Барьерефрайхайт]]
- `group:` не указан → элемент в «Typical page content»
- Site Set `andersundsehr/accordion` добавлен в `config/sites/main/config.yaml`
- Иконка: `content-accordion` из ядра TYPO3
  ```bash
  cp vendor/typo3/cms-core/Resources/Public/Icons/T3Icons/svgs/content/content-accordion.svg \
     packages/content_element_accordion/ContentBlocks/ContentElements/accordion/assets/icon.svg
  ```
- `[overflow-wrap:anywhere]` на `<summary>` — иначе длинное немецкое слово обрезается
- `hyphens-auto` **убран**: с `anywhere` не работает никогда (anywhere вмешивается в расчёт min-width и выигрывает). Альтернатива — `min-w-0` на флекс-элемент + `break-word`, но это возня ради косметики

## Файлы

```
Classes/Enum/AccordionItemsSelect.php          One | Three
Components/Element/Accordion/
  Accordion.fluid.html                         div + f:for → c:molecule.accordionItem
  Accordion.fixture.yaml                       Default (Three), SingleItem (One)
  Accordion.transformer.php                    собирает Record для таблицы accordion_items
Components/Molecule/AccordionItem/
  AccordionItem.fluid.html                     details/summary, аргумент open
  AccordionItem.fixture.yaml                   Default, LongText, LongWord, Opened
  AccordionItem.spec.ts                        клик + клавиатура
ContentBlocks/ContentElements/accordion/
  templates/frontend.fluid.html
  templates/backend-preview.fluid.html
  language/labels.xlf, de.labels.xlf
  assets/icon.svg
  config.yaml
```

## Ревью (PR в Bitbucket)

| Пункт | Кто | Статус |
|---|---|---|
| Перенести в `Organism/Accordion` | Kevin | ❌ отозвано, Element остаётся |
| Больше вариантов фикстуры (короткий / длинный / длинное слово) | Matthias | ✅ |
| Реальные тексты вместо Lorem | Matthias | ✅ FAQ кровельщика |
| Вариант с `None` или убрать из энума | Matthias | ✅ убран `None` — `minitems: '1'` не даёт пустого состояния |
| backend-preview: `f:render.text` | Matthias | ✅ |
| Скриншоты открытого состояния | Matthias | ⏳ сделал через вариант `Opened`, вопрос про `toHaveScreenshot` открыт |

## Находка дня

`tw:`-классы в backend-preview этого пакета **не применяются**: ни `line-clamp-1`, ни `opacity-70`. Без них выглядит идентично. Мёртвые классы убрал. → [[Открытые вопросы]]

Ссылки: [[andersundsehr]] · [[Content Blocks]] · [[Тесты Playwright]]
