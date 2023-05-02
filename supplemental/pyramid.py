import cv2


def build_laplacian_pyramid(image, levels):
    gaussian_pyramid = [image]
    for i in range(levels - 1):
        image = cv2.pyrDown(image)
        gaussian_pyramid.append(image)

    laplacian_pyramid = [gaussian_pyramid[-1]]
    # Store the original sizes of Gaussian images
    original_sizes = [image.shape[:2]]

    for i in range(levels - 1, 0, -1):
        size = (gaussian_pyramid[i - 1].shape[1],
                gaussian_pyramid[i - 1].shape[0])
        original_sizes.append(size)  # Store the size
        expanded_image = cv2.pyrUp(gaussian_pyramid[i], dstsize=size)
        laplacian_image = cv2.subtract(gaussian_pyramid[i - 1], expanded_image)
        laplacian_pyramid.append(laplacian_image)

    # Return the pyramid and original sizes
    return laplacian_pyramid, original_sizes[::-1]


def on_change(x):
    pass


def main():
    cap = cv2.VideoCapture('surf.mp4')
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps)

    max_levels = 5
    cv2.createTrackbar('Levels', 'Video', 0, max_levels, on_change)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        levels = cv2.getTrackbarPos('Levels', 'Video')

        laplacian_pyramid, _ = build_laplacian_pyramid(frame, levels)
        laplacian_frame = laplacian_pyramid[-1]

        for i in range(levels - 2, -1, -1):
            laplacian_frame = cv2.pyrUp(laplacian_frame)
            h, w, _ = laplacian_pyramid[i].shape
            laplacian_frame = cv2.add(
                laplacian_frame[:h, :w], laplacian_pyramid[i])

        cv2.imshow('Video', laplacian_frame)

        key = cv2.waitKey(delay) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
