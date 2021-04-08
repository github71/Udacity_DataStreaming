# Public Transit Status with Apache Kafka

## Running and Testing

To run the simulation, you must first start up the Kafka ecosystem in the udacity terminal, there is an option to use the docker but we will not follow it on this occasion.

The following services will be available:

| Service | Host URL | Username | Password |
| --- | --- | --- | --- |
| Public Transit Status | [http://localhost:8888](http://localhost:8888) 
| Landoop Kafka Connect UI | [http://localhost:8084](http://localhost:8084)
| Landoop Kafka Topics UI | [http://localhost:8085](http://localhost:8085)
| Landoop Schema Registry UI | [http://localhost:8086](http://localhost:8086)
| Kafka | PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094
| REST Proxy | [http://localhost:8082](http://localhost:8082/) 
| Schema Registry | [http://localhost:8081](http://localhost:8081/ )
| Kafka Connect | [http://localhost:8083](http://localhost:8083) 
| KSQL | [http://localhost:8088](http://localhost:8088) 
| PostgreSQL | `jdbc:postgresql://localhost:5432/cta` |  `cta_admin` | `chicago` |

### Running the Simulation

There are two pieces to the simulation, the `producer` and `consumer`. As you develop each piece of the code, it is recommended that you only run one piece of the project at a time.

However, when you are ready to verify the end-to-end system prior to submission, it is critical that you open a terminal window for each piece and run them at the same time. **If you do not run both the producer and consumer at the same time you will not be able to successfully complete the project**.

#### To run the `producer`:

1. `cd producers`
2. `python simulation.py`

Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

#### To run the Faust Stream Processing Application:
1. `cd consumers`
2. `faust -A faust_stream worker -l info`


#### To run the KSQL Creation Script:
1. `cd consumers`
2. `python ksql.py`

#### To run the `consumer`:

** NOTE **: Do not run the consumer until you have reached Step 6!
1. `cd consumers`
2. `python server.py`

Once the server is running, you may hit `Ctrl+C` at any time to exit.

## Viewing the output
 When running through the terminal it will not be possible to view the webpage , the following command will provide access to the data:
 
curl http://localhost:[PORT] > index.html where [PORT] is defined by WEB_SERVER_PORT in the consumers/server.py file

## Kafka command line
#### view stations coming through the Kafka connect topic:
kafka-console-consumer --bootstrap-server "kafka://localhost:9092" --topic "org.chicago.cta.jdbc.stations" --from-beginning
#### view stations coming through the Faust topic:
kafka-console-consumer --bootstrap-server "kafka://localhost:9092" --topic "org.chicago.cta.stations" --from-beginning
#### view stations coming through the Turnstile topic:
kafka-console-consumer --bootstrap-server "kafka://localhost:9092" --topic "TURNSTILE_SUMMARY" --from-beginning
#### view all topics
kafka-topis --list --zookeepr localhost:2181
#### view all turnstile messages
kafka-avro-console-consumer --topic org.chicago.cta.turnstile --bootstrap-server localhost:9092 --max-messages 100
#### view all weather messages
kafka-avro-console-consumer --topic org.chicago.cta.weather --from-beginning --bootstrap-server localhost:9092 --max-messages 100
#### view all stations info in postgres
kafka-console-consumer --topic org.chicago.cta.jdbc.stations --from-beginning --bootstrap-server localhost:9092 --max-messages 250

## Faust checks
#### tables
python faust_stream.py tables
#### transformed tables
kafka-console-consumer --topic org.chicago.cta.stations --from-beginning --bootstrap-server localhost:9092 --max-messages 250