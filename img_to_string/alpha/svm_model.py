from libsvm.python.svmutil import *
from libsvm.python.svm import *

def train_svm_model():
    y, x = svm_read_problem('1.txt')
    print(y)
    param = svm_parameter('-t 0 -c 4 -b 1')
    model = svm_train(y, x, param)
    svm_save_model("model", model)

def svm_test():
    test_y, test_x = svm_read_problem("2.txt")
    model = svm_load_model("model")
    p_label, p_acc, p_val = svm_predict(test_y, test_x, model)
    print(p_label)

if __name__ == "__main__":
    train_svm_model()
    svm_test()