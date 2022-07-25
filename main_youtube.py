import requests

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

import json

client_id = "b_GHhK7YJ9GfvaGW6kCc"
client_secret = "OGh9kCg2Sg"
url = "https://openapi.naver.com/v1/vision/face" 
img = "example.jpg"

files = {'image': open(img, 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
if(rescode==200):
    pass
else:
    print("Error Code:" + rescode)
    raise Exception

response = json.loads(response.text)
imginfo = response['info']
faces = response['faces']

faceRects = []
faceTexts = []


for face in faces:
    x = face['roi']['x']
    y = face['roi']['y']
    w = face['roi']['width']
    h = face['roi']['height']
    facerect = patches.Rectangle( (x,y) ,w,h, linewidth = 5, edgecolor = 'g', facecolor='none')

    faceRects.append(facerect)

    textset = [x,y,w,h]
    gendertext = "gender" + ":" + face['gender']['value'] + ' ,' + str(int(face['gender']['confidence'] * 100)) + "%"
    textset.append(gendertext)

    emotiontext = "emotion" + ":" + face['emotion']['value'] + ' ,' + str(int(face['emotion']['confidence'] * 100)) + "%"
    textset.append(emotiontext)

    agetext = "age" + ":" + face['age']['value'] + ' ,' + str(int(face['age']['confidence'] * 100)) + "%"
    textset.append(agetext)

    faceTexts.append(textset)

fig, ax = plt.subplots(figsize = (10,10))

ax.imshow(mpimg.imread(img))
for facerect in faceRects :
    ax.add_patch(facerect)

for text in faceTexts:
    x = text[0]
    y = text[1]
    w = text[2]
    h = text[3]
    ax.text(x+10, y+h+10, text[4] + '\n'+text[5]+'\n'+text[6] , fontsize = 15, color = 'red', verticalalignment = 'top')
plt.show()

