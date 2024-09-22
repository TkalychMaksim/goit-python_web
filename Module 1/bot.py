import pickle
from classes import *

def save_data(book, filename="addressbook.pkl"):
    try:
        with open(filename, "wb") as file:
            pickle.dump(book, file)
    except Exception as exc:
        print(exc)


def load_data(view, filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook(view)



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as exc:
            return f"Error: {str(exc)}"
    return inner



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise IndexError("Enter both name and phone numbers")
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_value=old_phone, new_value=new_phone)
    
    
@input_error
def phone_contact(args,book):
    name = args[0]
    record = book.find(name)
    phones =  f"{name} phones "+'; '.join(phone.value for phone in record.phones)
    return phones

def all_contacts(book: AddressBook):
    if not book.data:
        return "No contacts found"
    return book.show_all_contacts()


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday was added"
    

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    birthday = record.birthday.value
    return f"{name}: {birthday}"


@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    for birthday in upcoming_birthdays:
        print(f"{birthday['name']}: {birthday['birthday']}")


@input_error
def help(book=AddressBook):
    return book.show_help()
    
def main():
    view = ConsoleView()
    book = load_data(view)
    print("Welcome to the assistant bot :3")
    while True:
        user_input = input("Enter the command: ")
        command, *args = parse_input(user_input)
        match command:
            case "hello": print("How I can help you?")
            case "exit" | "end":
                save_data(book)
                print("Good Bye!") 
                exit()
            case "add":
                print(add_contact(args,book))
            case "change":
                change_contact(args,book)
            case "phone":
                print(phone_contact(args,book))
            case "all":
                print(all_contacts(book))
            case "add_birthday":
                print(add_birthday(args,book))
            case "show_birthday":
                print(show_birthday(args,book))
            case "birthdays":
                birthdays(book)
            case "help":
                help(book)
            case _:
                print("Command does not exist")               


if __name__ == "__main__":
    main()