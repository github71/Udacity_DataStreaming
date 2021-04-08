"""Producer base-class providing common utilities and functionality"""
import logging
import time

from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer, CachedSchemaRegistryClient

logger = logging.getLogger(__name__)

SCHEMA_REGISTRY_URL = "http://localhost:8081"
BROKER_URL = "PLAINTEXT://localhost:9092"


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
            self,
            topic_name,
            key_schema,
            value_schema=None,
            num_partitions=1,
            num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        self.broker_properties = {
            "bootstrap.servers": BROKER_URL,
            "schema.registry.url": SCHEMA_REGISTRY_URL
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = AvroProducer(self.broker_properties,
                                     default_key_schema=self.key_schema,
                                     default_value_schema=self.value_schema)

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""

        client = AdminClient({"bootstrap.servers": BROKER_URL})
        topic_metadata = client.list_topics(timeout=5)

        if self.topic_name in set(
                t.topic for t in iter(topic_metadata.topics.values())
        ):
            logger.debug("not recreating existing topic %s", self.topic_name)
            return

        client.create_topics([NewTopic(self.topic_name,
                                       num_partitions=self.num_partitions,
                                       replication_factor=self.num_replicas)
                              ])
        logger.debug("created new topic %s", self.topic_name)

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""

        self.producer.flush()

    @staticmethod
    def time_millis():
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
