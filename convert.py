import cv2
import os
import math


def convert_video(video_path, dest_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Create the frames directory if it doesn't exist
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    ret, frame = cap.read()

    # Get first frame to get the final size that will work nicely for the quad tree structure
    if ret:
        total_pixels = frame.shape[0] * frame.shape[1]
        depth = int(math.log(total_pixels, 4))
        size = 2 ** depth
    count = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the height to 1024
        height, width, _ = frame.shape
        ratio = size / height
        frame = cv2.resize(frame, (int(width * ratio), int(height * ratio)))

        # Crop the sides of the width evenly to make it 1024x1024
        height, width, _ = frame.shape
        delta = (width - size) // 2
        frame = frame[:, delta:delta+size]

        # Save the resized frame with the file name in the format frame_0000.jpg
        filename = f"{dest_path}/frame_{str(count).zfill(4)}.jpg"
        cv2.imwrite(filename, frame)

        count += 1

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


def resize_video(input_video_path, output_video_path, new_size):
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Get the video's original properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculate the new dimensions
    new_width = new_size
    new_height = new_size

    # Initialize the VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc,
                          fps, (new_width, new_height))

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:
            break

        # Resize and crop the frame
        ratio = new_size / height
        frame = cv2.resize(frame, (int(width * ratio), int(height * ratio)))
        delta = (frame.shape[1] - new_size) // 2
        frame = frame[:, delta:delta+new_size]

        # Write the resized frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
