import cv2
import numpy as np


def show_image(image, image_name='image'):
    """

    :param image: array with pixels to be dispayed
    :param image_name: default name of the image in the opened window
    """
    cv2.imshow(image_name, image)
    # wait for any key
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def fitness_f(original_img, new_img):
    """

    :param original_img: array with pixels of previous version of picture
    :param new_img:  array with pixels of generated new version of picture
    :return: fitness of new version related to previous (indicate whether new version is better )
    """
    return ((original_img.astype(float) - new_img.astype(float)) ** 2).sum()


def resize_image(img):
    """

    :param img: array with pixels of the picture of any size
    :return: resized image 512x512
    """
    img_size = (512, 512)
    height, width, chan_num = img.shape
    # to cut so that make the img square
    cut = (max(height, width) - min(height, width)) // 2
    if img.shape[:2] == img_size:
        if width > height:
            print(1)
            img = img[:, cut:-cut]
        elif width < height:
            print(2)
            img = img[cut:-cut, :]
            # compression
            resized_img = cv2.resize(img, img_size)
        else:
            resized_img = img.copy()
        return resized_img


# read paths to images that needed to be processed by the algorithm
# img = cv2.imread("pic2.png")
img_paths = ["pic2.png", "pic3.jpg", "pic4.jpg", "pic5.jpg"]
img_path_new = [i.replace('.', '-new.') for i in img_paths]
img_list = [cv2.imread(img_path) for img_path in img_paths]
img_list = [resize_image(img) for img in img_list if img is not None]

# show the list of new names for future generated pictures
img_path_new

# display all red images to assure that all paths were treated correct
for i in img_list:
    show_image(i)


def mutation(resized_img, save_path):
    """
    generates random circles of some radius, rgb and with a centre in (x,y),
    check whether new picture is more suitable than previous version, if so - change it

    :param resized_img: image(512x512) based on which the new image will be generated
    :param save_path: name for the generated image
    """
    # create a black picture on which the alg will generate new image
    new_img = np.zeros_like(resized_img)
    # calculate initial value if fitness function
    fit_f = fitness_f(resized_img, new_img)
    # do 3000 iterations(generations) - for 1 picture takes approximately 3 hours
    for i in range(3000):
        # at each iteration generate 100 variants of values for each of parametres:
        # x, y coordinates, circle radius, rgb
        x_s, y_s, r_s, red_s, green_s, blue_s = np.random.randint(0, 511, size=(6, 100), dtype=int)
        red_s = list(map(int, red_s // 2))
        green_s = list(map(int, green_s // 2))
        blue_s = list(map(int, blue_s // 2))
        # go through each of 100 sets of generated circles
        for x, y, r, red, green, blue in zip(x_s, y_s, r_s, red_s, green_s, blue_s):
            temp_img = cv2.circle(np.zeros_like(new_img), (x, y), r, (blue, green, red), -1).astype(float)
            temp_img = np.where(temp_img == 0, new_img, (new_img / 3 + 2.0 * temp_img / 3)).astype('uint8')
            temp_fit_f = fitness_f(resized_img, temp_img)
            # if new image fits to the ideal better, keep it
            if temp_fit_f < fit_f:
                new_img = temp_img
                fit_f = temp_fit_f
                print(temp_fit_f)
            print(i)
            cv2.imshow('frame', new_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # save the image
        cv2.imwrite(save_path, new_img)
        cv2.destroyAllWindows()

    for image, new_path in zip(img_list, img_path_new):
        mutation(image, new_path)
