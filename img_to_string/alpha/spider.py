import requests
import time
# nuller
# 2017.12.22
for _ in range(100):
    img = requests.get("http://jf.bhu.edu.cn/xtgl/login_code.html?time=%s" % time.time()).content
    with open(".//data//%s.jpg" % time.time(), 'wb') as f:
        f.write(img)

