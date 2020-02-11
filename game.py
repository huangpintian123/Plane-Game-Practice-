import pygame
import random
import copy
import time
from pygame.locals import *

#bullet
class HeroBiu():
    def __init__(self,huabu,feijix,feijiy):
      self.huabu= huabu
      self.x=feijix + 50-11 #bulllet 坐标
      self.y=feijiy-22 #子弹坐标

      self.pic=pygame.image.load('/MyDocuments/img/bullet.png')  #导入子弹图片

    def draw(self):
        self.huabu.blit(self.pic,(self.x,self.y))
        self.move()
    def move(self):
        self.y-=8

# enemy bullet
class DjBiu():
    def __init__(self,huabu,dijix,dijiy):
        self.huabu=huabu
        self.x=dijix+69//2-4
        self.y=dijiy+89  #子弹坐标

        self.pic=pygame.image.load('/MyDocuments/img/bullet-1.gif')

    def draw(self):
        self.huabu.blit(self.pic,(self.x,self.y))
        self.move()
    def move(self):
        self.y+=2



huabu=pygame.display.set_mode((480,800),0,32) #0,32为色深
pygame.display.set_caption('my game')

iconPic=pygame.image.load('/MyDocuments/img/icon72x72.png')
pygame.display.set_icon(iconPic) #将图片放进程序

bg=pygame.image.load('/MyDocuments/img/background.png')

#主角飞机
feiji=pygame.image.load('/MyDocuments/img/hero1.png')
feijix=480//2-100/2  #feiji 横坐标
feijiy=800-124       #飞机纵坐标



#主角飞机效果

feiji2=pygame.image.load('/MyDocuments/img/hero2.png')
fjqh=1    #初始化飞机切换变量

#主角飞机爆炸

fjboomlist = ['/MyDocuments/img/hero_blowup_n1.png'  ,'/MyDocuments/img/hero_blowup_n2.png' ,
            '/MyDocuments/img/hero_blowup_n3.png' , '/MyDocuments/img/hero_blowup_n4.png']

boomIndex=0
fjboom= False

#敌人飞机
diji=pygame.image.load('/MyDocuments/img/enemy1.png')
dijix=480//2-69//2
dijiy=0


#敌机爆炸

djboomlist = ['/MyDocuments/img/enemy1_down1.png' ,  '/MyDocuments/img/enemy1_down2.png'  ,
            '/MyDocuments/img/enemy1_down3.png' ,  '/MyDocuments/img/enemy1_down4.png']

djboomIndex=0
djboom=False

re=pygame.image.load('/MyDocuments/img/restart_nor.png')

tuichu=pygame.image.load('/MyDocuments/img/quit_sel.png')

pygame.key.set_repeat(50,50)  #一直按住50ms后再次反应

direct='右'  #敌机移动标志

HeroBiulist=[]
DjBiulist=[]

while True:
    huabu.blit(bg,(0,0))
    if fjboom==False:
        if fjqh==1:
            huabu.blit(feiji,(feijix,feijiy))#加载飞机
            fjqh=2
        else:
            huabu.blit(feiji2,(feijix,feijiy))#同上
            fjqh=1
    else:
        time.sleep(0.5)
        if boomIndex==len(fjboomlist): #延时0.5秒展示爆炸，如果爆炸展示完啦， 就game over
            exit(0)
        pic= pygame.image.load(fjboomlist[boomIndex])
        huabu.blit(pic,(feijix,feijiy))
        huabu.blit(re,(240-55,380-11))
        huabu.blit(tuichu,(240-55,420-11))
        boomIndex+=1

    if djboom == False:  #if 没爆炸，继续加载敌机
        huabu.blit(diji,(dijix,dijiy))
    else:
        time.sleep(0.5)#如果爆炸了，加载爆炸图片
        if djboomIndex==len(djboomlist):
            exit(0)

        pic = pygame.image.load(djboomlist[djboomIndex])
        huabu.blit(pic,(dijix,dijiy))
        huabu.blit(re,(240-55,380-11))
        huabu.blit(tuichu,(240-55,420-11))
        djboomIndex+=1

    #添加事件，（鼠标键盘）

    for event in pygame.event.get():
        if event.type == QUIT:
            exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                feijix = feijix-5 if feijix>0 else 0
            elif event.key == K_RIGHT:
                feijix = feijix+5 if feijix<380  else 380
            elif event.key == K_UP:
                feijiy = feijiy-5 if feijiy>0   else 0
            elif event.key == K_DOWN:
                feijiy = feijiy+5 if feijiy<676  else 676

            elif event.key == K_SPACE:
                onezd = HeroBiu(huabu,feijix,feijiy)

                HeroBiulist.append(onezd)  #建立一个子弹就加入到列表

            elif event.key == K_a:
                onezd = DjBiu(huabu,dijix,dijiy)

                DjBiulist.append(onezd)


    #射子弹
    zdlist=copy.copy(HeroBiulist)  #复制一份，免得下标会乱
    djRect=Rect(dijix,dijiy,69,89)
    for zd in zdlist:
        zd.draw()
        zdRect=Rect(zd.x,zd.y,22,22)
        if zdRect.colliderect(djRect):
            HeroBiulist.remove(zd)
            djboom=True
            djboomIndex=0

        if zd.y<0:              #if 子弹射出窗口，就要在列表里删除这个子弹
            HeroBiulist.remove(zd)


    #敌人射的子弹
    zddjlist= copy.copy(DjBiulist)
    jsRect=Rect(feijix+36,feijiy,28,40)#机头大小
    jtRect=Rect(feijix,feijiy+40,100,84)#机身大小

    for zd in zddjlist:
        zd.draw()
        zdRect=Rect(zd.x,zd.y,9,21)#子弹大小

        if zdRect.colliderect(jtRect) or zdRect.colliderect(jsRect):
            DjBiulist.remove(zd)
            fjboom = True
            boomIndex = 0
        if zd.y>800:
            DjBiulist.remove(zd)


    #敌机移动
    if direct == '右':
        dijix+=2
        if dijix>480-69:
            dijix = 480-69
            direct = '左'    #if 敌机移动到最右边，就向左移动


    if direct == '左':
        dijix-=2
        if dijix<0:
            dijix=0
            direct = '右'



    #敌机随机发子弹
    x=random.randint(1,100)
    if x==3 or x==78:
        onezd = DjBiu(huabu,dijix,dijiy)
        DjBiulist.append(onezd)

    pygame.display.update()















