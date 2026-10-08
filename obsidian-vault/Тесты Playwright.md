---
tags: [работа, тесты]
---

# Тесты Playwright

## Зачем вообще тесты

Тест пишется **не** ради известного бага — известный баг надо чинить. Тест фиксирует **требование**, чтобы оно не сломалось через полгода, когда другой человек правит соседний код и не знает, что аккордеон обязан открываться с клавиатуры.

Не тестировать всё подряд. Плохой тест хуже отсутствующего: падает от мелочей, его чинят не глядя, потом отключают.

## Два вида файлов

| Файл | Движок | Где исполняется |
|---|---|---|
| `*.spec.ts` | Playwright | настоящий браузер |
| `*.test.ts` | Vitest | Node, без браузера |

## Откуда берутся снапшоты

Тесты **не лежат файлами**. Их создаёт на лету

```
packages/aus_project/Components/all-components.spec.ts
```

→ проходит по всем фикстурам → для каждого варианта объявляет тест → зовёт `snapshotTest()` из
`vendor/andersundsehr/frontend_studio/Playwright/src/snapshotTest.ts`

Внутри **пять проверок**:

1. HTTP 200 от превью-эндпоинта
2. `toMatchAriaSnapshot()` → `.aria.yml` — дерево доступности
3. `toHaveScreenshot()` → `.png` — пиксели
4. `logging.assertEmpty()` — консоль браузера чистая (`*.consoleignore`)
5. `checkAccessibility()` → **axe-core**, промышленный аудит доступности (`*.accessibilityignore`)

> [!note] Доступность тестируется автоматически
> axe проверяет контраст, alt, вложенность заголовков, конфликты ARIA. Это сильный аргумент для PR.

Имена файлов: `c-molecule-accordionItem-Opened-1-chromium-linux.png`
`chromium-linux` — снимки платформозависимы, поэтому CI и локалка должны быть на одном образе.

## Команды

```bash
ddev playwright test
ddev playwright test --grep "accordion"
ddev playwright test --update-snapshots    # принять текущий вид как эталон
```

> [!tip] Когда нужен --update-snapshots
> Только когда тест упал на `toMatchAriaSnapshot` или `toHaveScreenshot` **и ты согласен**, что новое состояние правильное. Во всех остальных случаях — обычный прогон.
>
> «A snapshot doesn't exist … writing actual» на первом прогоне — не ошибка, а «эталона ещё нет, записал».

> [!warning] Снапшоты-сироты
> Playwright **не удаляет** ненужные снимки. Убрал вариант или тест → зайди в папку `-snapshots` и подчисти руками.

## Свой спек

```ts
import { expect, test } from '@playwright/test';
import { getUrlForVariant } from '@frontend_studio/test';

const answer = 'Ja. Abdichtung, Dämmung ...';   // должно совпадать с фикстурой

test('answer is hidden until the item is opened', async ({ page }) => {
  await page.goto(getUrlForVariant('Default'));
  await expect(page.getByText(answer)).toBeHidden();      // ← без этого тест бессмыслен
  await page.locator('summary').click();
  await expect(page.getByText(answer)).toBeVisible();
  await page.locator('summary').click();
  await expect(page.getByText(answer)).toBeHidden();
});

test('item can be opened with keyboard', async ({ page }) => {
  await page.goto(getUrlForVariant('Default'));
  await page.locator('summary').focus();
  await expect(page.locator('summary')).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByText(answer)).toBeVisible();
});
```

- `await` перед каждой строкой — забудешь, тест будет падать случайным образом
- каждый тест получает **чистую вкладку**, поэтому `goto` нужен в каждом
- `.focus()` вместо Tab: проверяет, что элемент **способен принять фокус** (у `<div>` без tabindex не выйдет), и не ломается от обвязки Studio
- `.first()` если на странице несколько `summary`

## ⚠️ Нерешённое: свои скриншоты

`toHaveScreenshot()` в собственном спеке сохраняет снимок **в чужой пакет** — у меня улетало в `content_element_text/Slotter` и `content_element_text_teaser/TextTeaser`.

Причина: `setSnapshotPathTemplate` объявлен локально в `snapshotTest.ts` (строка 54), не экспортируется, и лезет в приватный API Playwright:
```ts
(test.info() as unknown as {_projectInternal: {...}})._projectInternal.snapshotPathTemplate = ...
```
Мой спек эту строку не вызывает → наследует путь последнего протестированного компонента.

**Обход, который сработал:** добавить компоненту аргумент `open`, завести вариант фикстуры `Opened` — и штатная автоматика снимет его сама, без хаков.

→ [[Открытые вопросы]]

Ссылки: [[andersundsehr]] · [[Fluid Components и Frontend Studio]]
