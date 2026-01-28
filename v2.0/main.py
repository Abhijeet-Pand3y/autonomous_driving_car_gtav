from grab_screen import grab_screen
import time
import cv2
from gamestate_subscriber import process_state, zmq_connect, get_car_state
import os
import numpy as np
from datetime import datetime, timezone
import pandas as pd

def main():
    #
    directory = r'D:\training_data'
<<<<<<< HEAD
    file_name = 'a_training_data1.pkl'
=======
    file_name = 'c_training_data1.pkl'
>>>>>>> 4a0de5fd441f173278e0378b802e1e5cf04afe35
    file_index = 1
    file_path = os.path.join(directory, file_name)

    while os.path.isfile(file_path):
        file_index += 1
        directory = r'D:\training_data'
<<<<<<< HEAD
        file_name = 'a_training_data' + str(file_index) + '.pkl'
=======
        file_name = 'c_training_data' + str(file_index) + '.pkl'
>>>>>>> 4a0de5fd441f173278e0378b802e1e5cf04afe35
        file_path = os.path.join(directory, file_name)

    columns = ['screen', 'speed', 'acceleration', 'output']
    training_data = pd.DataFrame(columns=columns)

    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()

    subscriber = zmq_connect()

    j = 0
    i = 0
    while True:
        j += 1
        if i != 0:
            before_speed = speed
            before_time = car_state['timestamp']
        else:
            before_time = datetime.utcnow()
            before_time = before_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            before_speed = 0
            i = 1

        subscriber = zmq_connect()
        car_state = get_car_state(subscriber)

        screen = grab_screen(region=(0, 40, 1280, 720))

        time1 = format(time.time() - last_time)
        # print(f'Time: {time1}')
        # print(f'FPS: {1 / float(time1)}')
        last_time = time.time()

        # screen = cv2.resize(screen, (480, 270))

        # Output -> [throttle_power, break_power, steering_angle]
        output, speed, acceleration = process_state(car_state, before_time, before_speed)

        # print(f"Speed = {speed} Throttle Power = {output[0]} Break State = {output[1]} Steering Angle = {output[2]} "
        #       f"Acceleration = {acceleration}")

<<<<<<< HEAD
        if j % 3 == 0:
=======
        if j % 4 == 0:
>>>>>>> 4a0de5fd441f173278e0378b802e1e5cf04afe35
            new_data = {'screen': screen, 'speed': speed, 'acceleration': acceleration, 'output': output}
            if len(training_data) == 0:
                training_data = pd.DataFrame([new_data])
            else:
                training_data = pd.concat([training_data, pd.DataFrame([new_data])], ignore_index=True)

            if len(training_data) % 100 == 0 and len(training_data) != 0:
                print(len(training_data))
                print("saved")
                with open(file_path, 'wb') as f:
                    training_data.to_pickle(f)

            if len(training_data) == 2000:

                while os.path.isfile(file_path):
                    file_index += 1
                    directory = r'D:\training_data'
<<<<<<< HEAD
                    file_name = 'a_training_data' + str(file_index) + '.pkl'
=======
                    file_name = 'c_training_data' + str(file_index) + '.pkl'
>>>>>>> 4a0de5fd441f173278e0378b802e1e5cf04afe35
                    file_path = os.path.join(directory, file_name)

                columns = ['screen', 'speed', 'acceleration', 'output']
                training_data = pd.DataFrame(columns=columns)

        subscriber.close()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()


