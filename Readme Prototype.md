🔹 Перший рівень: Реалізація патерна "Прототип"

📌 Опис

Патерн "Прототип" дозволяє створювати копії об'єктів без прив'язки до конкретних класів. Це корисно для збереження стану об'єкта та швидкого створення нових екземплярів.

📝 Код
```
import copy

class BookPrototype:
    """ Прототип книги """
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def clone(self):
        return copy.deepcopy(self)

    def get_info(self):
        return f'Книга: "{self.title}" - {self.author}, ${self.price:.2f}'
```
# Створення книги
original_book = BookPrototype("1984", "Джордж Орвелл", 12.99)

# Клонування книги
cloned_book = original_book.clone()
cloned_book.price = 9.99  # Зміна ціни для клонованого екземпляра

# Виведення інформації
print(original_book.get_info())
print(cloned_book.get_info())

🔍 Пояснення коду

BookPrototype — базовий клас книги з атрибутами: назва, автор, ціна.

Метод clone() — створює копію об'єкта за допомогою copy.deepcopy().

Зміна price у cloned_book демонструє незалежність клонів.

Виведення результату:

Книга: "1984" - Джордж Орвелл, $12.99
Книга: "1984" - Джордж Орвелл, $9.99

🔹 Другий рівень: Декомпозиція завдання з використанням "Прототипа"

📌 Опис

В рамках цього рівня ми виділяємо окремі модулі:

BookPrototype для збереження та клонування книг

Catalog для управління колекцією книг

📝 Код
```
class Catalog:
    """ Каталог книг """
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def list_books(self):
        return [book.get_info() for book in self.books]
```
# Використання
catalog = Catalog()
catalog.add_book(original_book)
catalog.add_book(cloned_book)

for book in catalog.list_books():
    print(book)

🔹 Третій рівень: Використання патернів "Прототип" та "Будівельник"

📌 Опис

Патерн "Будівельник" дозволяє поетапно створювати складні об'єкти, забезпечуючи гнучкість конфігурації книг.

📝 Код
```
class BookBuilder:
    """ Будівельник для створення книги """
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._book = BookPrototype("", "", 0.0)
    
    def set_title(self, title):
        self._book.title = title
        return self
    
    def set_author(self, author):
        self._book.author = author
        return self
    
    def set_price(self, price):
        self._book.price = price
        return self
    
    def build(self):
        book = self._book
        self.reset()
        return book
```
# Використання будівельника
builder = BookBuilder()
new_book = builder.set_title("Гаррі Поттер").set_author("Дж. Роулінг").set_price(20.99).build()

print(new_book.get_info())

🔍 Пояснення коду

BookBuilder дозволяє поетапно задавати атрибути книги.

Метод reset() створює новий об'єкт книги.

Ланцюжковий виклик (set_title().set_author().set_price()) дозволяє легко конфігурувати об'єкт.

Вивід результату:

Книга: "Гаррі Поттер" - Дж. Роулінг, $20.99

🔹 Висновки

Ця лабораторна робота продемонструвала:

Використання патерна "Прототип" для клонування книг

Використання патерна "Будівельник" для створення конфігурованих об'єктів

Декомпозицію завдання для спрощення управління каталогом книг

🚀 Проєкт став гнучким та розширюваним, що дозволяє легко змінювати та масштабувати функціонал!
