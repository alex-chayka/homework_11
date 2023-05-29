from bot_classes import AddressBook, Record, Name, Phone, Birthday
from pathlib import Path


file = Path("contacts.bin")

if file.exists():
    contacts_book = AddressBook.load_from_file(file)
else:
    contacts_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)

        except IndexError:
            return "Not enough params. Try again."

        except KeyError:
            return 'No such user in Contacts. Use "add" command to add one.'

        # except TypeError: as e:
        except TypeError:
            return "Not enough params. Try again."
            # return "Phone number should contain only numbers."
            # return e

        except ValueError as e:
            return e

    return inner


def hello():
    return "How can I help you?"


def exit():
    contacts_book.save_to_file(file)
    return "Good bye!"


@input_error
def change_phone(name, phone_old_input, phone_new_input):
    phone_old = Phone(phone_old_input)
    phone_new = Phone(phone_new_input)

    if not contacts_book.has_name(name):
        raise KeyError

    contacts_book[name].change_phone(phone_old, phone_new)

    return f"Phone number {phone_old} for user {name} is changed to {phone_new}."


@input_error
def delete_phone(name, phone_input):
    # name = args[0][2]
    phone = Phone(phone_input)

    if not contacts_book.has_name(name):
        raise KeyError

    contacts_book[name].delete_phone(phone)

    return f"Phone number {phone} for user {name} is deleted."


@input_error
def add_phone(name, phone_input):
    # name = args[0][2]
    phone = Phone(phone_input)

    if not contacts_book.has_name(name):
        raise KeyError

    contacts_book[name].add_phone(phone)

    return f"Phone number {phone} for user {name} is added."


@input_error
def show_phones(name):
    # name = args[0][2]

    if not contacts_book.has_name(name):
        raise KeyError

    phone_numbers = contacts_book[name].show_phones()

    return f"Phone numbers for {name}: {phone_numbers}."


@input_error
def search(search_str):
    results = contacts_book.search(search_str)
    if len(results) > 0:
        return f"Results: {results}\n"
    else:
        raise ValueError("Nothing found.")


@input_error
def days_to_bd(name):
    if not contacts_book.has_name(name):
        raise KeyError

    days_to_birthday = contacts_book[name].days_to_birthday()

    return f"{name} has a birthday in {days_to_birthday} day(s)."


@input_error
def show_all(_=None, item_counts=0):
    if len(contacts_book) == 0:
        raise ValueError("Phone book is empty.")

    if item_counts > 0:
        for k in contacts_book.show_records(item_counts):
            print("*" * 30)
            print(k)
            input("Press any key")

    else:
        all_users = ""
        for v in contacts_book.values():
            all_users += f"{v}\n"
        return all_users


@input_error
def add_user(name_input, phone_input, birthday_input=None):
    name = Name(name_input)
    phone = Phone(phone_input)

    if birthday_input:
        birthday = Birthday(birthday_input)
        record = Record(name, phone, birthday)
    else:
        record = Record(name, phone)

    if contacts_book.has_name(record.name.value):
        return f"User {name.value} is already in Contacts."

    contacts_book.add_record(record)

    return f"Added user {name.value} with phone number {phone.phone_number}."


def no_command():
    return "Unknown command, try again."


COMMANDS = {
    "hello": hello,
    "add user": add_user,
    "change phone": change_phone,
    "add phone": add_phone,
    "delete phone": delete_phone,
    "show phones": show_phones,
    "show all": show_all,
    "exit": exit,
    "close": exit,
    "good_bye": exit,
    "days to bd": days_to_bd,
    "search": search,
}


def command_handler(text):
    for keyword, command in COMMANDS.items():
        if text.lower().startswith(keyword):
            return command, text.replace(keyword, "").strip()
            # return command, text.split(" ")
    return no_command, None


def main():
    print(hello())
    while True:
        user_input = input(">>>")
        command, data = command_handler(user_input)

        if data:
            data = data.split(", ")

        if command != no_command:
            print(command(*data))
        else:
            print(no_command())

        if command == exit:
            break


if __name__ == "__main__":
    main()
