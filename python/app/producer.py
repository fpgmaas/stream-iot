from confluent_kafka import Producer
import time
import random

def delivery_report(err, msg):
    """
    Callback function after message delivery.
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def generate_random_word():
    """
    Generate a random word from a predefined list.
    """
    word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
    return random.choice(word_list)

def main():
    # Kafka configuration - update this based on your setup
    conf = {
        'bootstrap.servers': 'my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'  # Broker address
        # 'security.protocol': 'ssl',
        # 'ssl.ca.location': '../ca.crt'
    }

    producer = Producer(conf)

    try:
        while True:
            word = generate_random_word()
            producer.produce('words_topic', key=str(time.time()), value=word, callback=delivery_report)

            # Wait for any outstanding messages to be delivered and delivery reports to be received.
            producer.poll(0)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        # Wait for any outstanding messages to be delivered and delivery reports to be received.
        producer.flush()

if __name__ == '__main__':
    main()