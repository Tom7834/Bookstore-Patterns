# 📚 Система управління книжковим магазином  
### Патерни: Ітератор, Стан, Ланцюжок обов’язків

## 🔰 Опис проєкту

Цей проєкт моделює програмне забезпечення для управління функціональністю книжкового магазину. Основна увага приділяється застосуванню шаблонів проєктування для покращення архітектури: **Ітератор (Iterator)**, **Стан (State)** та **Ланцюжок обов’язків (Chain of Responsibility)**. Кожен патерн інтегрується у свій логічний модуль, що відповідає за певний аспект функціонування магазину — від навігації каталогом книжок до обробки клієнтських звернень.

---

### 🔁 1. Динамічна система промо-кампаній (**Ітератор**)

📌 **Опис:**  
Магазин регулярно створює різні промо-кампанії, які орієнтовані на свята, сезони або потреби окремих груп покупців. До кожної кампанії входять добірки книжок з окремими умовами (знижки, подарунки, купони). Ці добірки можуть змінюватись у режимі реального часу.

📌 **Реалізація:**  
- Для кожної кампанії створюється власна колекція книжок, що реалізована як окремий об’єкт, який підтримує ітерацію.
- Можна легко створювати і оновлювати кампанії без зміни основної логіки магазину.
- Наприклад, ітератор кампанії "Весняний настрій" дозволяє переглядати лише ті книжки, які входять до неї.

📌 **Перевага:**  
Гнучкість у формуванні тимчасових колекцій, які можна легко обійти або замінити без перезапуску магазину.

---

### 🔄 2. Відстеження історії замовлень клієнтів (**Стан**)

📌 **Опис:**  
Замовлення у книгарні проходить декілька стадій: від створення до доставки. Важливо відстежувати як поточний стан замовлення, так і мати змогу повертатись до історії змін. Наприклад, замовлення може бути в стані: "Новий", "Очікує оплати", "Оплачено", "Обробляється", "Доставлено", "Завершено", "Скасовано".

📌 **Реалізація:**  
- Кожен стан представлений як окремий об'єкт зі своєю поведінкою.
- Переходи між станами дозволяють системі динамічно реагувати на зміну ситуації.
- Система дозволяє повернутись до попереднього стану або повторити дії.

📌 **Перевага:**  
Зміни стану ізольовані й легко розширювані. Наприклад, додати новий стан "На перетримці складу" можна без переписування всієї системи.

---

### 🧾 3. Верифікація повернень і скарг (**Ланцюжок обов’язків**)

📌 **Опис:**  
У клієнтів можуть виникати різні типи запитів: питання про товар, скарги, запити на повернення або прохання до керівництва. Ці запити потрібно обробляти з урахуванням важливості та ролей відповідальних осіб.

📌 **Реалізація:**  
- Ланцюжок обробників побудований так, що кожен обробник перевіряє, чи може він відповісти на запит.
- Якщо ні — запит передається наступному в ланцюгу.
- Наприклад, чат-бот може обробити лише загальні питання, менеджер — повернення, а адміністратор — виняткові випадки.

📌 **Перевага:**  
Універсальний механізм маршрутизації запитів без дублювання логіки в кожному обробнику.

---

### 📌 4. Підбір персональних рекомендацій (**Ітератор + Стан**)

📌 **Опис:**  
Система має формувати динамічні персональні добірки книжок, які змінюються в залежності від поточної активності користувача. Наприклад, для новачків система показує популярні книги, а для постійних — добірки на основі куплених раніше.

📌 **Реалізація:**  
- Ітератор обирає книжки за категоріями (жанри, автори, інтереси).
- Стан користувача (новий, постійний, VIP) впливає на фільтрацію рекомендацій.
- Комбінований підхід дозволяє гнучко адаптувати рекомендації під конкретну поведінку.

📌 **Перевага:**  
Індивідуальний підхід до кожного клієнта, який дозволяє підвищити лояльність і обсяг продажів.

---

### 📌 5. Запуск масових повідомлень про акції та доставку (**Ланцюжок обов’язків**)

📌 **Опис:**  
Магазин надсилає клієнтам повідомлення: про акції, знижки, підтвердження доставок, зміни статусу замовлень. Кожен тип повідомлення повинен мати відповідального обробника.

📌 **Реалізація:**  
- Повідомлення проходить через ланцюжок служб, які можуть змінити або доповнити його.
- Наприклад, маркетинг додає акційну інформацію, логістика — дату доставки, фінанси — квитанцію.

📌 **Перевага:**  
Універсальна система повідомлень, яку легко масштабувати на нові типи інформації без переписування коду.

---

### 📌 6. Агрегація книжок із зовнішніх джерел (**Ітератор**)

📌 **Опис:**  
Книжковий магазин може підключати зовнішні постачальники, що надають каталоги у різних форматах (API, CSV, XML). Система повинна надати клієнту єдиний уніфікований каталог.

📌 **Реалізація:**  
- Для кожного постачальника створюється свій адаптер з власним ітератором.
- Всі ітератори об'єднуються в загальний об'єкт агрегації.
- Клієнт переглядає книжки як єдиний список, не знаючи про джерело.

📌 **Перевага:**  
Система легко масштабується, додаючи нові джерела, і не вимагає переробки логіки виводу книжок.

---

### 📌 7. Повернення і повторне включення книжки в продаж (**Стан + Ланцюжок обов’язків**)

📌 **Опис:**  
Після повернення книжка повинна пройти огляд, щоб визначити подальшу долю: повторний продаж, утилізація або передача до благодійності. Кожен етап має власного відповідального.

📌 **Реалізація:**  
- Книжка після повернення отримує стан "На перевірці".
- Далі вона проходить по ланцюгу: оператор перевіряє цілісність, менеджер складу — актуальність, адміністратор — остаточне рішення.
- Після завершення перевірки книжці присвоюється новий стан: "Повернено у продаж" або "Вибраковано".

📌 **Перевага:**  
Автоматизоване управління поверненням без втрати контролю, з фіксацією кожного етапу прийняття рішення.

---

## ✅ Висновок

Усі додаткові функції створюють комплексну систему управління, де ітератори забезпечують універсальний доступ до колекцій, патерн Стан дозволяє відстежувати поведінку об’єктів у часі, а Ланцюжок обов’язків реалізує гнучке делегування завдань. Це робить архітектуру системи масштабованою, стабільною та адаптивною до змін.

---


