from collections import UserDict
from pathlib import Path
from datetime import datetime
import re
import pickle


class AddressBook(UserDict):
    # def __init__(self, filename):
    #     super().__init__()
    #     self.file = Path(filename)
    #     self.deserialize()

    def add_record(self, record):
        self.data[record.name.value] = record

    def has_name(self, value):
        return value in self.data.keys()

    def search_name(self, search_str):
        result = []
        for key, record in self.data.items():
            if key.startswith(search_str):
                result.append(record)

        return result

    def search(self, search_str):
        result = []
        for key, record in self.data.items():
            if search_str in record:
                result.append(record)
        return result

    def save_to_file(self, file):
        with open(file, "wb") as f:
            pickle.dump(self.data, f)

    @staticmethod
    def load_from_file(file):
        with open(file, "rb") as f:
            return pickle.load(f)

    def show_record(self, rec_id):
        return f"{self.data[rec_id]}\n"

    def show_records(self, size: int):
        counter = 0
        result = ""
        for record in self.data.values():
            result += str(record)
            counter += 1
            if counter == size:
                yield result
                counter = 0
                result = ""
        yield result


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other):
        return self.value == other.value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        self.__value = datetime.strptime(value, "%d%m%Y").date()


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.phone_number = ""

        @Field.value.setter
        def value(self, value):
            if not re.match(r"^\+38\d{10}$", value):
                raise ValueError("Phone number should be +380XXXXXXXXX.")

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

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("No birthday")
        now = datetime.now()
        if (days_to_bd := (self.birthday.value.replace(year=now.year) - now).days) > 0:
            return days_to_bd
        return (self.birthday.value.replace(year=now.year + 1) - now).days
