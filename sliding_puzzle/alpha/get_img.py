from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
import numpy as np
'''
nuller
2018.1.6
破解滑动验证码alpha
'''
def spider():
    '''
    爬取数据截图到文件夹screen_shot中
    '''
    driver = webdriver.PhantomJS(executable_path='D:\Anaconda3\phantomjs.exe')
    driver.get("https://www.xiachufang.com/auth/apply/")
    show = driver.find_element_by_class_name("gt_ajax_tip")
    puzzle = driver.find_element_by_class_name("gt_slider_knob")
    action = ActionChains(driver)
    action.move_to_element(show).click().perform()
    time.sleep(1)
    driver.save_screenshot(".//screen_shot//a.png")
    action.move_to_element(puzzle).click_and_hold().perform()
    time.sleep(1)
    driver.save_screenshot(".//screen_shot//b.png")
    driver.refresh()
    time.sleep(1)

def crop_img(filename,top,left,right,bottom,tofilename):
    '''
    根据函数spider保存的截图来剪裁滑动验证码图片
    :param filename: spider保存的截图文件名
    :param top: 所要剪裁的上部坐标
    :param left: 所要剪裁的左部坐标
    :param right: 所要剪裁的右部坐标
    :param bottom: 所要剪裁的下部坐标
    :param tofilename: 剪裁图片要保存的文件名
    '''
    img1 = Image.open(filename)
    img1 = img1.crop((top, left, right, bottom))
    img1.save(tofilename)

def convert(img, threshold):
    '''
    二值化图像
    :param img:
    :return:
    '''
    img_grey = img.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    out_img = img_grey.point(table, '1')
    return out_img


def find_different_area(img1, img2, threshold):
    '''
    找到两个图不一样的地方
    :param img1: 图片1
    :param img2: 图片2
    :param threshold: 像素值所差的阈值
    :return: 不一样的像素坐标列表
    '''
    different_area = []
    for y in range(img1.height):
        for x in range(img1.width):
            pixel1 = img1.getpixel((x, y))
            pixel2 = img2.getpixel((x, y))
            for i in range(3):
                if abs(pixel1[i] - pixel2[i]) > threshold:
                    different_area.append((x, y))
    return different_area

def mark_find_different_area(img1,img2, different_threshold):
    '''
    用颜色标出find_different_area的返回值
    :param img1: 图片1
    :param img2: 图片2
    :param different_threshold:不一样的阈值
    :return:
    '''
    box = find_different_area(img1, img2, different_threshold)
    for w in range(img2.width):
        for h in range(img2.height):
            img2.putpixel((w, h), (255, 255, 255))
    for p in box:
            img2.putpixel((p[0], p[1]), (0, 0, 0))
    return img2

def get_distance_by_color(img, num_threshold):
    width = img.width
    height = img.height
    nums = []
    bounds = []
    for w in range(width):
        num = 0
        for h in range(height):
            if img.getpixel((w, h))[0] ==0 and img.getpixel((w, h))[1]==0 and img.getpixel((w, h))[2]==0:
                num += 1
        nums.append(num)
    for w in range(width):
        if nums[w]>num_threshold and nums[w+1]<num_threshold:
            bounds.append(w)

    return bounds

def minus_imgs(img1, img2):
    width = img1.width
    height = img2.height
    minus_pixels = []
    for w in range(width):
        for h in range(height):
            minus_pixels.append((abs(img1.getpixel((w, h))[0] - img2.getpixel((w, h))[0]), abs(img1.getpixel((w, h))[1] - img2.getpixel((w, h))[1]), abs(img1.getpixel((w, h))[2] - img2.getpixel((w, h))[2])))
    mat_img = np.asarray(minus_pixels).reshape((width, height, 3))
    image = Image.fromarray(np.uint8(mat_img))
    return image


def add_line_by_x(x_list, img):
    height = img.height
    for x in x_list:
        for h in range(height):
            img.putpixel((x, h), (0, 0, 0))
    img.save("6.jpg")

#if __name__ == "__main__":
    #crop_img(".//screen_shot//a.png",346, 300, 604, 418)

    #debug
    # different_threshold = 50
    # img1 = Image.open("2.jpg")
    #
    # img2 = Image.open("3.jpg")
    # img3 = Image.open("5.jpg")
    # box = find_different_area(img1, img2, different_threshold)
    # img6 = mark_find_different_area(img1, img2, different_threshold)
    # distance_x_points = get_distance_by_color(img6, 7)
    # add_line_by_x(distance_x_points, img3)
    # img4 = minus_imgs(img1, img2)
    # img4.save("7.jpg")
    # img5 = convert(img6, 100)
    # img5.save("9.jpg")
    # distance = distance_x_points[1] - distance_x_points[0]
    # print(distance)






