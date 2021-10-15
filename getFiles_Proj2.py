import requests

url = 'https://cs7ns1.scss.tcd.ie/index.php/?shortname=vnagaraj&download=resume_speed')
myFileNames = requests.get(url).text

print(myFileNames)
