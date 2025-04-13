from contact import Contact

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.categories = ["Друзья", "Семья", "Работа"]
    
    def add_contact(self, name, phone, email, category):
        contact = Contact(name, phone, email, category)
        self.contacts.append(contact)
        return contact
    
    def edit_contact(self, index, name, phone, email, category):
        if 0 <= index < len(self.contacts):
            self.contacts[index].name = name
            self.contacts[index].phone = phone
            self.contacts[index].email = email
            self.contacts[index].category = category
            return True
        return False
    
    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            return self.contacts.pop(index)
        return None
    
    def search_contacts(self, query):
        query = query.lower()
        return [
            contact for contact in self.contacts
            if (query in contact.name.lower() or 
                query in contact.phone or 
                query in contact.email.lower())
        ]
    
    def get_all_contacts(self):
        return self.contacts.copy()
