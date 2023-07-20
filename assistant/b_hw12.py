import atexit
from cl_hw12 import AddressBook, Name, Phone, Birthday, Record
from datetime import datetime

address_book = AddressBook()
address_book.load_from_file('address_book.dat')

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
/// "add [name] [phone] [birthday]" - Add a contact to the address book. Birthday is optional.
/// "changephone [name] [old_phone] [new_phone]" or "cp [name] [old_phone] [new_phone]" - Change the phone number for a contact.
/// "changebirthdate [name] [new_date]" or "cb [name] [new_date]" - Change the birthdate for a contact.
/// "showcontacts all" or "sc all" - Show all contacts.
/// "showcontacts [page_number]" or "sc [page_number]" - Show contacts page by page. Enter 'all' to show all contacts at once.
/// "find [search_text]" - Search for contacts by name or phone number.
/// "exit", "bye", "good bye", "close", "quit", "q" - Turn off the assistant."""

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
    birthday = None
    if len(args) > 2:
        birthday = Birthday(datetime.strptime(args[2], "%d.%m.%Y").date())

    existing_contact = address_book.get(name.value)
    if existing_contact:
        existing_contact.add_phone(phone)
        if birthday:
            existing_contact.birthday = birthday
        return f"/// Contact {name.value}: {phone} updated successfully"

    address_book.add_record(name, phone, birthday)
    return f"/// Contact {name.value}: {phone} added successfully"

@input_error
def cp_handler(*args):
    if len(args) < 3:
        return "/// Invalid command. Please provide name, old phone, and new phone."

    name = args[0]
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])

    rec: Record = address_book.get(name)
    if rec:
        if any(str(phone) == str(old_phone) for phone in rec.phones):
            rec.change_phone(old_phone, new_phone)
            return f"/// Phone number changed from {old_phone} to {new_phone} for contact {name}"
        else:
            return f"/// Phone number {old_phone} not found for contact {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"

@input_error
def cd_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and new birthdate (in the format 'dd.mm.yyyy')."

    name = args[0]
    new_birthday = Birthday(datetime.strptime(args[1], "%d.%m.%Y").date())

    rec: Record = address_book.get(name)
    if rec:
        rec.birthday = new_birthday
        return f"/// Birthdate changed to {new_birthday} for contact {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"

def exit_handler(*args):
    return "/// Good bye!"

@input_error
def unknown_handler(*args):
    return "/// Invalid command. Type \"help\" to show all commands."

def format_contact(index, contact):
    return f"/// {index}. {str(contact)[4:]}"

@input_error
def show_handler(*args):
    if len(args) < 1:
        return "/// Invalid command. Please provide the page number or 'all'."

    page_number = args[0]
    if page_number.lower() == "all":
        contacts = address_book.get_all_contacts()
        if not contacts:
            return "/// No contacts found in the address book."

        output = ["/// Contacts List:"]
        for i, contact in enumerate(contacts, start=1):
            output.append(format_contact(i, contact))
        return "\n".join(output)
    else:
        page_number = int(page_number)
        contacts_per_page = 5
        contacts = address_book.get_all_contacts()
        total_pages = (len(contacts) - 1) // contacts_per_page + 1

        if page_number < 1 or page_number > total_pages:
            return f"/// Invalid page number. Please enter a number between 1 and {total_pages}."

        start_index = (page_number - 1) * contacts_per_page
        end_index = min(start_index + contacts_per_page, len(contacts))
        contacts_on_page = contacts[start_index:end_index]

        output = [f"/// --- Contacts Page {page_number}/{total_pages} ---"]
        for i, contact in enumerate(contacts_on_page, start=start_index + 1):
            output.append(format_contact(i, contact))
        output.append(f"/// ---  End of Page {page_number}/{total_pages}  ---")
        return "\n".join(output)

def find_handler(*args):
    if len(args) < 1:
        return "/// Invalid command. Please provide the search text."

    search_text = args[0]
    search_results = address_book.search(search_text)

    if search_results:
        output = [f"/// Search results for '{search_text}':"]
        for record in search_results:
            output.append(f"{str(record)}")
        return "\n".join(output)
    else:
        return f"/// No contacts found matching '{search_text}'."

COMMANDS = {
    hello_handler: ("hello", "hi"),
    add_handler: ("add", "+", "plus"),
    cp_handler: ("changephone", "cp"),
    cd_handler: ("changebirthdate", "cb"),
    exit_handler: ("bye", "exit", "break", "good bye", "close", "quit", "q"),
    show_handler: ("sc all", "showcontacts all", "sc", "showcontacts"),
    help_handler: ("help"),
    find_handler: ("find"),
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

def save_address_book_on_exit():
    address_book.save_to_file('address_book.dat')
atexit.register(save_address_book_on_exit)

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

    address_book.save_to_file('address_book.dat')

if __name__ == "__main__":
    main()