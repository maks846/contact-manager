import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from manager import ContactManager
from contact import Contact

@pytest.fixture
def contact_manager():
    manager = ContactManager()
    return manager

def test_add_contact(contact_manager):
    contact = contact_manager.add_contact("Alice", "555-1234", "alice@example.com", "Work")
    assert len(contact_manager.contacts) == 1
    assert contact_manager.contacts[0] == contact
    assert contact.name == "Alice"

def test_edit_contact(contact_manager):
    contact = contact_manager.add_contact("Bob", "555-5678", "bob@example.com", "Friends")
    contact_manager.edit_contact(0, "Robert", "555-9012", "robert@example.com", "Family")
    assert contact_manager.contacts[0].name == "Robert"
    assert contact_manager.contacts[0].phone == "555-9012"
    assert contact_manager.contacts[0].email == "robert@example.com"
    assert contact_manager.contacts[0].category == "Family"

def test_delete_contact(contact_manager):
    contact = contact_manager.add_contact("Charlie", "555-3456", "charlie@example.com", "Work")
    contact_manager.delete_contact(0)
    assert len(contact_manager.contacts) == 0

def test_search_contacts(contact_manager):
    contact1 = contact_manager.add_contact("David", "555-7890", "david@example.com", "Friends")
    contact2 = contact_manager.add_contact("Eve", "555-2345", "eve@example.com", "Family")
    results = contact_manager.search_contacts("david")
    assert len(results) == 1
    assert results[0] == contact1
    results = contact_manager.search_contacts("555-2345")
    assert len(results) == 1
    assert results[0] == contact2
    results = contact_manager.search_contacts("invalid")
    assert len(results) == 0

def test_get_all_contacts(contact_manager):
    contact1 = contact_manager.add_contact("Frank", "555-6789", "frank@example.com", "Work")
    contact2 = contact_manager.add_contact("Grace", "555-0123", "grace@example.com", "Friends")
    all_contacts = contact_manager.get_all_contacts()
    assert len(all_contacts) == 2
    assert all_contacts[0] == contact1
    assert all_contacts[1] == contact2
    assert all_contacts is not contact_manager.contacts  # Check if it's a copy

