# Public Transit Status with Apache Kafka

## Running and Testing

To run the simulation, you must first start up the Kafka ecosystem on their machine utilizing Docker Compose.

```%> docker-compose up```

Docker compose will take a 3-5 minutes to start, depending on your hardware. Please be patient and wait for the docker-compose logs to slow down or stop before beginning the simulation.

Once docker-compose is ready, the following services will be available:

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

Note that to access these services from your own machine, you will always use the `Host URL` column.

When configuring services that run within Docker Compose, like **Kafka Connect you must use the Docker URL**. When you configure the JDBC Source Kafka Connector, for example, you will want to use the value from the `Docker URL` column.

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