import connect
import json 
from models import Author, Quote


Author.ensure_indexes()
Quote.ensure_indexes()
with open("authors.json", encoding="utf-8") as file:
    authors = json.load(file)
for item in authors:
    Author(
        fullname=item["fullname"],
        born_date=item["born_date"],
        born_location=item["born_location"],
        description=item["description"]
    ).save()

with open ("quotes.json", encoding="utf-8") as file:
    qoutes = json.load(file)
for item in qoutes:
    author = Author.objects(fullname=item["author"]).first()
    if author:
        Quote(
            tags=item["tags"],
            author = author,
            quote = item["quote"]
        ).save()