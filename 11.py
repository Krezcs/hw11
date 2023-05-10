from datetime import date
from collections import UserDict


class Field:
    def __init__(self, value=None):
        self._value = value

    def validate(self):
        raise NotImplementedError("Validation logic must be implemented in the subclass.")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate()
        self._value = new_value


class Name(Field):
    def validate(self):
        if not self.value:
            raise ValueError("Name field is required.")


class Phone(Field):
    def validate(self):
        if self.value and not isinstance(self.value, str):
            raise ValueError("Phone field must be a string.")


class Birthday(Field):
    def validate(self):
        if self.value and not isinstance(self.value, date):
            raise ValueError("Birthday field must be a date.")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        phone_obj.validate()
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                break

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                phone_obj.validate()
                break

    def days_to_birthday(self):
        if not self.birthday.value:
            return None

        today = date.today()
        next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)

        if next_birthday < today:
            next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)

        days_until_birthday = (next_birthday - today).days
        return days_until_birthday


class AddressBook(UserDict):
    def __init__(self, data=None):
        super().__init__(data)
        self._index = 0
        self._page_size = 5

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.data):
            raise StopIteration

        items = list(self.data.items())
        page_items = items[self._index : self._index + self._page_size]
        self._index += self._page_size
        return dict(page_items)

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        del self.data[record.name.value]

    def edit_record_name(self, old_name, new_name):
        record = self.data.pop(old_name)
        record.name.value = new_name
        self.data[new_name] = record
