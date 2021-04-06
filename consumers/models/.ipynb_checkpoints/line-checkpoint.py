"""Contains functionality related to Lines"""
import json
import logging

from models import Station


logger = logging.getLogger(__name__)


class Line:
    """Defines the Line Model"""

    def __init__(self, color):
        """Creates a line"""
        self.color = color
        self.color_code = "0xFFFFFF"
        if self.color == "blue":
            self.color_code = "#1E90FF"
        elif self.color == "red":
            self.color_code = "#DC143C"
        elif self.color == "green":
            self.color_code = "#32CD32"
        self.stations = {}
        logger.info('in line %s init', color)

    def _handle_station(self, value):
        """Adds the station to this Line's data model"""
        if value["line"] != self.color:
            return
        self.stations[value["station_id"]] = Station.from_message(value)
        logger.info('in handle station')

    def _handle_arrival(self, message):
        """Updates train locations"""
        logger.info('        in line handle arrivals')
        value = message.value()
        prev_station_id = value.get("prev_station_id")
        prev_dir = value.get("prev_direction")
        if prev_dir is not None and prev_station_id is not None:
            prev_station = self.stations.get(prev_station_id)
            if prev_station is not None:
                prev_station.handle_departure(prev_dir)
            else:
                logger.info("unable to handle previous station due to missing station")
        else:
            logger.info(
                "unable to handle previous station due to missing previous info"
            )

        station_id = value.get("station_id")
        station = self.stations.get(station_id)
        if station is None:
            logger.info("unable to handle message due to missing station")
            return
        station.handle_arrival(
            value.get("direction"), value.get("train_id"), value.get("train_status")
        )
        

    def process_message(self, message):
        """Given a kafka message, extract data"""
        # Based on the message topic, call the appropriate handler.
        logger.info('in line process message')
        if message.topic() == "output.faust.station": # Set the conditional correctly to the stations Faust Table
            logger.info('    in output faust')
            try:
                value = json.loads(message.value())
                self._handle_station(value)
            except Exception as e:
                logger.info("bad station? %s, %s", value, e)
        elif message.topic().startswith("org.chicago.cta.station.arrivals"): # Set the conditional to the arrival topic
            logger.info('    in line station arrivals')
            self._handle_arrival(message)
        elif message.topic() == "TURNSTILE_SUMMARY": # Set the conditional to the KSQL Turnstile Summary Topic
            logger.info('    in turnstile summary')
            json_data = json.loads(message.value())
            station_id = json_data.get("STATION_ID")
            station = self.stations.get(station_id)
            if station is None:
                logger.info("unable to handle message due to missing station")
                return
            station.process_message(json_data)
        else:
            logger.info(
                "unable to find handler for message from topic %s", message.topic()
            )