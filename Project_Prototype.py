from copy import deepcopy

# ----- Патерн "Прототип" -----
class BookPrototype:
    """Базовий клас прототипу книги."""
    def clone(self):
        return deepcopy(self)

class Book(BookPrototype):
    """Клас книги, який підтримує клонування."""
    def __init__(self, title, author, price, genre, isbn):
        self.title = title
        self.author = author
        self.price = price
        self.genre = genre
        self.isbn = isbn
    
    def __str__(self):
        return f"Книга: {self.title}, Автор: {self.author}, Жанр: {self.genre}, Ціна: {self.price}, ISBN: {self.isbn}"

# ----- Патерн "Будівельник" -----
class BookBuilder:
    """Будівельник для покрокового створення книги."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.book = Book(None, None, None, None, None)

    def set_title(self, title):
        self.book.title = title
        return self

    def set_author(self, author):
        self.book.author = author
        return self

    def set_price(self, price):
        self.book.price = price
        return self

    def set_genre(self, genre):
        self.book.genre = genre
        return self

    def set_isbn(self, isbn):
        self.book.isbn = isbn
        return self

    def build(self):
        return self.book

# ----- Використання -----
if __name__ == "__main__":
    # Використання патерну "Будівельник"
    builder = BookBuilder()
    new_book = (builder.set_title("Володар перснів")
                .set_author("Дж. Р. Р. Толкін")
                .set_price(500)
                .set_genre("Фентезі")
                .set_isbn("978-617-12-1234-5")
                .build())
    
    print("Створена книга:")
    print(new_book)
    
    # Використання патерну "Прототип"
    cloned_book = new_book.clone()
    cloned_book.price = 450  # Можна змінити деякі параметри
    
    print("Клонована книга:")
    print(cloned_book)
