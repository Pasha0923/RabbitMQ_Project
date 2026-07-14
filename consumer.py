import pika
import sys


def main():
    # credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.URLParameters('amqps://eohqpuez:DhXio2-yLN1NNxcTcynpeR_eYBRaRkOC@cow.rmq2.cloudamqp.com/eohqpuez')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello_world')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello_world', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
