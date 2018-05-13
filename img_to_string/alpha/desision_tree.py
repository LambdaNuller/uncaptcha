from sklearn import tree
from alpha import create_feature

def train_and_test(train_xs, train_ys, test_xs):
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_xs, train_ys)
    test_y = clf.predict(test_xs)

    return test_y

if __name__ == "__main__":

    xs, ys = create_feature.create_train_np_array(".//data//cut//")
    test_xs = create_feature.create_test_np_array(".//data//test//")
    result = [chr(result) for result in train_and_test(xs, ys, test_xs)]
    print(result)