import glob
import random
import os
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
import Augmentor

def img_flip():
    path = ""
    img = cv2.imread(path)

    horizontal_img = img.copy()
    vertical_img = img.copy()
    both_img = img.copy()

    horizontal_img = cv2.flip(img, 0)
    vertical_img = cv2.flip(img, 1)
    both_img = cv2.flip(img, -1)

    cv2.imshow("original img", img)
    cv2.imshow("horizontal img", horizontal_img)
    cv2.imshow("vertical img", vertical_img)
    cv2.imshow("both flip", both_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def flip_img_save2dir(file):
    img = cv2.imread(file)

    dst_dir = path_var.g_dst_dir

    h_img = img.copy()
    v_img = img.copy()
    b_img = img.copy()

    h_img = cv2.flip(img, 0)
    v_img = cv2.flip(img, 1)
    b_img = cv2.flip(img, -1)

    # file like F:/ad_samples/train_samples/ad_text_artifact/base_type/type_10.jpg
    # get file name "type_10"
    # type_10.jpg
    base_name = os.path.basename(file)
    # type_10
    base_name = os.path.splitext(base_name)[0]

    file_name = dst_dir + base_name + "_h" + ".jpg"
    cv2.imwrite(file_name, h_img)

    file_name = dst_dir + base_name + "_v" + ".jpg"
    cv2.imwrite(file_name, v_img)

    file_name = dst_dir + base_name + '_b' + ".jpg"
    cv2.imwrite(file_name, b_img)


def do_all_flip(base_dir=""):
    # get all files
    files = glob.glob(base_dir + "/*.png")
    # like ['E:/img\\1.jpg', 'E:/img\\10.jpg']

    # start 3 process
    # pool = ProcessPool(3)
    pool = ThreadPool(3)
    rets = pool.map(flip_img_save2dir, files)
    pool.close()
    pool.join()
    print ('all images accomplish flip and save to dir')


def flip_all_in_dir():
    base_dir = ""
    sub_dir_lst = glob.glob(base_dir + "*")
    # ['F:/dir1', 'F:/dir2']

    # print sub_dir_lst
    new_sub_dir = [os.path.join(base_dir, item + '_flip/') for item in os.listdir(base_dir)]
    # ['F:/dir1_flip', 'F:/dir2_flip']

    for dir_item, new_item in zip(sub_dir_lst[10:], new_sub_dir[10:]):
        global g_dst_dir
        if not os.path.exists(new_item):
            os.makedirs(new_item)
        # g_dst_dir = new_item
        # Path.g_dst_dir = new_item
        path_var.g_dst_dir = new_item
        print ('flip %s, flip dir %s' % (dir_item, new_item))
        do_all_flip(base_dir=dir_item)



def augmentation(path, output_path):
    # path = 'F:/ad_samples/train_samples/ad_text'
    # output_path = 'F:/ad_samples/train_samples/ad_text_artifact/augmentation'

    p = Augmentor.Pipeline(path, output_directory=output_path)

    p.zoom(probability=0.1, min_factor=1.1, max_factor=1.3)
    p.flip_left_right(probability=0.1)
    p.rotate(probability=0.2, max_left_rotation=15, max_right_rotation=16)
    p.shear(probability=0.2, max_shear_left=10, max_shear_right=10)
    p.skew(probability=0.1, magnitude=0.6)
    p.skew_tilt(probability=0.2, magnitude=0.6)
    p.random_distortion(probability=0.3, grid_height=4, grid_width=4, magnitude=4)

    # p.random_distortion(probability=0.2, grid_height=4, grid_width=4, magnitude=4)
    # p.rotate90(probability=1)
    # SIZE = 4164 * 4
    SIZE = 5 * 4
    p.sample(SIZE)


if __name__ == '__main__':
    # img_flip()
    # flip_all_in_dir()
    # do_all_flip()
    augmentation("source", "")
    augmentation("negative", "")
    # test single image flip and save
    # file = 'F:/ad_samples/train_samples/ad_text_artifact/base_type/type_10.jpg'
    # flip_img_save2dir(file=file)
    pass
