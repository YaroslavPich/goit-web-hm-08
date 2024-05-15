from random import choice

import pika
from mongoengine import connect
from faker import Faker
from models import Contact

connect(db='send_email',
        host="mongodb+srv://userweb8:8426@cluster0.ue8ckn7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

fake = Faker()


def create_contacts(n):
	contacts = []
	for _ in range(n):
		contact = Contact(
			fullname=fake.name(),
			email=fake.email(),
			phone_number=f'+380{fake.msisdn()[4:]}',
			message_sent=False,
			sms_or_email=choice(['SMS', 'Email'])
		)
		contact.save()
		contacts.append(contact)
	return contacts


def contacts_in_queue(contacts):
	for contact in contacts:
		if contact.sms_or_email == 'SMS':
			queue_name = 'sms_queue'
		else:
			queue_name = 'email_queue'
		channel.basic_publish(
			exchange='',
			routing_key=queue_name,
			body=str(contact.id)
		)
	print(f'Send contact ID: {contact.id} to {queue_name}')


if __name__ == '__main__':
	n_contacts = 10
	contacts_all = create_contacts(n_contacts)
	contacts_in_queue(contacts_all)

	connection.close()
