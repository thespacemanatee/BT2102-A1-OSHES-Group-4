class Customer:
    def __init__(self, cust_id, name, gender, email, address, phone):
        self.id: int = cust_id
        self.name: str = name
        self.gender: str = gender
        self.email: str = email
        self.address: str = address
        self.phone: int = phone
