import pika


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    # credentials = pika.PlainCredentials('guest', 'guest')
    # parameters = pika.URLParameters('amqps://eohqpuez:DhXio2-yLN1NNxcTcynpeR_eYBRaRkOC@cow.rmq2.cloudamqp.com/eohqpuez')
    # connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    channel.queue_declare(queue='hello_world')
    
    channel.basic_publish(exchange='', routing_key='hello_world', body='Hello world!'.encode())
    print(" [x] Sent 'Hello World!'")
    connection.close()
    

if __name__ == '__main__':
    main()