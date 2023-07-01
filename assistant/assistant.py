def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "/// Contact not found."
        except ValueError:
            return "/// Invalid input."
        except IndexError:
            return "/// Invalid command. Type \"help\" to show all commands "
    return wrapper


contacts = {}
help_info = """/// Commands:
/// "show all" - Show contacts.
/// "add [name] [phone]" - Add contact to memory.
/// "change [name] [phone]" - Change phone number.
/// "phone [name]" - Show phone number.
/// "exit"; "good bye"; "close"; "quit"; "q" - Turn off assistant."""


@input_error
def hello_handler():
    return "/// How can I help you?"

@input_error
def add_handler(name, phone):
    contacts[name] = phone
    return "/// Contact added."

@input_error
def change_handler(name, phone):
    if name in contacts:
        contacts[name] = phone
        return "/// Phone number changed."
    else:
        raise KeyError

@input_error
def phone_handler(name):
    return contacts[name]

@input_error
def show_all_handler():
    if len(contacts) == 0:
        return "/// Contacts empty."
    else:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    while True:
        c = input("/// ---> ").lower()
        
        if c == "good bye" or c == "close" or c == "exit" or c == "quit" or c == "q":
            print("/// Good bye!")
            break
        
        if c == "hello":
            print(hello_handler())
        elif c.startswith("help"):
            print(help_info)
        elif c.startswith("add"):
            try:
                _, name, phone = c.split()
                print(add_handler(name, phone))
            except ValueError:
                print("/// Give me name and phone please.")
        elif c.startswith("change"):
            try:
                _, name, phone = c.split()
                print(change_handler(name, phone))
            except ValueError:
                print("/// Give me name and phone please.")
        elif c.startswith("phone"):
            try:
                _, name = c.split()
                print(phone_handler(name))
            except ValueError:
                print("/// Enter user name.")
        elif c == "show all":
            print(show_all_handler())
        else:
            print("/// Invalid command. Type \"help\" to show all commands ")


if __name__ == "__main__":
    main()