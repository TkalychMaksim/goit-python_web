from collections import UserDict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)
    
    
    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return False


    def __hash__(self):
        return hash(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise ValueError("Phone number must contain 10 characters")
        else:
            super().__init__(value)
		

class Birthday(Field):
    def __init__(self, value):
        try:
            date_value = datetime.strptime(value,"%d.%m.%Y").date()
            super().__init__(date_value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)
        
    def remove_phone(self, value):
        phone_to_remove = Phone(value)
        if phone_to_remove in self.phones:
            self.phones.remove(phone_to_remove)
            print("The number has been deleted")
        else:
            print("The number has not been found")
            
    def edit_phone(self, old_value, new_value):
        old_phone = Phone(old_value)
        new_phone = Phone(new_value)
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
            print(f"Phone number {old_value} was changed to {new_value}")
        else:
            print(f"Phone number {old_value} not found")
            
    def find_phone(self, value):
        finding_phone = Phone(value)
        for phone in self.phones:
            if phone == finding_phone:
                return phone
        return None
    
    def add_birthday(self, value):
        birthday_day = Birthday(value)
        self.birthday = birthday_day

    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, Contact birthday: {birthday_str}, phones: {phones_str}"

class UserView(ABC):
    @abstractmethod
    def display_contact(self,record):
        pass
    
    @abstractmethod
    def display_all_contacts(self, address_book):
        pass
    
    @abstractmethod
    def display_help(self):
        pass

    
class ConsoleView(UserView):
    def display_contact(self, record):
        print(record)
        
    def display_all_contacts(self, address_book):
        if not address_book:
            print("No contacts found")
        else:
            for record in address_book.values():
                self.display_contact(record)
    
    def display_help(self):
        print("Available commands:")
        print("1. Add contact: add <name> <phone> [birthday]")
        print("2. Remove contact: remove <name>")
        print("3. Find contact: find <name>")
        print("4. Edit contact: edit <name> <old phone> <new phone>")
        print("5. Show all contacts: show all")
        print("6. Show upcoming birthdays: upcoming birthdays")


class AddressBook(UserDict):
    def __init__(self,view: UserView):
        super().__init__()
        self.view = view

    def show_contact(self, name):
        record = self.find(name)
        if record:
            self.view.display_contact(record)
        else:
            print(f"Contact {name} not found.")
    
    def show_all_contacts(self):
        self.view.display_all_contacts(self.data)

    def show_help(self):
        self.view.display_help()
        
        
    def add_record(self,record):
        self.data[record.name.value] = record
        
        
    def find(self,value):
        if value in self.data.keys():
            return self.data[value]
        else:
            return None
        
        
    def delete(self,value):
        if value in self.data.keys():
            self.data.pop(value)
        else:
            print("Record not found")
            
    
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        end_date = today + timedelta(days=7)

        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)

                if today <= next_birthday <= end_date:
                    if next_birthday.weekday() == 5:  
                        next_birthday += timedelta(days=2)
                    elif next_birthday.weekday() == 6: 
                        next_birthday += timedelta(days=1)

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": next_birthday.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays
        
            
    def __str__(self):
        if not self.data:
            return "No contacts found"
        return '\n'.join([f"{record}" for key, record in self.data.items()])
    
    
