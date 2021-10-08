class Product:
    def __init__(self, product_id, category, model, cost, price, warranty):
        self.product_id: int = product_id
        self.category: str = category
        self.model: str = model
        self.cost: float = cost
        self.price: float = price
        self.warranty: int = warranty
