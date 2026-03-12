import pika
import sys
import time
import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

def producer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    message = ' '.join(sys.argv[2:]) or "Hello World!"
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    print(f" [x] Sent '{message}'")
    connection.close()

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=callback)

    channel.start_consuming()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rabbitmq_example.py [producer|consumer] [message]")
        sys.exit(1)
    
    mode = sys.argv[1]
    if mode == "producer":
        producer()
    elif mode == "consumer":
        consumer()
    else:
        print("Invalid mode. Use 'producer' or 'consumer'.")
