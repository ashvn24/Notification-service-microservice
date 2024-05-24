import json
import os
import django
import pika
import logging
import signal
import sys
import time
from pika.exceptions import AMQPConnectionError, AMQPError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Notification.settings")

# Configure Django settings
django.setup()
from service.models import Notification

# Set up connection parameters
params = pika.URLParameters('amqps://hjbmtads:qOh03ewMbJOTgf_g2osT6DpZp7UFVqcj@puffin.rmq2.cloudamqp.com/hjbmtads')

connection = None
channel = None
should_reconnect = True

def connect():
    global connection, channel
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='main')
        logger.info("Connected to RabbitMQ")
    except AMQPConnectionError as e:
        logger.error(f"Connection failed: {e}")
        time.sleep(5)
        connect()

def callback(ch, method, properties, body):
    logger.info('Received in main')
    data = json.loads(body)
    print(data)
    print(properties)
    notification = Notification.objects.create(content=data['content'], type=data['type'])
    notification.save()
    print('saved')
def start_consuming():
    global channel
    try:
        channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
        logger.info('Started consuming')
        channel.start_consuming()
    except AMQPError as e:
        logger.error(f"Consuming failed: {e}")
        if should_reconnect:
            reconnect()

def reconnect():
    global connection, channel
    logger.info("Reconnecting...")
    if connection and not connection.is_closed:
        connection.close()
    connect()
    start_consuming()

def shutdown(signal, frame):
    global should_reconnect
    should_reconnect = False
    if connection and not connection.is_closed:
        connection.close()
    logger.info("Consumer stopped")
    sys.exit(0)

# Handle termination signals to gracefully shut down
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

if __name__ == "__main__":
    connect()
    start_consuming()
