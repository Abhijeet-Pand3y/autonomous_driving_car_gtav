import zmq
import time
import json
import socketio

def socketio_client_conn():
    sio = socketio.Client()
    sio.connect('http://localhost:8000')

    @sio.on('to_client_c')
    def on_message(data):
        print(data)
        simulate_coordinate_publisher(data)


def simulate_coordinate_publisher(data):

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)

    # Bind to the same address that the C# subscriber uses
    publisher.bind("tcp://127.0.0.1:1880")

    try:
        while True:
            # Simulate some x and y coordinates (replace this with your actual logic)
            x_coordinate = data['X']
            y_coordinate = data['Y']
            print(data)

            # Publish the coordinates as a JSON string
            coordinates = {"x": x_coordinate, "y": y_coordinate}
            publisher.send_multipart([b"coordinates", json.dumps(coordinates).encode()])

            # Simulate a delay between updates
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        publisher.close()
        context.term()


if __name__ == "__main__":
    socketio_client_conn()
