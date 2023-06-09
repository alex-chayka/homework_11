from collections import UserDict
from datetime import datetime, date
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

    def search_phone(self, search_str):
        result = []
        for record in self.data.values():
            for phone in record.phones:
                if phone.value.startswith(search_str):
                    result.append(record)
                    break
        return result

    def save_to_file(self, file):
        with open(file, "wb") as f:
            pickle.dump(self.data, f)

    def load_from_file(self, file):
        with open(file, "rb") as f:
            self.data = pickle.load(f)

    def show_records(self, size: int):
        counter = 0
        result = ""
        for record in self.data.values():
            result += f"{record}\n"
            counter += 1
            if counter == int(size):
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
        return f"{self.__value}"


#    def __eq__(self, other):
#       return self.value == other.value


class Birthday(Field):
    def __init__(self, value):
        # super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, value):
        try:
            # self.__value = datetime.strptime(value, "%d-%m-%Y").date()
            Field.value.fset(self, datetime.strptime(value, "%d-%m-%Y").date())
        except ValueError:
            raise ValueError("Date should be in format dd-mm-YYYY")


class Name(Field):
    def __init__(self, value):
        # super().__init__(value)
        self.value = value


class Phone(Field):
    def __init__(self, value):
        # super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, value):
        if not re.match(r"\+38\d{10}", value):
            raise ValueError("Phone number should be +380XXXXXXXXX.")
        Field.value.fset(self, value)

    #   def __str__(self) -> str:
    #        return self.__value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        return self.value == other


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
        return "; ".join(phone.value for phone in self.phones)

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("No birthday")
        now = date.today()
        if (days_to_bd := (self.birthday.value.replace(year=now.year) - now).days) > 0:
            return days_to_bd
        else:
            return (self.birthday.value.replace(year=now.year + 1) - now).days
