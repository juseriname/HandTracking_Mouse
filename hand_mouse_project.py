#Mediapipe를 이용한 손 인식
#사전 준비(pip install)
#cmd 창에서 cd (파이썬 설치 경로) 로 디렉토리 이동후  
#pip install mediapipe opencv-python 실행해서 mediapipe 설치 (이미지 인식)
#pip install pyautogui 해서 pyautogui 설치 (매크로)

#실행전 readme.txt 읽어보면 좋음!!

import cv2
import mediapipe as mp
import math
import pyautogui as pg
import time
import os

cap = cv2.VideoCapture(0)
pg.FAILSAFE = False

mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
try:
    def dist(x1,y1,x2,y2):
        return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

    compareIndex = [[18,20],[14,16],[10,12],[6,8]]
    fopen = [True,True,True,True] #기본 상태 True = 펴짐 False = 접힘 ,새끼 -> 검지 순
    gpath = os.path.dirname(os.path.realpath(__file__))+'\macro_list.txt'
    with open(gpath,'r' ,encoding='UTF-8') as g:
        gesture = g.read().split('\n')
        for i in range(len(gesture)):
            gesture[i]=gesture[i].split(',') # 파일 입력 받은후 리스트로 변환
            for j in range(len(gesture[i])):
                if gesture[i][j] == 'False': # 문자 False 를 bool False 로 변환
                    gesture[i][j] = False
                elif gesture[i][j] == 'True': # 문자 True 를 bool True 로 변환
                    gesture[i][j] = True
        umx,umy=pg.size() # 사용자의 화면 크기 측정
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
                        fopen[i] = dist(handLms.landmark[0].x,handLms.landmark[0].y,handLms.landmark[compareIndex[i][0]].x,handLms.landmark[compareIndex[i][0]].y) < dist(handLms.landmark[0].x,handLms.landmark[0].y,handLms.landmark[compareIndex[i][1]].x,handLms.landmark[compareIndex[i][1]].y)
                    #print(fopen)
                    text_x = (handLms.landmark[0].x * w)
                    text_y = (handLms.landmark[0].y * h)
                    for i in range(0,len(gesture)):
                        flag = True
                        for j in range(0,4):
                            if gesture[i][j] != fopen[j]:
                                flag = False
                        if flag == True:
                            cv2.putText(img,gesture[i][4],(round(text_x) - 50,round(text_y) - 250),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)
                            if gesture[i][4] == "'Click!'":
                                pg.click()
                                time.sleep(0.3)
                            #if gesture[i][4] == "'Rlick!'":
                            #    pg.rightClick()
                            #    time.sleep(0.3)
                            #if gesture[i][4] == "'Down!'":
                            #    pg.scroll(-200)
                            #    time.sleep(0.1)
                            #if gesture[i][4] == "'Up!'":
                            #    pg.scroll(200)
                            #    time.sleep(0.1)
                    mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS) #현재 카메라에 인식된 손 모양 보여주기(없어도 됨)
                    #이 밑은 마우스 코드
                    hx1,hx2,hx3,hx4,hx5 = handLms.landmark[0].x,handLms.landmark[17].x,handLms.landmark[13].x,handLms.landmark[9].x,handLms.landmark[5].x
                    hy1,hy2,hy3,hy4,hy5 = handLms.landmark[0].y,handLms.landmark[17].y,handLms.landmark[13].y,handLms.landmark[9].y,handLms.landmark[5].y
                    pointx = ((hx1+hx2+hx3+hx4+hx5)/5)*(umx+300) # 현재 화면 크기보다 넉넉하게 잡아주기
                    pointy = ((hy1+hy2+hy3+hy4+hy5)/5)*(umy+300)

                    #보정단위 7픽셀
                    if abs(pointax[-1]-pointx) <= 4:
                        pointx = pointax[-1]
                    if abs(pointay[-1]-pointy) <= 4:
                        pointy = pointay[-1]
                    pointax.append(pointx)
                    pointay.append(pointy)
                    
                    pg.moveTo(pointx,pointy,0.05)
                    #여기까지

            cv2.imshow("HandTracking Mouse",img) # 현재 카메라에 찍히는 모습 보여주기(없어도 됨)
            cv2.waitKey(1)
            #time.sleep(0.15)
except Exception as ex:
    print('error!! : ',ex)

# 참고 자료:
# https://developeralice.tistory.com/10
# https://techtutorialsx.com/2019/04/21/python-opencv-flipping-an-image/
# https://wikidocs.net/85581
