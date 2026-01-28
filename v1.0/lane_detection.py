import numpy as np
from statistics import mean


def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
    try:
        ys = []
        for line in lines:
            for coords in line:
                # [x1,y1,x2,y2]
                ys += [coords[1], coords[3]]
        # Getting min_y and max_y so that the line always ends at bottom of screen at resolution of 800x600 i.e. at 600
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        # finding x1 and x2 for the min_y and max_y with same slope and y-intercept
        for idx, i in enumerate(lines):
            for xyxy in i:
                # Getting x and y co-ordinates of the Hough Lines
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])

                # np.vstack().T with np.ones() makes matrix with x_coords in the first column and '1' in second column
                A = np.vstack([x_coords, np.ones(len(x_coords))]).T
                # getting slope 'm' and y-intercept b with least-square solution method.
                m, b = np.linalg.lstsq(A, y_coords)[0]

                # getting x1 and x2 from min_y and max_y with formula 'y = mx + b'
                x1 = (min_y - b) / m
                x2 = (max_y - b) / m

                # making line dictionary with slope, y-intercept and array of [x1, y1, x2, y2] with index as key.
                line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]

        # dictionary to store different slope lines with different keys and store similar slope keys under same index
        # index of the dict is its slope
        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            # adding first line if none is added to dictionary
            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]

            else:
                found_copy = False

                # other_ms iterates the keys that is slope in this case
                for other_ms in final_lanes_copy:
                    if not found_copy:
                        # if the new slope is not similar it is considered new line and added under new value of m
                        if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
                            # similar to slope the y-intercept is checked if it is similar
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(
                                    final_lanes_copy[other_ms][0][1] * 0.8):
                                # if the lines are similar the lines are appended in the existing array of key 'm'
                                final_lanes[other_ms].append([m, b, line])

                                # breaking loop if line is similar
                                found_copy = True
                                break
                        else:
                            # different lines are added in the dictionary under their respective slope as key
                            final_lanes[m] = [[m, b, line]]
        line_counter = {}

        for lanes in final_lanes:
            # checking how many lines are under 1 key and putting it in line_counter dictionary
            line_counter[lanes] = len(final_lanes[lanes])

        # assuming that the lane lines have highest number of lines we take the counter to measure number of lines in
        # each group of keys

        # taking 2 highest numbered lines. First sorting line_counter.items() in descending order with [::-1] and taking
        # items with highest 2 lines with [:2] -> first 2 array element
        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        # this is key value(m) of 2 lines taken in top_lanes
        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            # lane data is dictionary with key and value as { m : [m, b, [x1, y1, x2, y2]]}
            for data in lane_data:
                # taking x1, y1, x2, y2
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id

    except Exception as e:
        print(str(e))