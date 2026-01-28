import cv2
import time
from grab_screen import grab_screen
from process_img import process_img
from gameinput import drive_with_lane_detection


def main():
    last_time = time.time()
    while True:
        screen = grab_screen(region=(0, 40, 800, 600))
        cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2HLS))
        # printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8')\
        # .reshape((printscreen_pil.size[1],printscreen_pil.size[0], 3))

        # for knowing FPS
        time1 = format(time.time() - last_time)
        print(f'Time: {time1}')
        print(f'FPS: {1 / float(time1)}')
        last_time = time.time()

        processed_img, org_image, m1, m2 = process_img(screen)

        # diplaying processed_img with openCV
        # cv2.imshow('window', processed_img)
        # diplaying original_img in RGB form with openCV
        # cv2.imshow('window2', cv2.cvtColor(org_image, cv2.COLOR_BGR2RGB))

        # driving with lane detection only (if-else)
        # drive_with_lane_detection(m1, m2)

        # exiting window if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()