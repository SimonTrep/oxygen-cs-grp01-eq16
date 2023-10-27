# pylint: disable=E1101

import logging
import json
import time
import os
from dbConnection import get_conn
from datetime import datetime
from dotenv import load_dotenv
from signalrcore.hub_connection_builder import HubConnectionBuilder
import requests

load_dotenv()


class Main:
    def __init__(self):
        """Setup environment variables and default values."""
        self._hub_connection = None
        self.HOST = os.getenv("HOST")  # Setup your host here
        self.TOKEN = os.getenv("TOKEN")  # Setup your token here

        self.TICKETS = os.getenv("TICKETS")  # Setup your tickets here
        self.T_MAX = os.getenv("T_MAX")  # Setup your max temperature here
        self.T_MIN = os.getenv("T_MIN")  # Setup your min temperature here

        self.dbConnection = get_conn()        

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        """Setup Oxygen CS."""
        self.set_sensorhub()

    def start(self):
        """Start Oxygen CS."""
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.", flush=True)
        while True:
            time.sleep(2)

    def set_sensorhub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(
            lambda: print("||| Connection opened.", flush=True)
        )
        self._hub_connection.on_close(
            lambda: print("||| Connection closed.", flush=True)
        )
        self._hub_connection.on_error(
            lambda data: print(
                f"||| An exception was thrown closed: {data.error}", flush=True
            )
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            temperature = float(data[0]["data"])
            self.save_data_to_database(date, temperature)
            self.take_action(temperature)
        except Exception as err:
            print(err, flush=True)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac("TurnOnHeater")

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKETS}")
        details = json.loads(r.text)
        print(details, flush=True)
        self.send_event_to_database(details)

    def send_event_to_database(self, event):
        """Save event into database."""
        try:
            cursor = self.dbConnection.cursor()
            current_datetime = datetime.now()
            cursor.execute("INSERT INTO hvacEvents (date, event) VALUES (?, ?)", current_datetime, str(event))
            self.dbConnection.commit()
            pass
        except Exception as e:
            print(e, flush=True)
            pass

    def save_data_to_database(self, timestamp, temperature):
        """Save sensor data into database."""
        try:
            cursor = self.dbConnection.cursor()
            cursor.execute("INSERT INTO temperatures (date, temperature) VALUES (?, ?)", datetime.fromisoformat(timestamp.split(".")[0]), temperature)
            self.dbConnection.commit()
            pass
        except Exception as e:
            print(e, flush=True)
            pass


if __name__ == "__main__":
    main = Main()
    main.start()
