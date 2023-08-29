from confluent_kafka import Producer
import numpy as np
import time
from app.config import Config

np.random.seed(42)

N_SAMPLES = 20


class RandomSensorDataGenerator:
    """
    A generator for simulating random sensor data.

    This class is designed to produce random sensor data based on a Gaussian distribution with user-defined
    means and standard deviations. The generated data is returned as a comma-separated string of floating-point
    numbers rounded to two decimal places. For example: "1.24,45.67,18.45,..."
    """

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
    config = Config.get()
    producer = Producer(config)
    generator = RandomSensorDataGenerator(n_samples=N_SAMPLES)

    try:
        while True:
            sensor_data = generator.generate_data()
            producer.produce(
                "sensors",
                key=str(time.time()),
                value=sensor_data,
                callback=delivery_report,
            )
            producer.poll(0)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()


if __name__ == "__main__":
    main()
