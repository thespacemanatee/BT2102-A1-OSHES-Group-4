import datetime
import enum
from typing import Union


class Item:
    def __init__(self, item_id, colour, power_supply, factory, production_year, purchase_status, service_status, purchase_date,
                 customer_id, admin_id, product_id):
        self.item_id = item_id
        self.colour: str = colour
        self.power_supply: str = power_supply
        self.factory: str = factory
        self.production_year: int = production_year
        self.purchase_status: PurchaseStatus = purchase_status
        self.service_status: ServiceStatus = service_status
        self.purchase_date: datetime.date = purchase_date
        self.customer_id: Union[int, None] = customer_id
        self.admin_id: Union[int, None] = admin_id
        self.product_id: int = product_id


class ServiceStatus(enum.Enum):
    WaitingForApproval = 'Waiting for approval'
    InProgress = 'In progress'
    Completed = 'Completed'


class PurchaseStatus(enum.Enum):
    Sold = 'Sold'
    Unsold = 'Unsold'
