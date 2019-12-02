import cv2
import numpy as np

hand_hist = None
hand_hist2 = None
hand_hist3 = None
hand_hist4 = None
traverse_point = []
total_rectangle = 9

total_hands = 0

hand_rects = [[None, None] for i in range(0, 4)]

hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

hand_rect_three_x = None
hand_rect_three_y = None

hand_rect_four_x = None
hand_rect_four_y = None

hand_rect_five_x = None
hand_rect_five_y = None

hand_rect_six_x = None
hand_rect_six_y = None

hand_rect_seven_x = None
hand_rect_seven_y = None

hand_rect_eight_x = None
hand_rect_eight_y = None


def rescale_frame(frame, wpercent=100, hpercent=100):
    width = int(frame.shape[1] * wpercent / 100)
    height = int(frame.shape[0] * hpercent / 100)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def contours(hist_mask_image):
    gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_hist_mask_image, 150, 255, 0)[1]
    cont = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    return cont


def max_contour(contour_list):
    max_i = 0
    max_area = 0

    for i in range(len(contour_list)):
        cnt = contour_list[i]

        area_cnt = cv2.contourArea(cnt)

        if area_cnt > max_area:
            max_area = area_cnt
            max_i = i

        return contour_list[max_i]


def draw_rect(frame):
    rows, cols, _ = frame.shape
    global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y

    hand_rect_one_x = np.array(
        [6 * rows / 20, 6 * rows / 20, 6 * rows / 20, 9 * rows / 20, 9 * rows / 20, 9 * rows / 20, 12 * rows / 20,
         12 * rows / 20, 12 * rows / 20], dtype=np.uint32)

    hand_rect_one_y = np.array(
        [9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20,
         10 * cols / 20, 11 * cols / 20], dtype=np.uint32)

    hand_rect_two_x = hand_rect_one_x + 10
    hand_rect_two_y = hand_rect_one_y + 10

    for i in range(total_rectangle):
        cv2.rectangle(frame, (hand_rect_one_y[i], hand_rect_one_x[i]),
                      (hand_rect_two_y[i], hand_rect_two_x[i]),
                      (0, 255, 0), 1)

    # # ///////////////////////////////////////////////////////////////
    #
    # hand_rect_three_x = np.array(
    #     [x2[0], x2[0], x2[0], x2[1], x2[1], x2[1], x2[2],
    #      x2[2], x2[2]], dtype=np.uint32)
    #
    # hand_rect_three_y = np.array(
    #     [y1[0], y1[1], y1[2], y1[0], y1[1], y1[2], y1[0],
    #      y1[1], y1[2]], dtype=np.uint32)
    #
    # hand_rect_four_x = hand_rect_three_x + 10
    # hand_rect_four_y = hand_rect_three_y + 10
    #
    # for i in range(total_rectangle):
    #     cv2.rectangle(frame, (hand_rect_three_x[i], hand_rect_three_y[i]),
    #                   (hand_rect_four_x[i], hand_rect_four_y[i]),
    #                   (0, 255, 0), 1)
    # # //////////////////////////////////////////////////////////////
    #
    # hand_rect_five_x = np.array(
    #     [x1[0], x1[0], x1[0], x1[1], x1[1], x1[1], x1[2],
    #      x1[2], x1[2]], dtype=np.uint32)
    #
    # hand_rect_five_y = np.array(
    #     [y2[0], y2[1], y2[2], y2[0], y2[1], y2[2], y2[0],
    #      y2[1], y2[2]], dtype=np.uint32)
    #
    # hand_rect_six_x = hand_rect_five_x + 10
    # hand_rect_six_y = hand_rect_five_y + 10
    #
    # for i in range(total_rectangle):
    #     cv2.rectangle(frame, (hand_rect_five_x[i], hand_rect_five_y[i]),
    #                   (hand_rect_six_x[i], hand_rect_six_y[i]),
    #                   (0, 255, 0), 1)
    # # ///////////////////////////////////////////////////////////////////////////////////////////
    #
    # hand_rect_seven_x = np.array(
    #     [x2[0], x2[0], x2[0], x2[1], x2[1], x2[1], x2[2],
    #      x2[2], x2[2]], dtype=np.uint32)
    #
    # hand_rect_seven_y = np.array(
    #     [y2[0], y2[1], y2[2], y2[0], y2[1], y2[2],
    #      y2[0],
    #      y2[1], y2[2]], dtype=np.uint32)
    #
    # hand_rect_eight_x = hand_rect_seven_x + 10
    # hand_rect_eight_y = hand_rect_seven_y + 10
    #
    # for i in range(total_rectangle):
    #     cv2.rectangle(frame, (hand_rect_seven_x[i], hand_rect_seven_y[i]),
    #                   (hand_rect_eight_x[i], hand_rect_eight_y[i]),
    #                   (0, 255, 0), 1)

    return frame


def hand_histogram(frame):
    global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y
    # , \
    #     hand_rect_three_x, hand_rect_three_y, hand_rect_four_x, hand_rect_four_y, hand_rect_five_x, hand_rect_five_y, \
    #     hand_rect_six_x, hand_rect_six_y, hand_rect_seven_x, hand_rect_seven_y, hand_rect_eight_x, hand_rect_eight_y

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

    for i in range(total_rectangle):
        roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10,
                                          hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # elif hand == 2:
    #     for i in range(total_rectangle):
    #         roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_three_x[i]:hand_rect_three_x[i] + 10,
    #                                           hand_rect_three_y[i]:hand_rect_three_y[i] + 10]
    #
    #     hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # elif hand == 3:
    #     for i in range(total_rectangle):
    #         roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_five_x[i]:hand_rect_five_x[i] + 10,
    #                                           hand_rect_five_y[i]:hand_rect_five_y[i] + 10]
    #
    #     hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # elif hand == 4:
    #     for i in range(total_rectangle):
    #         roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_seven_x[i]:hand_rect_seven_x[i] + 10,
    #                                           hand_rect_seven_y[i]:hand_rect_seven_y[i] + 10]
    #
    #     hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)


def hist_masking(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)

    # thresh = cv2.dilate(thresh, None, iterations=5)

    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(frame, thresh)


def centroid(max_contour):
    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        return cx, cy
    else:
        return None


def farthest_point(defects, contour, centroid):
    if defects is not None and centroid is not None:
        s = defects[:, 0][:, 0]
        cx, cy = centroid

        x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
        y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

        xp = cv2.pow(cv2.subtract(x, cx), 2)
        yp = cv2.pow(cv2.subtract(y, cy), 2)
        dist = cv2.sqrt(cv2.add(xp, yp))

        dist_max_i = np.argmax(dist)

        if dist_max_i < len(s):
            farthest_defect = s[dist_max_i]
            farthest_point = tuple(contour[farthest_defect][0])
            return farthest_point
        else:
            return None


def draw_circles(frame, traverse_point):
    if traverse_point is not None:
        for i in range(len(traverse_point)):
            cv2.circle(frame, traverse_point[i], int(5 - (5 * i * 3) / 100), [0, 255, 255], -1)


def manage_image_opr(frame, hand_hist):
    hist_mask_image = hist_masking(frame, hand_hist)
    contour_list = contours(hist_mask_image)
    max_cont = max_contour(contour_list)

    cnt_centroid = centroid(max_cont)
    cv2.circle(frame, cnt_centroid, 5, [255, 0, 255], -1)

    if max_cont is not None:
        hull = cv2.convexHull(max_cont, returnPoints=False)
        defects = cv2.convexityDefects(max_cont, hull)
        far_point = farthest_point(defects, max_cont, cnt_centroid)
        print("Centroid : " + str(cnt_centroid) + ", farthest Point : " + str(far_point))
        cv2.circle(frame, far_point, 5, [0, 0, 255], -1)
        if len(traverse_point) < 20:
            traverse_point.append(far_point)
        else:
            traverse_point.pop(0)
            traverse_point.append(far_point)

        draw_circles(frame, traverse_point)


def main():
    global hand_hist, hand_hist2, hand_hist3, hand_hist4
    is_hand_hist_created = False
    capture = cv2.VideoCapture(1)
    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    capture.set(cv2.CAP_PROP_EXPOSURE, -3)
    capture.set(cv2.CAP_PROP_BRIGHTNESS, 170)
    cropped_dimensions = [65, 378, 21, 620]

    while capture.isOpened():
        global total_hands
        pressed_key = cv2.waitKey(1)

        _, frame = capture.read()
        cropped_frame = frame[cropped_dimensions[0]:cropped_dimensions[1], cropped_dimensions[2]:cropped_dimensions[3]]

        if pressed_key & 0xFF == ord('z'):
            if total_hands == 0:
                hand_hist = hand_histogram(cropped_frame)
                total_hands += 1
            # elif total_hands == 1:
            #     hand_hist2 = hand_histogram(cropped_frame)
            #     total_hands += 1
            # elif total_hands == 2:
            #     hand_hist3 = hand_histogram(cropped_frame)
            #     total_hands += 1
            # elif total_hands == 3:
            #     hand_hist4 = hand_histogram(cropped_frame)
            #     total_hands += 1
                is_hand_hist_created = True

        if is_hand_hist_created:
            manage_image_opr(cropped_frame, hand_hist)
            # manage_image_opr(cropped_frame, hand_hist2)
            # manage_image_opr(cropped_frame, hand_hist3)
            # manage_image_opr(cropped_frame, hand_hist4)

        else:
            cropped_frame = draw_rect(cropped_frame)

        cv2.imshow("Live Feed", rescale_frame(cropped_frame))

        if pressed_key == 27:
            break

    cv2.destroyAllWindows()
    capture.release()


if __name__ == '__main__':
    main()
