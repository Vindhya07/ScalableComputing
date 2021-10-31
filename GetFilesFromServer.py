import requests
import os

fileList = requests.get("http://cs7ns1.scss.tcd.ie/index.php/?shortname=vnagaraj&download=noresume_speed").text


for i in fileList.split(',\n'):
    f = requests.get("http://cs7ns1.scss.tcd.ie/index.php/?shortname=vnagaraj&download=noresume_speed&myfilename="+i)
    os.chdir("vnagaraj-files2")
    file = open(i, "wb")
    file.write(f.content)
    file.close()
