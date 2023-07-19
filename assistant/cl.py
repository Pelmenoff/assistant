from typing import Optional
from collections import UserDict
from datetime import date


class Field:
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Please provide a 10-digit number.")

    @Field.value.setter
    def value(self, new_value):
        self.validate_phone(new_value)
        super(Phone, Phone).value.__set__(self, new_value)

    @Field.value.getter
    def value(self):
        return super(Phone, Phone).value.__get__(self)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate_birthday(self, value):
        if not isinstance(value, date):
            raise ValueError("Invalid birthday format. Please provide a date object.")

    @Field.value.setter
    def value(self, new_value):
        self.validate_birthday(new_value)
        super(Birthday, Birthday).value.__set__(self, new_value)

    @Field.value.getter
    def value(self):
        return super(Birthday, Birthday).value.__get__(self)

    def __str__(self):
        return self.value.strftime("%d-%m-%Y")

    def __repr__(self):
        return str(self.value)


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [] if phone is None else [phone]
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)
        return f"/// Contact {self.name}: {phone} added successfully"

    def change_phone(self, old_phone, new_phone):
        if any(str(phone) == str(old_phone) for phone in self.phones):
            self.phones = [new_phone if str(phone) == str(old_phone) else phone for phone in self.phones]
            return f"/// Phone number changed from {old_phone} to {new_phone} for contact {self.name}"
        else:
            return f"/// Phone number {old_phone} not found for contact {self.name}"

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "N/A"
        birthday_days_info = self.days_to_birthday()

        if birthday_days_info is not None:
            return f"/// {self.name}: {phones_str}, Birthday: {birthday_str}. {birthday_days_info} days"
        else:
            return f"/// {self.name}: {phones_str}, Birthday: {birthday_str}."


class AddressBook(UserDict):
    def add_record(self, name, phone, birthday=None):
        record = Record(name, phone, birthday)
        self.data[name] = record

    def get(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def get_all_contacts(self):
        return list(self.data.values())

    def __iter__(self):
        return AddressBookIterator(self.data.values())


class AddressBookIterator:
    def __init__(self, records):
        self.records = records
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.records):
            record = self.records[self.index]
            self.index += 1
            return record
        raise StopIteration
