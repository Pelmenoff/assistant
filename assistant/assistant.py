def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "/// Contact not found."
        except ValueError:
            return "/// Invalid input."
        except IndexError:
            return "/// Invalid command. Type \"help\" to show all commands."
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
def show_all_handler(*args, **kwargs):
    if len(contacts) == 0:
        return "/// Contacts empty."
    else:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


@input_error
def exit_handler():
    return "/// Good bye!"
         

commands = {
    "hello": hello_handler,
    "add": add_handler,
    "change": change_handler,
    "phone": phone_handler,
}


def main():
    while True:
        user_input = input("/// Enter command: ")
        command_parts = user_input.split(" ")
        command = command_parts[0].lower()
        args = command_parts[1:]

        if command == "exit" or command == "good bye" or command == "close" or command == "quit" or command == "q":
            print(exit_handler())
            break
        elif command == "help":
            print(help_info)
        elif command == "show" and "all" in args:
            print(show_all_handler())
        
        else:
            try:
                print(commands[command](*args))
            except (IndexError, KeyError):
                print("/// Invalid command. Type \"help\" to show all commands.")


if __name__ == "__main__":
    main()