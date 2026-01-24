import connect 
from models import Author,Quote



def main():
    print("Enter command (name:,tag:, tags:)")
    print("Enter exit to close program")

    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() == "exit":
            print("Exit from program")
            break
        if ":" not in user_input:
         print("Invalid command format. Please, use command:value")
         continue

        command,value = user_input.split(":", 1)
        command = command.strip().lower()
        value = value.strip()
        if command == "name":
           find_by_author(value)
        elif command == "tag":
           find_by_tag(value)
        elif command == "tags":
           find_by_tags(value)
        else:
           print("Unknown command. Enter command from list")




def find_by_author(user_author_name):
   author = Author.objects(fullname=user_author_name).first()
   if not author:
      print("Author not found")
      return
   quotes = Quote.objects(author=author)
   for q in quotes:
      print(f"{q.quote}")

def find_by_tag(user_tag):
   quotes = Quote.objects(tags=user_tag)
   if not quotes:
      print("No quotes contain this tag")
      return
   for q in quotes:
      print(f"{q.quote}")

def find_by_tags(user_tags):
    tags=user_tags.split(",")
    quotes = Quote.objects(tags__in=tags)
    if not quotes:
        print("No quotes contain this tags")
        return
    for q in quotes:  
       print(f"{q.quote}")
    

   
       
   
         
         
main()