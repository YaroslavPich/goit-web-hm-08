from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(db='homework',
        host="mongodb+srv://userweb8:8426@cluster0.ue8ckn7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


class Author(Document):
	fullname = StringField(required=True, unique=True)
	born_date = StringField(max_length=50)
	born_location = StringField(max_length=150)
	description = StringField()
	meta = {"collection": "authors"}


class Quote(Document):
	author = ReferenceField(Author, reverse_delete_rule=CASCADE)
	tags = ListField(StringField(max_length=15))
	quote = StringField()
	meta = {"collection": "quotes"}
