---
tags: [работа, fluid]
---

# Fluid

## Грабли, на которые наступал

> [!danger] Фигурные скобки всегда вычисляются
> `{accordion_title}` — это **переменная**, даже внутри кавычек. Если нужно имя поля строкой — пиши без скобок:
> ```html
> {item -> f:render.text(field: 'accordion_title')}
> ```
> Ошибка при путанице: `get(): Argument #1 must be string, null given`

- `f:for` — это ViewHelper, у него только аргументы `each`, `as`, `key`, `reverse`, `iteration`. Класс туда не передать → ошибка `Undeclared arguments passed to ForViewHelper: class`. Класс вешай на обёртку.
- `&lt;` — чтобы вывести literal `<`
- пространства имён объявляются в `<html>`:
  ```html
  <html
    xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
    xmlns:ausProject="http://typo3.org/ns/Andersundsehr/AusProject/ViewHelpers"
  >
  ```
  Без `xmlns:f` IDE ругается «Namespace 'f' is not bound» на инлайн-записи `{f:if(...)}`

## Булев HTML-атрибут

> [!warning] `open="false"` ТОЖЕ раскрывает
> Булевы атрибуты (`open`, `disabled`, `checked`) срабатывают от самого факта присутствия. Писать `open="{open}"` нельзя.
> Правильно — подставлять **сам атрибут** как текст:
> ```html
> <details class="group" {f:if(condition: open, then: 'open')}>
> ```

## Вывод RTE-текста

```html
{item -> f:render.text(field: 'accordion_text')}        <!-- с форматированием -->
{item.accordion_text -> f:format.stripTags() -> f:format.htmlentitiesDecode()}  <!-- голый текст -->
```

- `f:render.text` отдаёт готовый HTML (`<p>`, `<ul>`, `<a>`) — выглядит лучше
- ⚠️ при этом `line-clamp` перестаёт работать: обрезка по строкам не достаёт до вложенного `<p>`

## ViewHelper-ы принимают только свои аргументы

```
Undeclared arguments passed to ViewHelper SvgInlineViewHelper: aria-hidden.
Valid arguments are: path, class
```

Нужен произвольный атрибут → оберни в обычный HTML-тег:
```html
<span aria-hidden="true" class="shrink-0">
  <ausProject:svgInline path="..." class="..."/>
</span>
```

Ссылки: [[andersundsehr]] · [[Content Blocks]] · [[Fluid Components и Frontend Studio]]
