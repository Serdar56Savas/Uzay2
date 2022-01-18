import pygame
import random
import math
from pygame import mixer

pygame.init()

#pencere yaratır
screen=pygame.display.set_mode((800,600))

background=pygame.image.load("uzay.jpg")

#arkaplan ses efekti
mixer.music.load("background.wav")
mixer.music.play(-1)

running = True

#Başlık ve İcon
pygame.display.set_caption("Space Game")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load("aracc.png")
playerX=370
playerY=500
playerX_change=0

#düşman
dusmanImg=[]                  #düşmanı dizi faktörüne çevirdik ki düşman sayısını arttırmak için
dusmanX=[]
dusmanY=[]
dusmanX_change=[]
dusmanY_change=[]
num_of_dusman=6

for i in range(num_of_dusman):
    dusmanImg.append(pygame.image.load("uzaylı.png"))
    dusmanX.append(random.randint(0,730))
    dusmanY.append(random.randint(50,150))
    dusmanX_change.append(0.3)
    dusmanY_change.append(40)


#Mermi
#hazır durumunda iken mermi görünmez
#ateşleme de ise mermi hareket halinde
mermiImg=pygame.image.load("mermi.png")
mermiX=0
mermiY=480
mermiX_change=0
mermiY_change=1
mermi_state="ready"     #mermi hazır durumda

#skor
score_deger=0
font=pygame.font.Font("freesansbold.ttf",32)

textX=10
textY=10

#Oyunun bitimi için text
bitis_font=pygame.font.Font("freesansbold.ttf",64)

def skor_goster(x,y):
    score=font.render("Score : "+str(score_deger),True,(0,255,255))
    screen.blit(score,(x,y))

def oyun_bitim_text():
    bitis_text=bitis_font.render("OYUN BİTTİ",True,(0,255,255))
    screen.blit(bitis_text,(200,250))


def player(x,y):
    screen.blit(playerImg,(x,y))

def dusman(x,y,i):    #düşman için 3 parametre kullandık
    screen.blit(dusmanImg[i],(x,y))

def mermi_atesleme(x,y):     #mermi ateşlenince fire durumuna geçiyor
    global mermi_state
    mermi_state="fire"
    screen.blit(mermiImg,(x+16,y+10))

def carpisma(dusmanX,dusmanY,mermiX,mermiY):
    mesafe=math.sqrt(math.pow(dusmanX-mermiX,2) + math.pow(dusmanY-mermiY,2))
    if mesafe<27:
        return True
    else:
        return False
while running:

    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        # klavye ile hareket ettirme
        if event.type == pygame.KEYDOWN:
            #print("bir tuşa bastınız")

            if event.key== pygame.K_LEFT:
                #print("sol tuşa bastınız")
                playerX_change=-0.3

            if event.key== pygame.K_RIGHT:
                #print("sağ tuşa bastınız")
                playerX_change=0.3

            #boşluk tuşuna basınca mermi ateşleme
            if event.key==pygame.K_SPACE:
                if mermi_state=="ready":  #eğer merminin durumu tekrar ready olunca ateşlemesini sağlandı
                    mermiX=playerX
                    mermi_atesleme(mermiX,mermiY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT:
                #print("Hareket Durduruldu")
                playerX_change=0

    playerX +=playerX_change

    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    dusmanX+=dusmanX_change
    for i in range(num_of_dusman):  #burda hangi uzaylı vurulmuş ve vurulduysa yenisi oluşması için içiçe yazdık
        #oyun bitiş
        if dusmanY[i]>450:
            for j in range(num_of_dusman):
                dusmanY[j]=2000
            oyun_bitim_text()
            break

        dusmanX[i]+=dusmanX_change[i]
        if dusmanX[i]<=0:
            dusmanX_change[i]=0.3
            dusmanY[i]+=dusmanY_change[i]
        elif dusmanX[i]>736:
            dusmanX_change[i]=-0.3
            dusmanY[i]+=dusmanY_change[i]

        carpma = carpisma(dusmanX[i], dusmanY[i], mermiX, mermiY)
        if carpma:
            patlama_sesi=mixer.Sound("Explode sound Effects (convert-video-online.com)-[AudioTrimmer.com].wav")
            patlama_sesi.play()
            mermiY = 480
            mermi_state = "ready"
            score_deger+=1
            dusmanX[i] = random.randint(0, 730)
            dusmanY[i] = random.randint(50, 150)
        dusman(dusmanX[i], dusmanY[i],i)



    #merminin hareketi

    if mermiY <=0:  #ilk mermi ekrandan çıkınca diğer mermi ready durumuna geçmiş oldu
        mermiY=480
        mermi_state="ready"


    if mermi_state=="fire":
        mermi_atesleme(playerX,mermiY)
        mermiY-=mermiY_change




    player(playerX, playerY)
    skor_goster(textX,textY)
    pygame.display.update()