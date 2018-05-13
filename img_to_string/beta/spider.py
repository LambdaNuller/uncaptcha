import requests

for i in range(400):
    res = requests.get('https://i.mgtv.com/vcode?from=pcclient').content
    with open(".//data//%s.jpg" % i, 'wb') as f:
        f.write(res)
