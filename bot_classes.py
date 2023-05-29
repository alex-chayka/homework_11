from collections import UserDict

# import re


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def has_name(self, value):
        return value in self.data.keys()


class Field:
    pass


class Name(Field):
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value


class Phone(Field):
    def __init__(self, value):
        # self.phone_number = ""
        # if not re.match(r"^\+38\d{10}$", value):
        #    raise ValueError("Phone number should be +380XXXXXXXXX.")
        self.phone_number = value

    def __str__(self) -> str:
        return self.phone_number

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.phone_number == other.phone_number
        return self.phone_number == other


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phones = []
        if phone is not None:
            self.add_phone(phone)
        self.birthday = birthday

    def __str__(self) -> str:
        return f"Name: {self.name}. Phones: {self.show_phones()}. Birthday: {self.birthday}"

    def add_phone(self, phone):
        # if phone.phone_number not in (_.phone_number for _ in self.phones):
        if phone not in self.phones:
            self.phones.append(phone)
        else:
            raise ValueError("The phone number already exists.")

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)

        except ValueError:
            raise ValueError("There is no such phone number.")

    def change_phone(self, phone_old, phone_new):
        found = False
        for i, v in enumerate(self.phones):
            # if v.phone_number == phone_old.phone_number:
            if v == phone_old:
                self.phones[i] = phone_new
                found = True

        if not found:
            raise ValueError("There is no such phone number.")

    def show_phones(self):
        return "; ".join(phone.phone_number for phone in self.phones)
