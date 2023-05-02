# from numpy import zeros, ptp, mean, all, full_like, hstack, vstack
# import cv2


# class Qtree:
#     def __init__(self, image=None, level=0):
#         self.level = level
#         self.image = image
#         self.children = {}
#         self.range = zeros(3)

#     def insert(self, img, range=None, max_levels=None):

#         self.image = img

#         self.range = ptp(img, axis=(0, 1))

#         # Image was already made square so no need for any other dimension
#         h = img.shape[0]
#         half = h // 2

#         if h <= 1:
#             return

#         if range is not None and all(self.range <= range):
#             mean_color = mean(self.image, axis=(0, 1))
#             self.image = full_like(self.image, mean_color)
#             return

#         if max_levels is not None and self.level >= max_levels:
#             return

#         # Split the image into quadrants
#         quadrants = {
#             'northwest': img[:half, :half],
#             'northeast': img[:half, half:],
#             'southwest': img[half:, :half],
#             'southeast': img[half:, half:],
#         }

#         # Create child nodes and insert the corresponding quadrant
#         for name, quadrant in quadrants.items():
#             child_node = Qtree(img, level=self.level + 1)
#             child_node.insert(quadrant, range=range,
#                               max_levels=max_levels)
#             self.children[name] = child_node

#     def size(self):
#         count = 1
#         for child in self.children.values():
#             count += child.size()
#         return count

#     def print_tree(self, max_level=None):
#         if max_level is None or self.level <= max_level:
#             print(
#                 f"Level: {self.level}, Image shape: {self.image.shape}, Range: {self.range}")

#             for child in self.children.values():
#                 child.print_tree(max_level=max_level)

#     def show_images(self, min_level=0, max_level=None):
#         if max_level is None or min_level <= self.level <= max_level:
#             cv2.imshow(
#                 f"Level {self.level}, Image shape: {self.image.shape}, Range: {self.range}", self.image)
#             cv2.waitKey(0)

#             for child in self.children.values():
#                 child.show_images(max_level=max_level)

#         cv2.destroyAllWindows()

#     def reconstruct_image(self):
#         if not self.children:
#             return self.image

#         northwest = self.children['northwest'].reconstruct_image()
#         northeast = self.children['northeast'].reconstruct_image()
#         southwest = self.children['southwest'].reconstruct_image()
#         southeast = self.children['southeast'].reconstruct_image()

#         top = hstack((northwest, northeast))
#         bottom = hstack((southwest, southeast))
#         final = vstack((top, bottom))

#         return final

from numpy import zeros, ptp, mean, all, full_like, hstack, vstack
import cv2


class Qtree:
    def __init__(self, image=None, level=0):
        self.level = level
        self.image = image
        self.children = []
        self.range = zeros(3)

    def insert(self, img, range=None, max_levels=None):

        self.image = img

        self.range = ptp(img, axis=(0, 1))

        h = self.image.shape[0]
        half = h // 2

        if h <= 1:
            return

        if range is not None and all(self.range <= range):
            mean_color = mean(self.image, axis=(0, 1))
            self.image = full_like(self.image, mean_color)
            return

        if max_levels is not None and self.level >= max_levels:
            return

        # Split the image into quadrants
        quadrants = [
            img[:half, :half],
            img[:half, half:],
            img[half:, :half],
            img[half:, half:]
        ]

        # Create child nodes and insert the corresponding quadrant
        for quadrant in quadrants:
            child_node = Qtree(img, level=self.level + 1)
            child_node.insert(quadrant, range=range, max_levels=max_levels)
            self.children.append(child_node)

    def size(self):
        count = 1
        for child in self.children:
            count += child.size()
        return count

    def print_tree(self, max_level=None):
        if max_level is None or self.level <= max_level:
            print(
                f"Level: {self.level}, Image shape: {self.image.shape}, Range: {self.range}")

            for child in self.children:
                child.print_tree(max_level=max_level)

    def show_images(self, min_level=0, max_level=None):
        if max_level is None or min_level <= self.level <= max_level:
            cv2.imshow(
                f"Level {self.level}, Image shape: {self.image.shape}, Range: {self.range}", self.image)
            cv2.waitKey(0)

            for child in self.children:
                child.show_images(max_level=max_level)

        cv2.destroyAllWindows()

    def reconstruct_image(self):
        if not self.children:
            return self.image

        reconstructed_children = [child.reconstruct_image()
                                  for child in self.children]

        top = hstack((reconstructed_children[0], reconstructed_children[1]))
        bottom = hstack((reconstructed_children[2], reconstructed_children[3]))
        final = vstack((top, bottom))

        return final
