# =========================
# Патерн Інтерпретатор (Interpreter)
# =========================
from abc import ABC, abstractmethod

# Інтерфейс виразу
class Expression(ABC):
    @abstractmethod
    def interpret(self, context: dict) -> bool:
        pass

# Конкретні вирази
class PriceLessThan(Expression):
    def __init__(self, price):
        self.price = price

    def interpret(self, context):
        return context.get("price", float('inf')) < self.price

class AuthorIs(Expression):
    def __init__(self, author):
        self.author = author

    def interpret(self, context):
        return context.get("author") == self.author

class YearIs(Expression):
    def __init__(self, year):
        self.year = year

    def interpret(self, context):
        return context.get("year") == self.year

class AndExpression(Expression):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def interpret(self, context):
        return self.expr1.interpret(context) and self.expr2.interpret(context)

# Дані про книги
books = [
    {"title": "Володар Перснів", "author": "Дж. Р. Р. Толкін", "price": 95, "year": 1954},
    {"title": "Гаррі Поттер", "author": "Дж. К. Роулінг", "price": 120, "year": 1997},
    {"title": "1984", "author": "Джордж Орвелл", "price": 80, "year": 1949},
]

# Побудова запиту
query = AndExpression(PriceLessThan(100), AuthorIs("Дж. Р. Р. Толкін"))

# Виконання запиту
for book in books:
    if query.interpret(book):
        print("Знайдена книга:", book["title"])


# =========================
# Патерн Посередник (Mediator)
# =========================

# Базовий інтерфейс посередника
class Mediator(ABC):
    @abstractmethod
    def notify(self, sender, event):
        pass

# Компоненти
class PaymentService:
    def __init__(self, mediator):
        self.mediator = mediator

    def pay(self):
        print("[Оплата] Замовлення оплачено")
        self.mediator.notify(self, "paid")

class DeliveryService:
    def __init__(self, mediator):
        self.mediator = mediator

    def deliver(self):
        print("[Доставка] Замовлення доставлено")

class OrderConfirmation:
    def __init__(self, mediator):
        self.mediator = mediator

    def confirm(self):
        print("[Підтвердження] Замовлення підтверджено")
        self.mediator.notify(self, "confirmed")

# Конкретний посередник
class OrderMediator(Mediator):
    def __init__(self):
        self.payment = PaymentService(self)
        self.delivery = DeliveryService(self)
        self.confirmation = OrderConfirmation(self)

    def notify(self, sender, event):
        if event == "confirmed":
            self.payment.pay()
        elif event == "paid":
            self.delivery.deliver()

# Використання
mediator = OrderMediator()
mediator.confirmation.confirm()


# =========================
# Комбінований приклад: Інтерпретатор + Посередник
# =========================

class OrderContext:
    def __init__(self, delivery_speed, payment_method):
        self.delivery_speed = delivery_speed
        self.payment_method = payment_method

class SpeedIs(Expression):
    def __init__(self, speed):
        self.speed = speed

    def interpret(self, context):
        return context.delivery_speed == self.speed

class PaymentIs(Expression):
    def __init__(self, method):
        self.method = method

    def interpret(self, context):
        return context.payment_method == self.method

class CombinedOrderMediator(Mediator):
    def __init__(self):
        self.payment = PaymentService(self)
        self.delivery = DeliveryService(self)

    def process_order(self, context_expr, context_obj):
        if context_expr.interpret(context_obj):
            print("[Медіатор] Умови замовлення виконано")
            self.payment.pay()

    def notify(self, sender, event):
        if event == "paid":
            self.delivery.deliver()

# Демонстрація
context = OrderContext("express", "credit_card")
expression = AndExpression(SpeedIs("express"), PaymentIs("credit_card"))
combined_mediator = CombinedOrderMediator()
combined_mediator.process_order(expression, context)
