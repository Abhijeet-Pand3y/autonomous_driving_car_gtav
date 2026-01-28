import zmq
import json
import time
from datetime import datetime
import math


def subscribe_to_car_state():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    # Connect to the publisher
    subscriber.connect("tcp://127.0.0.1:1900")

    # Subscribe to the topic "car_state"
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "car_state")

    while True:
        # Receive the topic and message
        topic = subscriber.recv_string()
        message = subscriber.recv_string()

        # Check if the topic is "car_state"
        if topic == "car_state":
            # Parse the JSON message
            car_state = json.loads(message)

            output = [car_state['throttle_power'], car_state['brake_poner'], car_state['steering_angle']]

            print(car_state)

            # Handle the car state data as needed
            # print("Received Car State:", car_state)


# subscribe_to_car_state()


def zmq_connect():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    # Connect to the publisher
    subscriber.connect("tcp://127.0.0.1:1900")

    # Subscribe to the topic "car_state"
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "car_state")

    return subscriber


def get_car_state(subscriber):
    # Receive the topic and message
    topic = subscriber.recv_string()
    message = subscriber.recv_string()

    # Check if the topic is "car_state"
    if topic == "car_state":
        # Parse the JSON message
        car_state = json.loads(message)

        return car_state


def time_diff(before_time, current_time):
    before_time = before_time[:-1]
    current_time = current_time[:-1]

    # Split the string to separate seconds and microseconds
    seconds1, microseconds1 = before_time.split('.')
    seconds2, microseconds2 = current_time.split('.')

    # Convert strings to datetime objects
    datetime_obj1 = datetime.strptime(f"{seconds1}.{microseconds1[:6]}", "%Y-%m-%dT%H:%M:%S.%f")
    datetime_obj2 = datetime.strptime(f"{seconds2}.{microseconds2[:6]}", "%Y-%m-%dT%H:%M:%S.%f")

    # Calculate the time difference
    time_difference = datetime_obj2 - datetime_obj1

    return time_difference.total_seconds()


def calculate_acceleration(del_time, del_speed):
    acceleration = del_speed/del_time

    return acceleration


def process_state(car_state, before_time, before_speed):
    speed = car_state['speed']

    del_time = abs(time_diff(before_time, car_state['timestamp']))

    del_speed = speed - before_speed

    acceleration = calculate_acceleration(del_time, del_speed)

    output = [car_state['throttle_power'], car_state['brake_poner'], car_state['steering_angle']]

    return output, speed, acceleration

