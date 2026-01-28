import mss
from win32gui import FindWindow, GetWindowRect, SetForegroundWindow
from PIL import ImageGrab
import torch
import cv2 as cv
import numpy as np
from time import time, sleep

from utils.utils import letterbox, driving_area_mask, lane_line_mask, \
    split_for_trace_model, non_max_suppression, plot_one_box, scale_coords, clip_coords

window_handle = FindWindow(None, "Grand Theft Auto V")
window_rect = GetWindowRect(window_handle)
SetForegroundWindow(window_handle)

x0, y0, x1, y1 = window_rect
x_corr = 6
y_corr = 29
w, h = x1 - x0 - x_corr, y1 - y0 - y_corr


def Screen_Shot(left=0, top=40, width=800, height=600):
    # stc = mss.mss()
    # scr = stc.grab({
    #     'left': left,
    #     'top': top,
    #     'width': width,
    #     'height': height
    # })
    #
    # img = np.array(scr)
    # img = cv.cvtColor(img, cv.IMREAD_COLOR)

    src = ImageGrab.grab(bbox=(0, 40, 800, 600))

    img = np.array(src)
    img = cv.cvtColor(img, cv.IMREAD_COLOR)

    return img


model_file_path = r"C:\Users\abhij\OneDrive\Desktop\SDC\YOLOPv2\data\weights\yolopv2.pt"
model = torch.jit.load(model_file_path)
model.cuda()
model.half()
model.eval()

imgsz = 640
model(torch.zeros(1, 3, imgsz, imgsz).cuda().type_as(next(model.parameters())))

loop_time = time()
with torch.no_grad():
    while (True):

        screenshot = Screen_Shot(x0 + x_corr, y0 + y_corr, w, h)

        img0 = screenshot.copy()
        img = cv.resize(img0, (640, 480), interpolation=cv.INTER_NEAREST)

        output = img.copy()
        out_w, out_h = output.shape[1], output.shape[0]

        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).cuda()
        img = img.float().half()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        [pred, anchor_grid], seg, ll = model(img)

        masking = True
        obj_det = True

        if masking:
            da_seg_mask = seg
            _, da_seg_mask = torch.max(da_seg_mask, 1)
            da_seg_mask = da_seg_mask.int().squeeze().cpu().numpy()

            ll_seg_mask = ll
            ll_seg_mask = torch.round(ll_seg_mask).squeeze(1)
            ll_seg_mask = ll_seg_mask.int().squeeze().cpu().numpy()

            color_area = np.zeros((da_seg_mask.shape[0], da_seg_mask.shape[1], 3), dtype=np.uint8)

            color_area[da_seg_mask == 1] = [0, 255, 0]
            color_area[ll_seg_mask == 1] = [255, 0, 0]
            color_seg = color_area
            color_seg = color_seg[..., ::-1]
            color_mask = np.mean(color_seg, 2)
            output[color_mask != 0] = output[color_mask != 0] * 0.5 + color_seg[color_mask != 0] * 0.5

        if obj_det:
            pred = split_for_trace_model(pred, anchor_grid)
            pred = non_max_suppression(pred)
            pred0 = pred[0]

            img0_shape = output.shape
            clip_coords(pred0, img0_shape)

            for det in pred0:
                *xyxy, _, _ = det
                plot_one_box(xyxy, output)

        cv.imshow("YOLOPv2", output)

        print("FPS {}".format(1.0 / (time() - loop_time)))
        loop_time = time()
        key = cv.waitKey(5)
        if key == ord("q"):
            cv.destroyAllWindows()
            break