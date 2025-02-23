#!/usr/bin/env python3
import pika
import time

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "testuser"
RABBITMQ_PASS = "passwd123"

try:
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    exchange_name = 'test_exchange'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    print(f"Exchange '{exchange_name}' declared successfully.")

    queue_name = 'test_queue'
    ttl_args = {'x-message-ttl': 3600000}
    channel.queue_declare(queue=queue_name, durable=True, arguments=ttl_args)
    print(f"Queue '{queue_name}' declared successfully.")
    channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key='')
    print(f"Queue '{queue_name}' bound to exchange '{exchange_name}'.")

    sample_messages = [
        "uno",
        "dos",
        "tres",
        "It just works"
    ]

    for msg in sample_messages:
        channel.basic_publish(exchange=exchange_name, routing_key='', body=msg)
        print(f"Sent: {msg}")
        time.sleep(1)

    connection.close()
    print("All messages sent. Connection closed.")

except Exception as e:
    print(f"ERROR: {e}")
