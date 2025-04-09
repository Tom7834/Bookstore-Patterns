# Патерн Стратегія (Strategy)
from abc import ABC, abstractmethod

# Інтерфейс для стратегії оплати
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Конкретні стратегії
class CreditCardPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Оплата карткою на суму {amount} гривень.")

class PayPalPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Оплата через PayPal на суму {amount} гривень.")

class CashOnDeliveryPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Оплата при отриманні на суму {amount} гривень.")

class CryptoPayment(PaymentStrategy):
    def process_payment(self, amount):
        print(f"Оплата криптовалютою на суму {amount} гривень.")

# Клас для кошика покупок
class ShoppingCart:
    def __init__(self, payment_strategy: PaymentStrategy):
        self.payment_strategy = payment_strategy
    
    def checkout(self, amount):
        self.payment_strategy.process_payment(amount)

# Використання Стратегії
cart = ShoppingCart(CreditCardPayment())
cart.checkout(500)  # Оплата карткою на суму 500 гривень.

# -------------------------------------------------------

# Патерн Спостерігач (Observer)
from abc import ABC, abstractmethod

# Інтерфейс для спостерігача
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# Спостерігачі
class EmailNotifier(Observer):
    def update(self, message):
        print(f"Email: {message}")

class SMSNotifier(Observer):
    def update(self, message):
        print(f"SMS: {message}")

class PushNotifier(Observer):
    def update(self, message):
        print(f"Push: {message}")

# Суб'єкт для сповіщень
class NotificationService:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

# Використання Спостерігача
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()
push_notifier = PushNotifier()

notification_service = NotificationService()
notification_service.subscribe(email_notifier)
notification_service.subscribe(sms_notifier)
notification_service.subscribe(push_notifier)

notification_service.notify("Ваше замовлення було відправлено!")

# -------------------------------------------------------

# Патерн Команда (Command)
from abc import ABC, abstractmethod

# Інтерфейс для команди
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Конкретні команди
class AddBookCommand(Command):
    def __init__(self, catalog, book):
        self.catalog = catalog
        self.book = book

    def execute(self):
        self.catalog.append(self.book)
        print(f"Книга '{self.book['title']}' додана в каталог.")

    def undo(self):
        self.catalog.remove(self.book)
        print(f"Книга '{self.book['title']}' видалена з каталогу.")

class UpdatePriceCommand(Command):
    def __init__(self, book, new_price):
        self.book = book
        self.old_price = book['price']
        self.new_price = new_price

    def execute(self):
        self.book['price'] = self.new_price
        print(f"Ціна книги '{self.book['title']}' оновлена на {self.new_price} гривень.")

    def undo(self):
        self.book['price'] = self.old_price
        print(f"Ціна книги '{self.book['title']}' відновлена на {self.old_price} гривень.")

# Клас для адміністратора
class Admin:
    def __init__(self):
        self.history = []

    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)

    def undo_command(self):
        if self.history:
            command = self.history.pop()
            command.undo()

# Використання Команди
book = {'title': 'Python для початківців', 'price': 250}
catalog = []

add_book_command = AddBookCommand(catalog, book)
update_price_command = UpdatePriceCommand(book, 300)

admin = Admin()
admin.execute_command(add_book_command)  # Додавання книги
admin.execute_command(update_price_command)  # Оновлення ціни

# Відміна останньої команди
admin.undo_command()  # Відновлення ціни
admin.undo_command()  # Видалення книги
