from sliding_puzzle.alpha.get_img import *

'''
nuller
2018.1.14
破解滑动验证码alpha
生成滑动轨迹并滑动
'''

def create_slide_track(distances):
    '''
    :param distances: start point: distances[0]; end point:distances[1]
    :return:
    '''
    distance = distances[0] - distances[1]
    current = distances[0]
    track = []
    flag = distance*(2/3)
    t = 0.3
    v = 0
    while current < distances[1]:
        if current < flag:
            a = 2
        else:
            a = -3

        v0 = v
        v = v0 + a*t
        move = v0*t + (1/2)*a*(t**2)
        current += move
        track.append(round(move))
    return track

def do_it(driver, track, slider):
    '''

    :param driver: driver
    :param track:tracks array
    :param slider:slider element
    :return:
    '''
    action = ActionChains(driver)
    action.click_and_hold(slider).perform()
    for t in track:
        action.move_by_offset(xoffset=t, yoffset=0).perform()
    time.sleep(1)
    action.release().perform()

if __name__ == "__main__":
    # distances = get_distance_by_color()
    # track = create_slide_track(distances[:2])
    driver = webdriver.Firefox()

    driver.get("https://www.xiachufang.com/auth/apply/")
    slider = driver.find_element_by_class_name("gt_slider_knob")
    #do_it(driver, track, slider)
