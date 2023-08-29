from confluent_kafka import Consumer, KafkaError
from app.config import Config
import pymongo
import os
import datetime as dt


def parse_message_into_document(message: dict):
    """
    Parse a message received from Kafka and return a document to be stored in MongoDB.
    """
    document = parse_sensor_data(message.value().decode("utf-8"))
    timestamp = dt.datetime.fromtimestamp(float(message.key().decode("utf-8")))
    document["timestamp"] = timestamp
    document["timestamp_str"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return document


def parse_sensor_data(data_str: str):
    """
    Parse a comma-separated string of sensor values into a dictionary.

    Example:
    >>> parse_sensor_data("1,2,4")
    {'sensor_1': 1, 'sensor_2': 2, 'sensor_3': 4}
    """
    data_list = data_str.split(",")
    return {f"sensor_{idx+1}": float(value) for idx, value in enumerate(data_list)}


def main():
    """
    Consumes messages from Kafka and stores them into MongoDB.

    Note: This implementation processes messages one-by-one for simplicity. For higher throughput,
    consider batch processing to accumulate and insert messages in bulk.
    """

    # Connect to MongoDB
    mongodb_connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
    client = pymongo.MongoClient(mongodb_connection_string)
    db = client["streamiotcosmosdb"]
    collection = db.sensors

    # Set-up Kafka consumer
    config = Config.get()
    config["group.id"] = "sensor_group"
    consumer = Consumer(config)
    consumer.subscribe(["sensors"])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(
                        f"Reached the end of partition {msg.partition()} at offset {msg.offset()}"
                    )
                else:
                    print(f"Error while consuming message: {msg.error()}")
            else:
                print(f"Received message (key: {msg.key()}): {msg.value()}")
                document = parse_message_into_document(msg)
                collection.insert_one(document)

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer
        consumer.close()


if __name__ == "__main__":
    main()
