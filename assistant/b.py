from cl import AddressBook, Name, Phone, Record

address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "/// Contact not found."
        except ValueError:
            return "/// Invalid input."
        except IndexError:
            return "/// Invalid command. Type \"help\" to show all commands."
    return wrapper


help_info = """/// Commands:
/// "show all" - Show contacts.
/// "add [name] [phone]" - Add contact to memory.
/// "change [name] [old_phone] [new_phone]" - Change phone number.
/// "phone [name]" - Show phone number.
/// "exit"; "good bye"; "close"; "quit"; "q" - Turn off assistant."""


@input_error
def hello_handler(*args):
    return "/// How can I help you?"


@input_error
def help_handler(*args):
    return f"{help_info}"


@input_error
def add_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and phone."

    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)

    rec = Record(name)
    rec.add_phone(phone)
    address_book.add_record(rec)
    return f"/// Contact {rec.name}: {phone} added successfully"


@input_error
def change_handler(*args):
    if len(args) < 3:
        return "/// Invalid command. Please provide name, old phone, and new phone."

    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])

    rec: Record = address_book.get(str(name))
    if rec:
        if any(str(phone) == str(old_phone) for phone in rec.phones):
            rec.change_phone(old_phone, new_phone)
            return f"/// Phone number changed from {old_phone} to {new_phone} for contact {name}"
        else:
            return f"/// Phone number {old_phone} not found for contact {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"




def exit_handler(*args):
    return "/// Good bye!"


@input_error
def unknown_handler(*args):
    return "/// Invalid command. Type \"help\" to show all commands."


def show_all_handler(*args):
    contacts = address_book.get_all_contacts()
    if contacts:
        return "\n".join(str(record) for record in contacts)
    else:
        return "/// No contacts found in the address book."


COMMANDS = {
    hello_handler: ("hello", "hi"),
    add_handler: ("add", "+", "plus"),
    change_handler: ("change", "ch"),
    exit_handler: ("bye", "exit", "break", "good bye", "close", "quit", "q"),
    show_all_handler: ("show all"),
    help_handler: ("help"),
}


def parser(text: str):
    if not text.strip():
        return unknown_handler, []

    command_parts = text.strip().split()
    cmd = command_parts[0]
    data = command_parts[1:] if len(command_parts) > 1 else []

    for handler, keywords in COMMANDS.items():
        if cmd.lower() in keywords:
            return handler, data
    return unknown_handler, []



def main():
    while True:
        user_input = input("/// ---> ")
        
        cmd, data = parser(user_input)
        
        result = cmd(*data)
        try:
            print(result)
        except IndexError:
            print(unknown_handler())

        if cmd == exit_handler:
            break


if __name__ == "__main__":
    main()
