import pika

from datetime import datetime
import sys
import json

# 1) ВАРИАНТ ПОДКЛЮЧЕНИЕ ЧЕРЕЗ ОБЛАКО https://api.cloudamqp.com/console/d5b0eae4-bc26-4d0f-b88a-1a846f070923/details ( RabbitMQ manager https://cow.rmq2.cloudamqp.com/#/)
# parameters = pika.URLParameters('amqps://eohqpuez:DhXio2-yLN1NNxcTcynpeR_eYBRaRkOC@cow.rmq2.cloudamqp.com/eohqpuez')
# connection = pika.BlockingConnection(parameters)

# 2) ВАРИАНТ ПОДКЛЮЧЕНИЕ ЧЕРЕЗ ЛОКАЛЬНЫЙ СЕРВЕР (RabbitMQ manager http://localhost:15672/#/)
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    for i in range(5):
        message = {
            "id": i + 1,
            "payload": f"Task #{i + 1}",
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()
    
    
if __name__ == '__main__':
    main()
