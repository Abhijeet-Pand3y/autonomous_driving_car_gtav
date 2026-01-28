import zmq
import json
import socketio



def subscribe_to_playerpos():

    sio = socketio.Client()
    sio.connect('http://localhost:8000')

    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)


    # Connect to the publisher
    subscriber.connect("tcp://127.0.0.1:1810")

    # Subscribe to the topic "player_coords"
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "player_coords")

    while True:
        # Receive the topic and message
        topic = subscriber.recv_string()
        message = subscriber.recv_string()
        # Check if the topic is "player_coords"
        if topic == "player_coords":
            # Parse the JSON message
            playerpos = json.loads(message)

            sio.emit('from_client_b', playerpos)
            # Handle the player position data as needed
            print("Received Player Position:", playerpos)


if __name__ == "__main__":
    subscribe_to_playerpos()
