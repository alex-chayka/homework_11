from bot_classes import AddressBook, Record, Name, Phone

# users_dict = {}
contacts_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)

        except IndexError:
            return "Not enough params. Try again."

        except KeyError:
            return 'No such user in Contacts. Use "add" command to add one.'

        except TypeError as e:
            # return "Phone number should contain only numbers."
            return e

        except ValueError as e:
            return e

    return inner


def hello(*args):
    return "How can I help you?"


def exit(*args):
    return "Good bye!"


@input_error
def change_phone(*args):
    name = args[0][2]
    phone_old = Phone(args[0][3])
    phone_new = Phone(args[0][4])

    if not contacts_book.has_name(name):
        raise KeyError

    contacts_book[name].change_phone(phone_old, phone_new)

    return f"Phone number {phone_old} for user {name} is changed to {phone_new}."


@input_error
def delete_phone(*args):
    name = args[0][2]
    phone = Phone(args[0][3])

    if not contacts_book.has_name(name):
        raise KeyError

    contacts_book[name].delete_phone(phone)

    return f"Phone number {phone} for user {name} is deleted."


@input_error
def add_phone(*args):
    name = args[0][2]
    phone = Phone(args[0][3])

    if not contacts_book.has_name(name):
        raise KeyError

    contacts_book[name].add_phone(phone)

    return f"Phone number {phone} for user {name} is added."


@input_error
def show_phones(*args):
    name = args[0][2]

    if not contacts_book.has_name(name):
        raise KeyError

    phone_numbers = contacts_book[name].show_phones()

    return f"Phone numbers for {name}: {phone_numbers}."


@input_error
def show_all(*args):
    if len(contacts_book) == 0:
        raise ValueError("Phone book is empty.")

    all_users = ""
    for v in contacts_book.values():
        all_users += f"{v}\n"

    return all_users


@input_error
def add_user(*args):
    name = Name(args[0][2])
    phone = Phone(args[0][3])

    record = Record(name, phone)

    if contacts_book.has_name(record.name.value):
        return f"User {name.value} is already in Contacts."

    contacts_book.add_record(record)

    return f"Added user {name.value} with phone number {phone.phone_number}."


def no_command(*args):
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
}


def command_handler(text):
    for keyword, command in COMMANDS.items():
        if text.lower().startswith(keyword):
            # return command, text.replace(keyword, "").strip().split()
            return command, text.split(" ")
    return no_command, None


def main():
    print(hello())
    while True:
        user_input = input(">>>")
        command, data = command_handler(user_input)
        print(command(data))
        if command == exit:
            break


if __name__ == "__main__":
    main()
