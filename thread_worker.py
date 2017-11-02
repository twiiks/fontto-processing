import threading, pika, logging, json


class ThreadWorker(threading.Thread):
    def __init__(self, amqp_url, queue, thread_num):
        print(thread_num, "run")
        super().__init__()
        self.amqp_url = amqp_url
        self.thread_num = thread_num
        self.queue = queue
        self.channel = None

    def run(self):
        connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

        self.channel.basic_consume(self.processing_callback, queue=self.queue, no_ack=True)
        logging.info('fontto-processing started!')
        self.channel.start_consuming()

    def processing_callback(self, ch, method, properties, body):
        logging.info("%s" % self.thread_num)
        logging.info("received %r" % body)

        received_message = json.loads(body.decode('utf8').replace("'", '"'))

        # you can use like this
        # received_message['userId']
        # received_message['count']
        # received_message['unicodes']

        received_message_dumps = json.dumps(received_message, indent=4)
        print(received_message_dumps)

        # processing...........
