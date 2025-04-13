class Contact:
    def __init__(self, name, phone, email, category):
        self.name = name
        self.phone = phone
        self.email = email
        self.category = category
    
    def __str__(self):
        return f"{self.name} ({self.category}): {self.phone}, {self.email}"
