import datetime
import enum
from typing import Union


class Request:
    def __init__(self, request_id, service_amount, service_payment_date, request_status, request_date, customer_id,
                 admin_id):
        self.request_id: int = request_id
        self.service_amount: float = service_amount
        self.service_payment_date: datetime.date = service_payment_date
        self.request_status: RequestStatus = request_status
        self.request_date: datetime.date = request_date
        self.customer_id: int = customer_id
        self.admin_id: Union[int, None] = admin_id


class RequestStatus(enum.Enum):
    Empty = ''
    Submitted = 'Submitted'
    WaitingForApproval = 'Submitted and Waiting for payment'
    InProgress = 'In progress'
    Approved = 'Approved'
    Canceled = 'Canceled'
    Completed = 'Completed'