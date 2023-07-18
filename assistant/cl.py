from typing import Optional
from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phone=None):
        self.name = name
        self.phones = [] if phone is None else [phone]

    def add_phone(self, phone):
        self.phones.append(phone)
        return f"/// Contact {self.name}: {phone} added successfully"

    def change_phone(self, old_phone, new_phone):
        if any(str(phone) == str(old_phone) for phone in self.phones):
            self.phones = [new_phone if str(phone) == str(old_phone) else phone for phone in self.phones]
            return f"/// Phone number changed from {old_phone} to {new_phone} for contact {self.name}"
        else:
            return f"/// Phone number {old_phone} not found for contact {self.name}"

    def __str__(self):
        return f"/// {self.name}: {', '.join(str(phone) for phone in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, name, phone):
        record = Record(name, phone)
        self.data[name] = record

    def get(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def get_all_contacts(self):
        return list(self.data.values())

    def __iter__(self):
        return iter(self.data.values())

