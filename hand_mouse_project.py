#Mediapipe를 이용한 손 인식
#사전 준비(pip install)
#cmd 창에서 cd (파이썬 설치 경로) 로 디렉토리 이동후  
#pip install mediapipe opencv-python 실행해서 mediapipe 설치 (이미지 인식)
#pip install pyautogui 해서 pyautogui 설치 (매크로)

from tkinter.tix import Tree
import cv2
import mediapipe as mp
import math
import pyautogui as pg
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def dist(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

compareIndex = [[18,20],[14,16],[10,12],[6,8]]
open = [True,True,True,True] #기본 상태 True = 펴짐 False = 접힘 ,새끼 -> 검지 순
gesture = [[False,False,False,False,'Click!'],[False,False,True,True,'Yeah!']]
pointax = [0]
pointay = [0]

while 1:
    success,limg = cap.read()
    img = cv2.flip(limg, 1)
    h,w,c = img.shape
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)
    if results.multi_hand_landmarks:
        if len(pointax) >= 40 and len(pointay) >= 40:
            del pointax[0:]
            del pointay[0:]
            pointax.append(0)
            pointay.append(0)
        for handLms in results.multi_hand_landmarks:
            for i in range(0,4):
                open[i] = dist(handLms.landmark[0].x,handLms.landmark[0].y,handLms.landmark[compareIndex[i][0]].x,handLms.landmark[compareIndex[i][0]].y) < dist(handLms.landmark[0].x,handLms.landmark[0].y,handLms.landmark[compareIndex[i][1]].x,handLms.landmark[compareIndex[i][1]].y)
            #print(open)
            text_x = (handLms.landmark[0].x * w)
            text_y = (handLms.landmark[0].y * h)
            for i in range(0,len(gesture)):
                flag = True
                for j in range(0,4):
                    if gesture[i][j] != open[j]:
                        flag = False
                if(flag == True):
                    cv2.putText(img,gesture[i][4],(round(text_x) - 50,round(text_y) - 250),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)
                    if gesture[i][4] == 'Click!':
                        pg.click()
                        time.sleep(0.5)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            #이 밑은 마우스 코드
            hx1,hx2,hx3,hx4,hx5 = handLms.landmark[0].x,handLms.landmark[17].x,handLms.landmark[13].x,handLms.landmark[9].x,handLms.landmark[5].x
            hy1,hy2,hy3,hy4,hy5 = handLms.landmark[0].y,handLms.landmark[17].y,handLms.landmark[13].y,handLms.landmark[9].y,handLms.landmark[5].y
            pointx = ((hx1+hx2+hx3+hx4+hx5)/5)*2000
            pointy = ((hy1+hy2+hy3+hy4+hy5)/5)*1100
            #보정단위 10픽셀
            if abs(pointax[-1]-pointx) <= 10:
                pointx = pointax[-1]
                print('xBBIB')
            if abs(pointay[-1]-pointy) <= 10:
                pointy = pointay[-1]
                print('yBBIB')
            print(f'배열x={pointax[-1]},배열y={pointay[-1]}')
            print(f'현재x={pointx},현재y={pointy}')
            print(f'x차이={abs(pointax[-1]-pointx)},y차이={abs(pointay[-1]-pointy)}')
            pointax.append(pointx)
            pointay.append(pointy)
            
            #print(pointx,pointy)
            pg.moveTo(pointx,pointy,0.01)
            #여기까지

    cv2.imshow("HandTracking Mouse",img)
    cv2.waitKey(1)
    time.sleep(0.1)

# 참고 자료:
# https://developeralice.tistory.com/10
# https://techtutorialsx.com/2019/04/21/python-opencv-flipping-an-image/