import cv2
import os
import numpy as np
import pywt
import pickle


def frame_to_haar_tree(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    coeffs = pywt.wavedec2(gray_frame, 'haar', level=int(
        np.log2(min(gray_frame.shape))))
    return coeffs


def haar_tree_to_image(coeffs):
    reconstructed_frame = pywt.waverec2(coeffs, 'haar').astype(np.uint8)
    return reconstructed_frame


def preprocess_video(video_path, haar_output_directory):
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        haar_tree = frame_to_haar_tree(frame)

        # Save Haar wavelet representation
        haar_output_path = os.path.join(
            haar_output_directory, f'haar_frame_{frame_count:04d}.pkl')
        with open(haar_output_path, 'wb') as f:
            pickle.dump(haar_tree, f)

        frame_count += 1

    cap.release()


def preprocess_frames():
    video_path = 'static/surf.mp4'
    haar_output_directory = 'static/haar_frames'
    os.makedirs(haar_output_directory, exist_ok=True)
    preprocess_video(video_path, haar_output_directory)
