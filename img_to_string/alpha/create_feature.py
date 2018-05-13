import os
from img_to_string.alpha.op_img import *
from PIL import Image

def get_feature(img):
    features = []
    for h in range(2, img.height):
        temp_num = 0
        for w in range(img.width):
            if img.getpixel((w, h)) == 0:
                temp_num += 1

        features.append(temp_num)

    for w in range(2, img.width):
        temp_num = 0
        for h in range(img.height):
            if img.getpixel((w, h)) == 0:
                temp_num += 1

        features.append(temp_num)
    return features[:-1]

def create_train_libsvm_feature_file(data_file_paths, feature_file):
    '''
    创建libsvm格式文件
    :param data_file_paths: .//data//train//
    :param feature_file:
    :return:
    '''
    labels = os.listdir(data_file_paths)
    for label in labels:
        img_paths = [data_file_paths + label + "//" + path for path in os.listdir(data_file_paths + label + "//")]
        for path in img_paths:
            img = Image.open(path)
            img = convert(img)
            feature_values = get_feature(img)
            feature_string = ''
            for index in range(len(feature_values)):
                feature_string += str(index + 1) + ":" + str(feature_values[index]) + " "
            with open(feature_file, 'a+') as train_file:
                train_file.write(str(ord(label)) + " " + feature_string + '\n')

def create_test_libsvm_feature_file(data_file_paths, feature_file):
    '''
    创建libsvm格式文件
    :param data_file_paths: .//data//test//
    :param feature_file:
    :return:
    '''


    img_paths = [data_file_paths + path for path in os.listdir(data_file_paths)]
    for path in img_paths:
        img = Image.open(path)
        img = convert(img)
        feature_values = get_feature(img)
        feature_string = ''
        for index in range(len(feature_values)):
            feature_string += str(index + 1) + ":" + str(feature_values[index]) + " "
        with open(feature_file, 'a+') as train_file:
            train_file.write("0 " + feature_string + '\n')

def create_train_np_array(data_file_paths):
    xs = []
    ys = []
    labels = os.listdir(data_file_paths)
    for label in labels:
        img_paths = [data_file_paths + label + "//" + path for path in os.listdir(data_file_paths + label + "//")]
        for path in img_paths:
            img = Image.open(path)
            img = convert(img)
            feature_values = get_feature(img)
            xs.append(feature_values)
            ys.append(ord(label))
    xs = np.asarray(xs)
    ys = np.asarray(ys).reshape((-1,1))
    return xs, ys

def create_test_np_array(data_file_paths):
    xs = []
    img_paths = [data_file_paths + path for path in os.listdir(data_file_paths)]
    for path in img_paths:
        img = Image.open(path)
        img = convert(img)
        feature_values = get_feature(img)
        xs.append(feature_values)
    return xs

if __name__ == '__main__':
    create_train_libsvm_feature_file(".//data//cut//", "1.txt")
    create_test_libsvm_feature_file(".//data//test//", "2.txt")
    #xs, ys = create_train_np_array(".//data//cut//")
