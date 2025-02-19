from abc import ABC, abstractmethod

# Абстрактний клас книги
class Book(ABC):
    def __init__(self, title: str, author: str, price: float):
        self.title = title
        self.author = author
        self.price = price

    @abstractmethod
    def get_info(self) -> str:
        pass

# Конкретні класи книг
class FictionBook(Book):
    def get_info(self) -> str:
        return f'Художня книга: "{self.title}" - {self.author}, ${self.price:.2f}'

class ScienceBook(Book):
    def get_info(self) -> str:
        return f'Наукова книга: "{self.title}" - {self.author}, ${self.price:.2f}'

# Абстрактна фабрика
class BookFactory(ABC):
    @abstractmethod
    def create_book(self, title: str, author: str, price: float) -> Book:
        pass

# Конкретні фабрики
class FictionBookFactory(BookFactory):
    def create_book(self, title: str, author: str, price: float) -> Book:
        return FictionBook(title, author, price)

class ScienceBookFactory(BookFactory):
    def create_book(self, title: str, author: str, price: float) -> Book:
        return ScienceBook(title, author, price)

# Використання фабричного методу
if __name__ == "__main__":
    fiction_factory = FictionBookFactory()
    science_factory = ScienceBookFactory()

    book1 = fiction_factory.create_book("1984", "Джордж Орвелл", 12.99)
    book2 = science_factory.create_book("Коротка історія часу", "Стівен Хокінг", 15.50)

    print(book1.get_info())
    print(book2.get_info())
