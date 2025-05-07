# 📦 Клас Книга
class Book:
    def __init__(self, title, genre, price):
        self.title = title
        self.genre = genre
        self.price = price

    def accept(self, visitor):
        visitor.visit_book(self)


# 🧑‍💼 Клас Клієнт
class Customer:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def accept(self, visitor):
        visitor.visit_customer(self)


# 🧾 Клас Замовлення
class Order:
    def __init__(self, customer, books):
        self.customer = customer
        self.books = books

    def accept(self, visitor):
        visitor.visit_order(self)


# 📦 Клас Кошика з Memento
class Cart:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)

    def create_memento(self):
        return CartMemento(self.books[:])

    def restore(self, memento):
        self.books = memento.get_state()


class CartMemento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state[:]


class CartHistory:
    def __init__(self):
        self.history = []

    def save(self, memento):
        self.history.append(memento)

    def undo(self):
        if self.history:
            return self.history.pop()
        return None


# ⚙️ Налаштування користувача з Memento
class UserSettings:
    def __init__(self, theme, language):
        self.theme = theme
        self.language = language

    def change_settings(self, theme, language):
        self.theme = theme
        self.language = language

    def create_memento(self):
        return SettingsMemento(self.theme, self.language)

    def restore(self, memento):
        self.theme = memento.theme
        self.language = memento.language


class SettingsMemento:
    def __init__(self, theme, language):
        self.theme = theme
        self.language = language


# 🧠 Патерн Відвідувач
class Visitor:
    def visit_book(self, book):
        pass

    def visit_customer(self, customer):
        pass

    def visit_order(self, order):
        pass


# 📊 Відвідувач для аналітики
class SalesAnalyticsVisitor(Visitor):
    def __init__(self):
        self.genre_count = {}
        self.customer_activity = {}
        self.total_revenue = 0

    def visit_book(self, book):
        self.genre_count[book.genre] = self.genre_count.get(book.genre, 0) + 1
        self.total_revenue += book.price

    def visit_customer(self, customer):
        self.customer_activity[customer.name] = len(customer.orders)

    def visit_order(self, order):
        for book in order.books:
            book.accept(self)


# 📄 Відвідувач для генерації звітів
class ReportVisitor(Visitor):
    def visit_book(self, book):
        print(f"Книга: {book.title}, Жанр: {book.genre}, Ціна: {book.price}")

    def visit_customer(self, customer):
        print(f"Клієнт: {customer.name}, Кількість замовлень: {len(customer.orders)}")

    def visit_order(self, order):
        print(f"Замовлення клієнта: {order.customer.name}, Кількість книг: {len(order.books)}")
        for book in order.books:
            book.accept(self)


# ✅ Приклад використання
if __name__ == "__main__":
    # Книги та клієнти
    book1 = Book("1984", "Дистопія", 300)
    book2 = Book("Гаррі Поттер", "Фентезі", 400)
    book3 = Book("Чарлі і шоколадна фабрика", "Дитяча", 250)

    customer = Customer("Олег")
    cart = Cart()
    cart_history = CartHistory()

    # Додавання книг до кошика
    cart.add_book(book1)
    cart_history.save(cart.create_memento())

    cart.add_book(book2)
    cart_history.save(cart.create_memento())

    cart.remove_book(book1)
    cart_history.save(cart.create_memento())

    # Відкат стану
    cart.restore(cart_history.undo())

    # Налаштування користувача
    settings = UserSettings("Світла", "UA")
    backup = settings.create_memento()
    settings.change_settings("Темна", "EN")
    settings.restore(backup)

    # Замовлення
    order = Order(customer, cart.books[:])
    customer.add_order(order)

    # Відвідувачі
    analytics = SalesAnalyticsVisitor()
    report = ReportVisitor()

    order.accept(analytics)
    customer.accept(analytics)

    order.accept(report)
    customer.accept(report)

    print("Аналітика за жанрами:", analytics.genre_count)
    print("Активність клієнтів:", analytics.customer_activity)
    print("Загальний прибуток:", analytics.total_revenue)