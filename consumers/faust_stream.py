"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# Define a Faust Stream that ingests data from the Kafka Connect stations topic and
# places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")

# Input topic
topic = app.topic("jdbc.stations", value_type=Station)

# Output topic
out_topic = app.topic("output.faust.stations", partitions=1)

table = app.Table(
    "output.faust.stations",
    default=TransformedStation,
    partitions=1,
    changelog_topic=out_topic,
)


# Using Faust, transform input `Station` records into `TransformedStation` records.
@app.agent(topic)
async def transform(stations):

    async for station in stations:
        
        if station.red:
            line = 'red'
        elif station.blue:
            line = 'blue'
        elif station.green:
            line = 'green'
        else:
            logger.debug(f"Can't parse line color with station_id = {station.station_id}")
            line = ''

        transformed_station = TransformedStation(
            station_id=station.station_id,
            station_name=station.station_name,
            order=station.order,
            line=line
        )
        
        table[station.stop_id] = transformed_station
        logger.info(f"Station %s transformed ", station.station_name)

if __name__ == "__main__":
    app.main()