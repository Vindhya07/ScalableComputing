import requests

url = 'https://cs7ns1.scss.tcd.ie/index.php/?shortname=vnagaraj&download=resume_speed'
myFileNames = requests.get(url).text

print(myFileNames)

for i in myFileNames:
  file_url = 'https://cs7ns1.scss.tcd.ie/index.php/?shortname=vnagaraj&download=resume_speed&myfilename=' + i
  iFIlePath = '/vnagaraj-files2'+i
  myFiles = requests.get(file_url)
  myFile = open(iFilePath, "wb")
  myFile.write(myFiles.content)
  myFile.close()
