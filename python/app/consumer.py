from confluent_kafka import Consumer, KafkaError
from app.config import Config
import pymongo
import os


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
    COSMOSDB_CONNECTION_STRING = os.environ.get("COSMOSDB_CONNECTION_STRING")
    print(COSMOSDB_CONNECTION_STRING[:20])
    client = pymongo.MongoClient(COSMOSDB_CONNECTION_STRING)
    db = client["floapp001cosmosdb"]
    collection = db.sensors

    config = Config.get()
    config["group.id"] = "sensor_group"
    consumer = Consumer(config)

    # Subscribe to the topic
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
                document = parse_sensor_data(msg.value().decode("utf-8"))
                collection.insert_one(document)

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer
        consumer.close()


if __name__ == "__main__":
    main()
