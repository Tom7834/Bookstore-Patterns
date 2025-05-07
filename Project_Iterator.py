# ===============================
# 1. Iterator — Промо-кампанії
# ===============================

class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price

class PromoCampaign:
    def __init__(self, name):
        self.name = name
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def __iter__(self):
        return iter(self._books)

# ===============================
# 2. Iterator + State — Рекомендації
# ===============================

class RecommendationIterator:
    def __init__(self, books):
        self._books = books

    def __iter__(self):
        return iter(self._books)

class UserState:
    def recommend(self, books):
        raise NotImplementedError

class NewUserState(UserState):
    def recommend(self, books):
        return RecommendationIterator([b for b in books if 'popular' in b.title.lower()])

class RegularUserState(UserState):
    def recommend(self, books):
        return RecommendationIterator([b for b in books if 'classic' in b.title.lower()])

class VIPUserState(UserState):
    def recommend(self, books):
        return RecommendationIterator(books)

class User:
    def __init__(self, state):
        self.state = state

    def get_recommendations(self, books):
        return self.state.recommend(books)

# ===============================
# 3. Iterator + State + Chain of Responsibility — Повернення
# ===============================

class BookReturnRequest:
    def __init__(self, book):
        self.book = book
        self.status = "На перевірці"

class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, request):
        if self._next:
            return self._next.handle(request)
        return request

class QualityCheckHandler(Handler):
    def handle(self, request):
        print(f"Перевірка цілісності книги '{request.book.title}'")
        return super().handle(request)

class StockManagerHandler(Handler):
    def handle(self, request):
        print(f"Перевірка актуальності книги '{request.book.title}'")
        return super().handle(request)

class AdminHandler(Handler):
    def handle(self, request):
        print(f"Адміністратор ухвалює рішення по книзі '{request.book.title}'")
        request.status = "Повернено у продаж"
        return request

# ===============================
# Демонстрація роботи
# ===============================
if __name__ == '__main__':
    # 1. Промо-кампанії
    spring = PromoCampaign("Весняний настрій")
    spring.add_book(Book("Весна в Парижі", 120))
    spring.add_book(Book("Квітучий сад", 100))
    print("\n[Промо-кампанія: Весняний настрій]")
    for book in spring:
        print(f"- {book.title} ({book.price} грн)")

    # 2. Рекомендації
    books = [Book("Popular science", 200), Book("Classic tales", 150), Book("Modern love", 180)]
    user = User(NewUserState())
    print("\n[Рекомендації для нового користувача]")
    for book in user.get_recommendations(books):
        print(f"- {book.title}")

    # 3. Повернення книжки
    request = BookReturnRequest(Book("Класика ХХ століття", 130))
    chain = QualityCheckHandler()
    chain.set_next(StockManagerHandler()).set_next(AdminHandler())
    result = chain.handle(request)
    print(f"\n[Результат перевірки повернення]: {result.status}")
