from confluent_kafka import Consumer, KafkaError
import time

def main():
    # Kafka configuration - update this based on your setup
    conf = {
        'bootstrap.servers': '20.23.114.182:9094',  # Broker address
        'group.id': 'word_group',
        'auto.offset.reset': 'earliest',
        'security.protocol': 'ssl',
        'ssl.ca.location': '../ca.crt'
    }

    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe(['words_topic'])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error
                    print(f'Reached the end of partition {msg.partition()} at offset {msg.offset()}')
                else:
                    # Print out the error
                    print(f'Error while consuming message: {msg.error()}')
            else:
                # Proper message
                print(f'Received message (key: {msg.key()}): {msg.value()}')

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer
        consumer.close()

if __name__ == '__main__':
    main()