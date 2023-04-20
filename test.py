import cv2
import os


def split_video_to_frames(video_path, output_directory):
    cap = cv2.VideoCapture(video_path)
    os.makedirs(output_directory, exist_ok=True)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        output_path = os.path.join(
            output_directory, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(output_path, gray_frame)

        frame_count += 1

    cap.release()


video_path = 'static/surf.mp4'
output_directory = 'frames'
split_video_to_frames(video_path, output_directory)
