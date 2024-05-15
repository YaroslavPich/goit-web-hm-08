from mongoengine import connect, Document, StringField, BooleanField
connect(db='send_email', host="mongodb+srv://userweb8:8426@cluster0.ue8ckn7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


class Contact(Document):
	fullname = StringField(required=True)
	email = StringField(required=True)
	message_sent = BooleanField(required=False)
	phone_number = StringField()
	sms_or_email = StringField(choices=['SMS', 'Email'])

	meta = {'collection': 'contacts'}
