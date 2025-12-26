import cv2
import numpy as np
import pandas as pd
import math


def get_dx_median(dx, x, y, w, h):
    return np.median(dx[y:(y + h), x])


def pre_process(img_path):
    img = cv2.imread(img_path, 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    rect_area = []
    rect_arc_length = []
    cnt_infos = {}

    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) < 5000 or cv2.contourArea(cnt) > 25000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cnt_infos[i] = {'rect_area': w * h,
                        'rect_arclength': 2 * (w + h),
                        'cnt_area': cv2.contourArea(cnt),
                        'cnt_arclength': cv2.arcLength(cnt, True),
                        'cnt': cnt,
                        'w': w,
                        'h': h,
                        'x': x,
                        'y': y,
                        'mean': np.mean(np.min(img[y:(y + h), x:(x + w)], axis=2)),
                        }
        rect_area.append(w * h)
        rect_arc_length.append(2 * (w + h))
    dx = cv2.Sobel(img, -1, 1, 0, ksize=5)

    return img, dx, cnt_infos


def tencent_mark_pos(img_path):
    img, dx, cnt_infos = pre_process(img_path)
    df = pd.DataFrame(cnt_infos).T
    df.head()
    df['dx_mean'] = df.apply(lambda x: get_dx_median(dx, x['x'], x['y'], x['w'], x['h']), axis=1)
    df['rect_ratio'] = df.apply(lambda v: v['rect_arclength'] / 4 / math.sqrt(v['rect_area'] + 1), axis=1)
    df['area_ratio'] = df.apply(lambda v: v['rect_area'] / v['cnt_area'], axis=1)
    df['score'] = df.apply(lambda x: abs(x['rect_ratio'] - 1), axis=1)

    result = df.query('x>0').query('area_ratio<2').query('rect_area>5000').query('rect_area<20000').sort_values(
        ['mean', 'score', 'dx_mean']).head(2)
    return result
