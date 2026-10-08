---
tags: [работа, fluid, компоненты]
---

# Fluid Components и Frontend Studio

Namespace `c:` — Atomic Design: Atom → Molecule → Organism, плюс Element как переходник к TYPO3 ([[Content Blocks]]).

```html
<f:argument name="uid" type="int"/>
<f:argument name="items" type="TYPO3\CMS\Core\Collection\LazyRecordCollection|array"/>
<f:argument name="open" type="bool" optional="true" default="false"/>
```

- `string|Stringable` — для текста из RTE. В фикстуре такие значения пишутся с вложенным `string:`
- `bool` — просто `open: true`, без вложенности

## Frontend Studio

Витрина компонентов. Рендерит компонент **без базы данных**, подставляя данные из фикстуры.

Модуль: Admin → Frontend Studio. Кнопка «Open rendered variant» открывает компонент на отдельной странице (удобно для проверки узкой ширины через Ctrl+Shift+M).

## Цепочка данных

```
фикстура (YAML) → трансформер (PHP) → компонент
```

**Фикстура** — простые значения:
```yaml
variants:
  Default:
    title:
      string: 'Arbeiten Sie auch an Flachdächern?'
    text:
      string: 'Ja. Abdichtung, Dämmung ...'
  Opened:
    title: { string: '...' }
    text: { string: '...' }
    open: true
```

**Трансформер** нужен, когда компонент принимает объекты (например коллекцию `Record`) — такое в YAML не напишешь:

```php
return new ArgumentTransformers(
    items: static function (AccordionItemsSelect $select): array {
        $getRecord = static function (int $uid, string $title, string $text): Record {
            $rawRecord = new RawRecord($uid, 0, [], new ComputedProperties(), 'accordion_items');
            return new Record($rawRecord, [
                'uid' => $uid,
                'accordion_title' => $title,
                'accordion_text' => $text,
            ]);
        };
        // ...
    },
);
```

**Энум** — «пульт»: фикстура не может передать объекты, поэтому передаёт слово, а трансформер по этому слову собирает данные. Плюс строгая типизация и выпадающий список в Studio.

```php
enum AccordionItemsSelect: string
{
    case One = 'one';
    case Three = 'three';
}
```
```yaml
items:
  select: !php/enum Andersundsehr\ContentElementAccordion\Enum\AccordionItemsSelect::Three
```

> [!tip] Имя таблицы для RawRecord
> Узнать реальное: `ddev mysql -e "show tables like '%accordion%'"`.
> При `prefixFields: false` таблица = `accordion_items`, без префикса вендора.
> Ошибка при неверном имени: `No TCA schema exists for the name "..."`

> [!important] Правило
> **Фикстура = объявление теста.** Добавил вариант → появился тест и снапшот. Удалил → исчез.
> Чтобы получить снимок состояния, надо уметь описать это состояние **данными**. «После клика» данными не описать → нужен свой спек ([[Тесты Playwright]]).

После `ddev composer dump-autoload` — иначе новый класс энума не найдётся.

Ссылки: [[andersundsehr]] · [[Тесты Playwright]] · [[Fluid]]
