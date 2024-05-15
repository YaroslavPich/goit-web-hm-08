import pika
from mongoengine import connect
from models import Contact
import time

connect(db='send_email',
        host="mongodb+srv://userweb8:8426@cluster0.ue8ckn7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')


def send_email(contact):
	print(f"Send email to {contact.email}")
	time.sleep(1)
	contact.message_sent = True
	contact.save()
	print(f"Email send to {contact.email}")


def callback(ch, method, body):
	contact_id = body.decode()
	try:
		contact = Contact.objects.get(id=contact_id)
		send_email(contact)
	except Exception:
		print(f"No contact {contact_id}")
	ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
	channel.basic_consume(queue='email_queue', on_message_callback=callback)
	print("Waiting for messages. To exit press CTRL+C")
	channel.start_consuming()
