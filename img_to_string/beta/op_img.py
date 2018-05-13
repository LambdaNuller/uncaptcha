from PIL import Image
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


def convert(img):
    '''
    二值化图像
    :param img:
    :return:
    '''
    img_grey = img.convert('L')
    threshold = 130
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

def vertical_scaning(img):
    xs = img.width
    nums = []
    for x in range(xs):
        num = 0
        for y in range(img.height):
            if img.getpixel((x, y)) == 0:
                num += 1
        nums.append(num)
    return nums

def plot_vertical_scaning(width, x):
    plt.plot(range(width), x, mec='r', mfc='w')
    plt.show()

def print_mat_img(img):
    mat_img = np.asarray(img, np.int8)
    for h in range(img.height):
        for w in range(img.width):
            print(mat_img[h][w], end='')
        print('')

def find_cut_x_line(img, cut_param):
    nums = vertical_scaning(img)
    cut_x_points = []
    for index in range(1, len(nums)-1):
        if nums[index]==cut_param and (nums[index-1]!=cut_param or nums[index+1]!=cut_param):
            cut_x_points.append(index)
    return cut_x_points

def add_line_by_x(x_list, img):
    for x in x_list:
        for h in range(img.height):
            img.putpixel((x, h), 0)
    return img

if __name__ == '__main__':
    i = Image.open(".//data//1.jpg")
    i = convert(i)
    i = remove_noise_point(i, 0, 5)
    #print(vertical_scaning(i))
    #print_mat_img(i)
    #plot_vertical_scaning(i.width, vertical_scaning(i))
    #i = add_line_by_x(find_cut_x_line(i, 0), i)
    i.save("d.jpg")