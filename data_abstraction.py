import cv2
import numpy as np
import pywt


def frame_to_haar_tree(frame):
    coeffs = pywt.wavedec2(frame, 'haar', level=int(np.log2(min(frame.shape))))
    return coeffs_to_tree(coeffs)


def coeffs_to_tree(coeffs):
    if len(coeffs) == 1:
        return [coeffs[0]]
    else:
        tree = []
        tree.append(coeffs[0])
        for detail_coeffs in coeffs[1:]:
            tree.extend(detail_coeffs)
        return tree


def tree_to_frame(tree, shape):
    coeffs = [tree[0]]
    details = tree[1:]
    levels = int(np.log2(min(shape)))
    for _ in range(levels):
        coeffs.append((details.pop(0), details.pop(0), details.pop(0)))
    frame = pywt.waverec2(coeffs, 'haar')
    return frame
