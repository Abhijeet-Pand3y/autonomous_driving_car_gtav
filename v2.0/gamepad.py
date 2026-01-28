from inputs import get_gamepad
# import inputs

# event-code
# LT(break) -  ABS_Z
# RT(acceleration)  -  ABS_RZ
# Left Stick(left/right)  -  ABS_X

output = [0, 0, 0]
# while True:
#     # [ left/right, acceleration, break]
#     events = get_gamepad()
#
#     if event.code == "BTN_SOUTH":
#         break


def give_output(events):
    for event in events:
        if event.code == "ABS_X":
            output[0] = int(event.state)/32768
            # print(f"Event Type: {event.ev_type}\nEvent Code: {event.code}\nEvent State: {int(event.state)/32768}\n")

        elif event.code == "ABS_RZ":
            output[1] = int(event.state)/255

        elif event.code == "ABS_Z":
            output[2] = int(event.state)/255

        return output


while True:
    events = get_gamepad()
    op = give_output(events)
    print(op)