# Рівень 1: Декоратор і Адаптер

# === ДЕКОРАТОР ===
class Order:
    def __init__(self, book_title):
        self.book_title = book_title

    def get_description(self):
        return f"Book: {self.book_title}"

    def get_cost(self):
        return 100

class OrderDecorator(Order):
    def __init__(self, base_order):
        self.base_order = base_order

    def get_description(self):
        return self.base_order.get_description()

    def get_cost(self):
        return self.base_order.get_cost()

class GiftWrap(OrderDecorator):
    def get_description(self):
        return self.base_order.get_description() + ", with gift wrap"

    def get_cost(self):
        return self.base_order.get_cost() + 20

class Autograph(OrderDecorator):
    def get_description(self):
        return self.base_order.get_description() + ", with autograph"

    def get_cost(self):
        return self.base_order.get_cost() + 50

# === АДАПТЕР ===
class PayPalAPI:
    def send_payment(self, amount):
        print(f"PayPal: paid {amount} UAH")

class LiqPayAPI:
    def make_transaction(self, sum_hryvnia):
        print(f"LiqPay: paid {sum_hryvnia} UAH")

class PaymentAdapter:
    def __init__(self, payment_service, method_name):
        self.payment_service = payment_service
        self.method_name = method_name

    def pay(self, amount):
        if self.method_name == "paypal":
            self.payment_service.send_payment(amount)
        elif self.method_name == "liqpay":
            self.payment_service.make_transaction(amount)


# Рівень 2: Facade, Proxy, Bridge

# === ФАСАД ===
class Inventory:
    def check_stock(self, title):
        return True

class Billing:
    def create_invoice(self, title):
        print(f"Invoice created for: {title}")

class StockManager:
    def reduce_stock(self, title):
        print(f"Stock reduced for: {title}")

class BookOrderFacade:
    def __init__(self):
        self.inventory = Inventory()
        self.billing = Billing()
        self.stock = StockManager()

    def order_book(self, title):
        if self.inventory.check_stock(title):
            self.billing.create_invoice(title)
            self.stock.reduce_stock(title)
            print("Order completed")

# === ПРОКСІ ===
class BookDatabase:
    def get_book_info(self, title):
        print(f"Fetching real info for: {title}")
        return f"Real info about {title}"

class BookDatabaseProxy:
    def __init__(self):
        self.db = BookDatabase()
        self.cache = {}

    def get_book_info(self, title):
        if title not in self.cache:
            self.cache[title] = self.db.get_book_info(title)
        else:
            print(f"Cache hit for: {title}")
        return self.cache[title]

# === МІСТ ===
class BookDisplay:
    def __init__(self, renderer):
        self.renderer = renderer

    def show(self, title):
        self.renderer.render(title)

class WebRenderer:
    def render(self, title):
        print(f"Web View: {title}")

class PDFRenderer:
    def render(self, title):
        print(f"PDF Document: {title}")

class MobileRenderer:
    def render(self, title):
        print(f"Mobile View: {title}")

# ==== Тестування ====
if __name__ == "__main__":
    # Декоратор
    order = Order("1984 by Orwell")
    order = GiftWrap(order)
    order = Autograph(order)
    print(order.get_description())
    print(f"Total cost: {order.get_cost()} UAH")

    # Адаптер
    paypal = PayPalAPI()
    adapter1 = PaymentAdapter(paypal, "paypal")
    adapter1.pay(120)

    liqpay = LiqPayAPI()
    adapter2 = PaymentAdapter(liqpay, "liqpay")
    adapter2.pay(150)

    # Фасад
    facade = BookOrderFacade()
    facade.order_book("The Hobbit")

    # Проксі
    proxy = BookDatabaseProxy()
    print(proxy.get_book_info("Dune"))
    print(proxy.get_book_info("Dune"))

    # Міст
    display_web = BookDisplay(WebRenderer())
    display_web.show("Brave New World")

    display_pdf = BookDisplay(PDFRenderer())
    display_pdf.show("Brave New World")
