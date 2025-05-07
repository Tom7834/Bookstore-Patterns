from abc import ABC, abstractmethod
from typing import List, Dict

# -------------------- Базові інтерфейси та класи --------------------
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class MacroCommand(Command):
    def __init__(self, commands: List[Command]):
        self.commands = commands
        
    def execute(self):
        for command in self.commands:
            command.execute()
            
    def undo(self):
        for command in reversed(self.commands):
            command.undo()

class ReportTemplate(ABC):
    def generate_report(self):
        """Шаблонний метод - визначає структуру генерації звіту"""
        self.collect_data()
        self.analyze_data()
        report = self.format_report()
        self.send_report(report)
        return report
    
    @abstractmethod
    def collect_data(self):
        pass
    
    @abstractmethod
    def analyze_data(self):
        pass
    
    @abstractmethod
    def format_report(self):
        pass
    
    def send_report(self, report):
        print(f"\n[Відправка звіту]\n{report}\n")

# -------------------- Модуль управління книгами --------------------
class Book:
    def __init__(self, id: int, title: str, author: str, price: float, quantity: int):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.title} ({self.author}) - ${self.price} | {self.quantity} шт."

class BookCatalog:
    def __init__(self):
        self.books = {}
        
    def add_book(self, book: Book):
        self.books[book.id] = book
        print(f"Додано книгу: {book.title}")
        
    def update_book(self, book_id: int, **kwargs):
        if book_id in self.books:
            book = self.books[book_id]
            for key, value in kwargs.items():
                setattr(book, key, value)
            print(f"Оновлено книгу ID {book_id}: {kwargs}")
                
    def remove_book(self, book_id: int):
        if book_id in self.books:
            book = self.books[book_id]
            del self.books[book_id]
            print(f"Видалено книгу: {book.title}")
            
    def get_book(self, book_id: int) -> Book:
        return self.books.get(book_id)
    
    def check_stock(self, book_id: int, quantity: int) -> bool:
        book = self.get_book(book_id)
        if book is None:
            print(f"Книга ID {book_id} не знайдена")
            return False
        return book.quantity >= quantity

class AddBookCommand(Command):
    def __init__(self, catalog: BookCatalog, book: Book):
        self.catalog = catalog
        self.book = book
        
    def execute(self):
        self.catalog.add_book(self.book)
        
    def undo(self):
        self.catalog.remove_book(self.book.id)
        print(f"(Скасування) Видалено книгу {self.book.title}")

class UpdateBookPriceCommand(Command):
    def __init__(self, catalog: BookCatalog, book_id: int, new_price: float):
        self.catalog = catalog
        self.book_id = book_id
        self.new_price = new_price
        self.old_price = None
        
    def execute(self):
        book = self.catalog.get_book(self.book_id)
        if book:
            self.old_price = book.price
            self.catalog.update_book(self.book_id, price=self.new_price)
            
    def undo(self):
        if self.old_price is not None:
            self.catalog.update_book(self.book_id, price=self.old_price)
            print(f"(Скасування) Відновлено ціну {self.old_price} для книги ID {self.book_id}")

class CheckStockCommand(Command):
    def __init__(self, catalog: BookCatalog, book_id: int, quantity: int):
        self.catalog = catalog
        self.book_id = book_id
        self.quantity = quantity
        self.was_in_stock = None
        
    def execute(self):
        self.was_in_stock = self.catalog.check_stock(self.book_id, self.quantity)
        print(f"Перевірка наявності книги ID {self.book_id}: {'Є в наявності' if self.was_in_stock else 'Недостатньо на складі'}")
        return self.was_in_stock
        
    def undo(self):
        print("(Скасування) Перевірка наявності не змінює стан системи")

# -------------------- Модуль клієнтів --------------------
class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.orders = []
    
    def __str__(self):
        return f"{self.name} ({self.email}) | Замовлень: {len(self.orders)}"

class CustomerManager:
    def __init__(self):
        self.customers = {}
        
    def add_customer(self, customer: Customer):
        self.customers[customer.id] = customer
        print(f"Додано клієнта: {customer.name}")
        
    def get_customer(self, customer_id: int) -> Customer:
        return self.customers.get(customer_id)
    
    def add_order_to_customer(self, customer_id: int, order_id: int):
        customer = self.get_customer(customer_id)
        if customer:
            customer.orders.append(order_id)
            print(f"Додано замовлення {order_id} до клієнта {customer.name}")

class RegisterCustomerCommand(Command):
    def __init__(self, manager: CustomerManager, customer: Customer):
        self.manager = manager
        self.customer = customer
        
    def execute(self):
        self.manager.add_customer(self.customer)
        
    def undo(self):
        self.manager.customers.pop(self.customer.id, None)
        print(f"(Скасування) Видалено клієнта {self.customer.name}")

class NotifyCustomerCommand(Command):
    def __init__(self, manager: CustomerManager, customer_id: int, message: str):
        self.manager = manager
        self.customer_id = customer_id
        self.message = message
        
    def execute(self):
        customer = self.manager.get_customer(self.customer_id)
        if customer:
            print(f"Надіслано сповіщення для {customer.email}: {self.message}")
            
    def undo(self):
        print("(Скасування) Неможливо відкликати сповіщення")

# -------------------- Модуль замовлень --------------------
class Order:
    def __init__(self, id: int, customer_id: int, items: Dict[int, int]):
        self.id = id
        self.customer_id = customer_id
        self.items = items
        self.status = "created"
        self.total = 0.0
    
    def __str__(self):
        return f"Замовлення #{self.id} | Статус: {self.status} | Сума: ${self.total:.2f}"

class OrderManager:
    def __init__(self, book_catalog: BookCatalog, customer_manager: CustomerManager):
        self.orders = {}
        self.book_catalog = book_catalog
        self.customer_manager = customer_manager
        self.next_order_id = 1
        
    def create_order(self, customer_id: int, items: Dict[int, int]) -> Order:
        order_id = self.next_order_id
        self.next_order_id += 1
        order = Order(order_id, customer_id, items)
        self.orders[order_id] = order
        self.customer_manager.add_order_to_customer(customer_id, order_id)
        print(f"Створено нове замовлення #{order_id}")
        return order
    
    def calculate_total(self, order_id: int):
        order = self.orders.get(order_id)
        if order:
            total = 0.0
            for book_id, quantity in order.items.items():
                book = self.book_catalog.get_book(book_id)
                if book:
                    total += book.price * quantity
            order.total = total
            print(f"Розраховано суму замовлення #{order_id}: ${total:.2f}")
            return total
        return 0.0
    
    def update_order_status(self, order_id: int, status: str):
        order = self.orders.get(order_id)
        if order:
            order.status = status
            print(f"Оновлено статус замовлення #{order_id} на '{status}'")

class CreateOrderCommand(Command):
    def __init__(self, order_manager: OrderManager, customer_id: int, items: Dict[int, int]):
        self.order_manager = order_manager
        self.customer_id = customer_id
        self.items = items
        self.order_id = None
        
    def execute(self):
        order = self.order_manager.create_order(self.customer_id, self.items)
        self.order_id = order.id
        return order
        
    def undo(self):
        if self.order_id:
            self.order_manager.orders.pop(self.order_id, None)
            print(f"(Скасування) Видалено замовлення #{self.order_id}")

class CalculateTotalCommand(Command):
    def __init__(self, order_manager: OrderManager, order_id: int):
        self.order_manager = order_manager
        self.order_id = order_id
        self.previous_total = None
        
    def execute(self):
        order = self.order_manager.orders.get(self.order_id)
        if order:
            self.previous_total = order.total
            return self.order_manager.calculate_total(self.order_id)
            
    def undo(self):
        if self.previous_total is not None:
            order = self.order_manager.orders.get(self.order_id)
            if order:
                order.total = self.previous_total
                print(f"(Скасування) Відновлено попередню суму замовлення #{self.order_id}")

class UpdateOrderStatusCommand(Command):
    def __init__(self, order_manager: OrderManager, order_id: int, new_status: str):
        self.order_manager = order_manager
        self.order_id = order_id
        self.new_status = new_status
        self.old_status = None
        
    def execute(self):
        order = self.order_manager.orders.get(self.order_id)
        if order:
            self.old_status = order.status
            self.order_manager.update_order_status(self.order_id, self.new_status)
            
    def undo(self):
        if self.old_status is not None:
            self.order_manager.update_order_status(self.order_id, self.old_status)
            print(f"(Скасування) Відновлено статус замовлення #{self.order_id} на '{self.old_status}'")

# -------------------- Модуль звітності --------------------
class SalesReport(ReportTemplate):
    def __init__(self, order_manager: OrderManager):
        self.order_manager = order_manager
        self.data = None
        self.analysis = None
        
    def collect_data(self):
        print("\nЗбір даних про продажі...")
        self.data = []
        for order in self.order_manager.orders.values():
            if order.status == "completed":
                self.data.append({
                    'order_id': order.id,
                    'customer_id': order.customer_id,
                    'total': order.total
                })
                
    def analyze_data(self):
        print("Аналіз даних про продажі...")
        total_sales = sum(item['total'] for item in self.data) if self.data else 0
        avg_sale = total_sales / len(self.data) if self.data else 0
        self.analysis = {
            'total_sales': total_sales,
            'avg_sale': avg_sale,
            'num_orders': len(self.data)
        }
        
    def format_report(self):
        return (
            "=== Звіт про продажі ===\n"
            f"Загальний обсяг продажів: ${self.analysis['total_sales']:.2f}\n"
            f"Середній чек: ${self.analysis['avg_sale']:.2f}\n"
            f"Кількість замовлень: {self.analysis['num_orders']}"
        )

class InventoryReport(ReportTemplate):
    def __init__(self, book_catalog: BookCatalog):
        self.book_catalog = book_catalog
        self.data = None
        self.analysis = None
        
    def collect_data(self):
        print("\nЗбір даних про інвентар...")
        self.data = []
        for book in self.book_catalog.books.values():
            self.data.append({
                'book_id': book.id,
                'title': book.title,
                'quantity': book.quantity,
                'price': book.price
            })
                
    def analyze_data(self):
        print("Аналіз даних про інвентар...")
        total_books = sum(item['quantity'] for item in self.data) if self.data else 0
        total_value = sum(item['quantity'] * item['price'] for item in self.data) if self.data else 0
        self.analysis = {
            'total_books': total_books,
            'total_value': total_value,
            'num_titles': len(self.data)
        }
        
    def format_report(self):
        return (
            "=== Звіт про інвентар ===\n"
            f"Загальна кількість книг: {self.analysis['total_books']}\n"
            f"Загальна вартість інвентарю: ${self.analysis['total_value']:.2f}\n"
            f"Кількість різних назв: {self.analysis['num_titles']}"
        )

# -------------------- Макрокоманди --------------------
class ProcessOrderMacro(MacroCommand):
    def __init__(self, 
                 book_catalog: BookCatalog, 
                 customer_manager: CustomerManager, 
                 order_manager: OrderManager,
                 customer_id: int,
                 items: Dict[int, int]):
        
        # Перевірка наявності всіх книг
        stock_commands = [
            CheckStockCommand(book_catalog, book_id, quantity) 
            for book_id, quantity in items.items()
        ]
        
        # Отримуємо майбутній ID замовлення
        order_id = order_manager.next_order_id
        
        commands = stock_commands + [
            CreateOrderCommand(order_manager, customer_id, items),
            CalculateTotalCommand(order_manager, order_id),
            UpdateOrderStatusCommand(order_manager, order_id, "processing"),
            NotifyCustomerCommand(
                customer_manager, 
                customer_id, 
                f"Ваше замовлення #{order_id} прийнято в обробку"
            )
        ]
        
        super().__init__(commands)

class UpdateCatalogMacro(MacroCommand):
    def __init__(self, book_catalog: BookCatalog, updates: List[Dict]):
        commands = []
        for update in updates:
            book_id = update['book_id']
            if 'price' in update:
                commands.append(UpdateBookPriceCommand(book_catalog, book_id, update['price']))
            if 'quantity' in update:
                # Можна додати команду для оновлення кількості
                pass
        
        super().__init__(commands)

# -------------------- Головна програма --------------------
def main():
    print("\n=== Ініціалізація системи книжкового магазину ===\n")
    
    # Ініціалізація системи
    catalog = BookCatalog()
    customer_manager = CustomerManager()
    order_manager = OrderManager(catalog, customer_manager)
    
    # Додаємо тестові дані
    print("\n=== Додавання тестових даних ===")
    catalog.add_book(Book(1, "Python для початківців", "Джон Сміт", 25.99, 15))
    catalog.add_book(Book(2, "Чистий код", "Роберт Мартін", 35.50, 8))
    catalog.add_book(Book(3, "Шаблони проєктування", "Банда чотирьох", 45.75, 5))
    catalog.add_book(Book(4, "Гаррі Поттер", "Дж. К. Роулінг", 20.00, 20))
    
    customer_manager.add_customer(Customer(1, "Іван Петренко", "ivan@example.com"))
    customer_manager.add_customer(Customer(2, "Марія Сидоренко", "maria@example.com"))
    
    # Приклад макрокоманди для оформлення замовлення
    print("\n=== Приклад оформлення замовлення ===")
    process_order = ProcessOrderMacro(
        catalog,
        customer_manager,
        order_manager,
        customer_id=1,
        items={1: 2, 2: 1}  # 2 Python книги, 1 Чистий код
    )
    process_order.execute()
    
    # Змінюємо статус замовлення на "completed"
    print("\n=== Завершення замовлення ===")
    UpdateOrderStatusCommand(order_manager, 1, "completed").execute()
    
    # Приклад макрокоманди для оновлення цін
    print("\n=== Оновлення цін на книги ===")
    update_catalog = UpdateCatalogMacro(
        catalog,
        [
            {'book_id': 1, 'price': 27.99},  # Зміна ціни на Python
            {'book_id': 3, 'price': 49.99}   # Зміна ціни на Шаблони проєктування
        ]
    )
    update_catalog.execute()
    
    # Генерація звітів
    print("\n=== Генерація звітів ===")
    sales_report = SalesReport(order_manager)
    print(sales_report.generate_report())
    
    inventory_report = InventoryReport(catalog)
    print(inventory_report.generate_report())
    
    # Демонстрація скасування дій
    print("\n=== Демонстрація скасування дій ===")
    update_catalog.undo()
    
    # Друге замовлення
    print("\n=== Друге тестове замовлення ===")
    process_order = ProcessOrderMacro(
        catalog,
        customer_manager,
        order_manager,
        customer_id=2,
        items={3: 1, 4: 2}  # 1 Шаблони проєктування, 2 Гаррі Поттер
    )
    process_order.execute()
    
    # Фінальний звіт про інвентар
    print("\n=== Фінальний стан інвентарю ===")
    print(inventory_report.generate_report())

if __name__ == "__main__":
    main()