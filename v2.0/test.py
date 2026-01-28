import cv2
import pandas as pd
import numpy as np
import os
import dill as pickle

# Load the DataFrame from the pickle file
# directory = r'C:\Users\abhij\OneDrive\Desktop\SDC\self-driving-car\v2.0\training_data'
# file_name = 'a_training_data2.pkl'
# file_index = 1
# file_path = os.path.join(directory, file_name)
data = pd.read_pickle(r'D:\training_data\a_training_data56.pkl')
#
# with open(r'C:\Users\abhij\OneDrive\Desktop\SDC\self-driving-car\v2.0\training_data\a_training_data2.pkl', 'rb+') as f:
#     data = pickle.load(f)

# Extract the 'screen' column
imgs = data['screen']
outputs = data['output']

throtle = 0
breaking = 0
steering = 0

for i in range(len(data)):
    img = imgs[i].astype(np.uint8)
    output = outputs[i]
    if output[0] != 0:
        throtle += 1
    if output[1] != 0:
        breaking += 1
    if output[2] != 0:
        steering += 1

    cv2.imshow("tes", img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break  # Break the loop on 'q' key press
print(throtle)
print(breaking)
print(steering)
# for img_array in imgs:
#     img = img_array.astype(np.uint8)
#     cv2.imshow("tes", img)
#     # print()
#
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break  # Break the loop on 'q' key press
