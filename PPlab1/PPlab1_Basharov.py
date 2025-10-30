import json
import xml.etree.ElementTree as ET


# главный класс магазина
class EStore:
    """Главный класс, представляющий интернет-магазин электроники."""

    def __init__(self, name: str):
        self.name = name
        self.warehouses: list[Warehouse] = []
        self.customers: list[Customer] = []
        self.orders: list[Order] = []
        self.workers: list[Worker] = []

    def add_warehouse(self, warehouse: "Warehouse") -> None:
        self.warehouses.append(warehouse)

    def add_customer(self, customer: "Customer") -> None:
        self.customers.append(customer)

    def add_order(self, order: "Order") -> None:
        self.orders.append(order)

    def add_worker(self, worker: "Worker") -> None:
        self.workers.append(worker)

    #работа с JSON файлами
    def save_to_json(self, filename: str) -> None:
        """Сохранение информации о магазине в JSON."""
        data = {
            "name": self.name,
            "warehouses": [
                {
                    "location": w.location,
                    "products": [{"name": p.name, "price": p.price, "quantity": p.quantity} for p in w.products],
                    "workers": [{"name": wr.name, "role": wr.role} for wr in w.workers]
                } for w in self.warehouses
            ],
            "customers": [{"name": c.name, "email": c.email} for c in self.customers],
            "orders": [
                {"customer": o.customer.name, "product": o.product.name, "quantity": o.quantity}
                for o in self.orders
            ],
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # работа с XML файлами
    def save_to_xml(self, filename: str) -> None:
        """Сохранение информации о магазине в XML."""
        root = ET.Element("estore", name=self.name)

        for w in self.warehouses:
            w_el = ET.SubElement(root, "warehouse", location=w.location)

            for p in w.products:
                ET.SubElement(
                    w_el, "product",
                    name=p.name,
                    price=str(p.price),
                    quantity=str(p.quantity)
                )

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)


class Product:
    """Класс, представляющий товар магазина."""

    def __init__(self, name: str, price: float, quantity: int = 0):
        self.name = name
        self.price = price
        self.quantity = quantity


class Worker:
    """Класс, представляющий сотрудника магазина."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role


class Customer:
    """Класс, представляющий покупателя."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class Warehouse:
    """Класс, представляющий склад магазина."""

    def __init__(self, location: str):
        self.location = location
        self.products: list[Product] = []
        self.workers: list[Worker] = []

    def add_product(self, product: Product) -> None:
        """Добавить товар на склад."""
        self.products.append(product)

    def get_products(self) -> list[Product]:
        """Получить список товаров."""
        return self.products

    def update_product(self, name: str, new_price: float) -> None:
        """Изменить цену товара."""
        for p in self.products:
            if p.name == name:
                p.price = new_price
                return
        raise ProductNotFoundError(f"Товар '{name}' не найден")

    def remove_product(self, name: str) -> None:
        """Удалить товар по названию."""
        for p in self.products:
            if p.name == name:
                self.products.remove(p)
                return
        raise ProductNotFoundError(f"Товар '{name}' не найден")

    def add_worker(self, worker: Worker) -> None:
        """Добавить сотрудника на склад."""
        self.workers.append(worker)


class Order:
    """Класс, представляющий заказ покупателя."""

    def __init__(self, customer: Customer, product: Product, quantity: int):
        self.customer = customer
        self.product = product
        self.quantity = quantity

    def process_order(self) -> None:
        """Обработка заказа, уменьшение остатков."""
        if self.quantity > self.product.quantity:
            raise InsufficientStockError(f"Недостаточно товара {self.product.name}")
        self.product.quantity -= self.quantity


#классы исключения
class StoreError(Exception):
    """Базовый класс ошибок"""
    pass


class ProductNotFoundError(StoreError):
    """Ошибка: товар не найден"""
    pass


class InsufficientStockError(StoreError):
    """Ошибка: недостаточно товара на складе"""
    pass


class InvalidOrderError(StoreError):
    """Ошибка: некорректный заказ"""
    pass
