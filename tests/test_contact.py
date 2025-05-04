import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Fixed __file__

import pytest
from contact import Contact

print(f"Contact class being used: {Contact}")

def test_contact_creation():
    contact = Contact("John Doe", "123-456-7890", "john@example.com", "Friends")
    assert contact.name == "John Doe"
    assert contact.phone == "123-456-7890"
    assert contact.email == "john@example.com"
    assert contact.category == "Friends"

def test_contact_repr():
    contact = Contact("Jane Smith", "987-654-3210", "jane@example.com", "Family")
    assert repr(contact) == "Contact(name='Jane Smith', phone='987-654-3210', email='jane@example.com', category='Family')"
    # assert str(repr(contact)) == expected  # Removed this line.  It's causing NameError and unnecessary

