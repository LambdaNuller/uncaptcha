from PIL import Image
import numpy as np
import time
import os


def convert(img):
    '''
    二值化图像
    :param img:
    :return:
    '''
    img_grey = img.convert('L')
    threshold = 200
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    out_img = img_grey.point(table, '1')
    return out_img

def flood_fill(img, x, y):
    '''
    降噪
    :param img:
    :param x: 当前x坐标
    :param y: 当前y坐标
    :return:
    '''
    cur_pixel = img.getpixel((x, y))
    width = img.width
    height = img.height

    # 若当前点为白色，则不统计邻域值
    if cur_pixel == 1:
        return 0

    if y == 0:
        if x == 0:
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))
            + img.getpixel((x + 1, y + 1))
            return 4 - sum
        else:
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum

def remove_noise_point(img, start, end):
    '''
    去杂点
    :param img:
    :param start:
    :param end:
    :return:
    '''
    noise_point_list = []
    for w in range(img.width):
        for h in range(img.height):
            around_num = flood_fill(img, w, h)
            if(start < around_num < end) and img.getpixel((w, h)) == 0:
                pos = (w, h)
                noise_point_list.append(pos)

    for pos in noise_point_list:
        img.putpixel((pos[0], pos[1]), 1)
    return img

def print_mat_img(img):
    mat_img = np.asarray(img, np.int8)
    for h in range(img.height):
        for w in range(img.width):
            print(mat_img[h][w], end='')
        print('')

def add_line_by_x(x_list, img):
    mat_img = np.asarray(img, np.int8)
    for x in x_list:
        for h in range(img.height):
            mat_img[h, x] = 0
        image = Image.fromarray(np.uint8(mat_img))
    return image

def add_line_by_y(y_list, img):
    mat_img = np.asarray(img, np.int8)
    for y in y_list:
        for w in range(img.width):
            mat_img[y, w] = 0
        image = Image.fromarray(np.uint8(mat_img))
    return image

def crop_img(img, points, width, height):
    '''
    剪裁图像
    :param img: Image图像
    :param points: 要剪裁的点的组合
    :return:
    '''
    imgs = []
    index = 0
    for point in points[:-1]:
        print(point[0], point[1])
        chirld_img = img.crop((point[0], point[1], point[0] + width, point[1] + height))
        imgs.append(chirld_img)
        chirld_img.save(".//data//cut//%s.jpg" % (str(time.time())+str(index)), "jpeg")
        index += 1

def make_crop_points(x_list, y_list):
    width = x_list[1] - x_list[0]
    height = y_list[1] - y_list[0]
    points = []
    for x in x_list:
        for y in y_list:
            pos = (x, y)
            points.append(pos)
    return points, width, height

if __name__ == "__main__":
    cut_by_x_start = 5
    cut_by_x_end = 58
    x_list = np.linspace(cut_by_x_start, cut_by_x_end, 5, dtype=np.int16).tolist()
    y_list = [1, 17]
    i2 = Image.open("1.jpg")
    # i2 = add_line_by_x(x_list, img)
    # i2 = add_line_by_y([1, 17], i2)
    i2 = convert(i2)
    # i2.save("2.jpg")
    print_mat_img(i2)
    # i3 = remove_noise_point(img_gray, 1, 7)
    # i3.save("3.jpg")

    points, width, height = make_crop_points(x_list, y_list)
    img_paths = os.listdir(".//data//source//")
    # for path in img_paths:
    #     img = Image.open(".//data//source//"+path, 'r')
    #     img_gray = convert(img)
    #     crop_img(img_gray, points[0::2], width, height)

