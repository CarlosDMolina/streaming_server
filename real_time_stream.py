import cv2
from quadtree import *
from concurrent.futures import ProcessPoolExecutor


def process_frames(frame, range):
    qtree = Qtree()
    qtree.insert(frame, range=range)
    processed_frame = qtree.reconstruct_image()
    return processed_frame


def process_frame(args):
    frame, range = args
    return process_frames(frame, range)


def on_change(x):
    pass


def main():
    video = 'surf_square.mp4'
    title = "Video Streaming Server"
    trackbar = "Bandwidth"

    cap = cv2.VideoCapture(video)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps)

    frame_size = 512

    cv2.namedWindow(title,
                    cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(title, frame_size, frame_size)

    max_range = 100
    cv2.createTrackbar(trackbar, title,
                       100, max_range, on_change)

    executor = ProcessPoolExecutor()

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        range = 100 - cv2.getTrackbarPos(trackbar, title)

        frame = cv2.resize(frame, (frame_size, frame_size))

        future = executor.submit(process_frame, (frame, range))
        qtree_frame = future.result()

        cv2.imshow(title, qtree_frame)

        key = cv2.waitKey(delay) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
