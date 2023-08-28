from confluent_kafka import Producer
import numpy as np
import time

np.random.seed(42)

N_SAMPLES = 20


class RandomSensorDataGenerator:
    def __init__(self, n_samples: int):
        self.n_samples = n_samples
        self.means = np.random.uniform(10, 90, N_SAMPLES)
        self.std_devs = np.random.uniform(1, 10, N_SAMPLES)

    def generate_data(self):
        random_numbers = np.random.normal(self.means, self.std_devs)
        clipped_numbers = np.clip(random_numbers, 0, 100)
        rounded_numbers = np.round(clipped_numbers, 2)
        result_string = ",".join(map(str, rounded_numbers))
        return result_string


def delivery_report(err, msg) -> None:
    """
    Callback function after message delivery.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def main():
    generator = RandomSensorDataGenerator(n_samples=N_SAMPLES)

    conf = {
        "bootstrap.servers": "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092",
    }

    producer = Producer(conf)

    try:
        while True:
            sensor_data = generator.generate_data()
            producer.produce(
                "sensors",
                key=str(time.time()),
                value=sensor_data,
                callback=delivery_report,
            )
            # Wait for any outstanding messages to be delivered and delivery reports to be received.
            producer.poll(0)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        # Wait for any outstanding messages to be delivered and delivery reports to be received.
        producer.flush()


if __name__ == "__main__":
    main()
