# %pylab
from numba import jit
import skimage.io
import skimage.filter
from skimage.util import img_as_float

execfile("C:\Users\myPc\Documents\graphics_2015\plants.py")


SIZE=1000
#plants=zeros((SIZE,SIZE,3))

def restart_background(Size=1000,SkyRate=0.8,frompicture=-1):
    M=zeros((Size,Size,3))+1
    if (frompicture>0):
        '''if (Size==1000):
            M=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/backgrounds/background"+str(frompicture)+".jpg")
            M=img_as_float(M)
            return M'''
        orig=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/backgrounds/background"+str(frompicture)+".jpg")
        orig=img_as_float(orig)
        for i in range(Size):
            for j in range(Size):
                temp=array(orig[int(i*1000/double(Size))][int(j*1000/double(Size))])
                M[i][j]=temp
        return M
    x,y = meshgrid(arange(0,1,1./Size),arange(0,1,1./Size))
    Limitx = SkyRate+0.02*(sin(x*3)+0.3*sin(x*x*10)-x*0.5)
    temp = (y-Limitx)**0.25
    M1 = zeros((Size, Size, 3))
    M1[:,:,0] = 0.65+y*y*0.2
    M1[:,:,1] = 0.6+y*0.2
    M1[:,:,2] = 1-y*y*y*0.2
    M2 = zeros((Size, Size, 3))
    M2[:,:,0] = 0.65-temp*0.3
    M2[:,:,0] =  0.6-temp*0.7 # <--
    M2[:,:,1] = 0.6-temp*0.5
    M2[:,:,1] =  0.8-temp*0.3 # <--
    M2[:,:,2] = 0.6-temp*0.6
    M2[:,:,2] = 0.8-temp*0.99 # <--
    Grass=True;
    fogcolor=[0.9,0.9,0.98]
    fogcolor=[0.6,0.7,0.5]
    RealHorizon=SkyRate-0.1
    if Grass:
        C1=[0.5,0.6,0.2]
        C2=[0.,0.3,0]
        
        DIST=(1-SkyRate+0.2)/(y-SkyRate+0.2)
        Fog=1-1/DIST
        
        M2[:,:,0] = (1-Fog)*(C1[0]+(C2[0]-C1[0])*0.5)+Fog*fogcolor[0]
        M2[:,:,1] = (1-Fog)*(C1[1]+(C2[1]-C1[1])*0.5)+Fog*fogcolor[1]
        M2[:,:,2] = (1-Fog)*(C1[2]+(C2[2]-C1[2])*0.5)+Fog*fogcolor[2] 
    return where((y<Limitx)[...,newaxis], M1, M2)

    '''for j in range(Size):
        x=j/double(Size)
        Limitx=SkyRate+0.02*(sin(x*3)+0.2*sin(x*x*10))
        for i in range(int(Limitx*Size)):
            y=i/double(Size)
            M[i][j]=[0.65+y*y*0.2,0.6+y*0.2,1-y*y*y*0.2]
        for i in range(int(Limitx*Size),Size):
            y=i/double(Size)
            d=abs(y-Limitx)
            temp=sqrt((sqrt(d)))
            M[i][j]=[0.65-temp*0.3, 0.6-temp*0.5, 0.6-temp*0.6]
    return M'''


fogcolor=[0.9,0.9,0.9]
screen_dist=15

def shade(dest,destsize,Minj,Maxj,depth,horizon,foglevel,fogcolor):
    ShadeBasicLevel=0.03
    Center=int((Minj+Maxj)/2.)
    Radius=int((Maxj-Minj)/2.)
    if (Radius<2):
        return
    for x in range(destsize):
        for y in range(destsize):
             if (double(dest[x][y][0])>1):
                         #print dest[x][y]
                         return
    for x in range(-Radius,Radius+1):
        H=horizon-horizon*(screen_dist/(screen_dist+depth+x*screen_dist/double(destsize)))
        if (H<0):
            return
        i=destsize-H
        Fog=1-(1-foglevel)**(depth+x*screen_dist/double(destsize))
        if (Fog<0):
            Fog=0
        C=[fogcolor[0]*Fog, fogcolor[1]*Fog, fogcolor[2]*Fog]
        #if (C[0]<0) or (C[0]>1):
        #    print "C:",C
        for y in range(-Radius,Radius+1):        
            j=Center+y
            d2=double(x*x+y*y)
            R2=double(Radius*Radius)
            if (d2<R2) and (0<j<destsize) and (0<i<destsize):
                for k in range(3):
                    Shade=ShadeBasicLevel*(1-d2/R2)
                    temp=dest[i][j]
                    dest[i][j][k]=C[k]*Shade+dest[i][j][k]*(1-Shade)
                    if (dest[i][j][0]>1):
                         # print temp,dest[i][j],Shade,C
                         return
                           
            
    
@jit
def place(orig,origsize,dest,destsize,place,depth,horizon,foglevel,fogcolor=-1,basicprop=-1,high_in_air=0):
        if (fogcolor==-1):
            fogcolor=[0.9,0.9,0.9]
        if (basicprop>0):
            Prop=(screen_dist/double(depth+screen_dist))*basicprop
        else:
            Prop=(screen_dist/double(depth+screen_dist))*destsize/double(origsize)
	
	H=horizon-horizon*(screen_dist/double(depth+screen_dist))
	#H=high from bottom of the screen to bottom of the tree
	Fog=1-(1-foglevel)**depth
	Minj=int(place+origsize*Prop/2)
	Maxj=int(place-origsize*Prop/2)
	for i in range(int(destsize-H-origsize*Prop),int(destsize-H)):
	    for j in range(int(place-origsize*Prop/2),int(place+origsize*Prop/2)):
		    temp=((destsize-H)-i)/Prop
		    x=origsize-temp
		    y=int((j-double(place))/Prop+origsize/2.)
		    if (0<x<origsize) and (0<y<origsize):
                        if (orig[x][y][0]!=1.) or (orig[x][y][1]!=1.) or (orig[x][y][2]!=1.):
                            if (j<Minj):
                                Minj=j
                            if (j>Maxj):
                                Maxj=j
                            i2=int(i-high_in_air*screen_dist/double(depth+screen_dist))
                            if (0<i2<destsize) and (0<j<destsize):
                                
                                if (depth>=0):
				    for k in range(3):
                                        dest[i2][j][k]=Fog*fogcolor[k]+(1-Fog)*orig[x][y][k]
                                    #if (dest[i2][j][0]>dest[i2][j][1]):
                                    #    print dest[i2][j], i2, j
				else:
                                    for k in range(3):
					    dest[i2][j][k]=orig[x][y][k]*double(screen_dist+depth)/screen_dist
				for k in range(3):
                                    if (dest[i2][j][k]>1)or(dest[i2][j][k]<0):
                                        print dest[i2][j]
				
	if (Minj<Maxj):
            shade(dest,destsize,Minj,Maxj,depth,horizon,foglevel,fogcolor)
            
            
                                    
def forest_possible_building(blur=0.06,foglevel=0.02): #slow, not important.
    plants=restart_background(SIZE, 0.93,3)
    fogcolor=[0.9,0.9,0.9]
    OS=SIZE #origsize
    anemone_freq=3
    sarach_freq=7
    for x in range(SIZE):
                for y in range(SIZE):
                     if (double(plants[x][y][0])>1):
                         print plants[x][y]
                         break
    TreeNum=100
    for ii in range(TreeNum+3): #520
        high_in_air=0
        prop=1
        if (ii<TreeNum):
            if (ii%10 in [1,2,3,4,5,6]):
                OS=200
                TRY=zeros((OS,OS,3))+1
                #print shape(TRY)
                param=0.4*(rand()+rand()-1)
                param2=0.4*rand()+0.6
                param3=0.3*rand()+0.1
                make_sarach(TRY,OS,OS,75,50,4,0.2*rand(),8,[param2,param,-param2],[0.3,0.95,0.3],[0,param3,0],[0.0,param3+0.1,0.0],1)
            if (ii%10 in [7,8,9]):
                OS=105-randint(10)
                prop=0.2
                TRY=anemone()
            if (ii%10 in [0]):
                OS=500
                high_in_air=randint(200)+200 
                TRY=Buterfly2(OS) 
            plants = skimage.filter.gaussian_filter(plants, blur, multichannel=True)
        else:
            OS=150
            TRY=zeros((OS,OS,3))+1
            param=0.4*(rand()+rand()-1)
            param2=0.4*rand()+0.6
            param3=0.3*rand()+0.1
            make_sarach(TRY,150,150,20,20,2,0.2*rand(),8,[param2,param,-param2],[0.3,0.95,0.3],[0,param3,0],[0.0,param3+0.1,0.0],1)
        place(TRY,OS,plants,SIZE,randint(SIZE),40-40.*ii/TreeNum,0.1*SIZE,foglevel, fogcolor, prop, high_in_air)
        print ii,
        
    return(plants)


def picture_from_flowers(picnum=6,blur=0.06,foglevel=0.02): #slow, not important.
    Flowers=[]
    Colors=[]
    FLOWER_NUM=7
    for i in range(FLOWER_NUM):
        temp=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/flowers/"+str(i)+".png")
        Flowers+=[img_as_float(temp)]
        temp==skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/flowers/C"+str(i)+".png")
        Colors+=[img_as_float(temp)[0][0]]
        #print Flowers[0][0], Colors[0]
    prop=1
    SIZE=1000
    plants=restart_background(SIZE, 0.5)
   
    picfinalsize=900
    Pic=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/pics/"+str(picnum)+".png")
    Pic=img_as_float(Pic)
    origI=shape(Pic)[0]
    origJ=shape(Pic)[1]
    #print origI, origJ
    OS=20
    fogcolor=[0.9,0.9,0.9]
    print origI, origJ
    for i in range(origI):
        print i
        for j in range(origJ):
            min_c_diff=1000000
            argmin=-1
            for k in range(FLOWER_NUM):
                c_diff=(Colors[k][0]-Pic[i][j][0])**2+(Colors[k][1]-Pic[i][j][1])**2+(Colors[k][2]-Pic[i][j][2])**2
                if (c_diff<min_c_diff):
                    min_c_diff=c_diff
                    argmin=k
            #print c_diff, argmin
            d=j-origJ/2.
            dep=(1.-double(i)/origI)*30
            Wide=SIZE/2.+(j-origJ/2.)*(picfinalsize/origJ)*(screen_dist/(dep+screen_dist))
            #plants[Wide][dep]=[1,0,0]
            #if (rand()<0.01):
            #    print i, j
            # print k
            place(Flowers[argmin],OS,plants,SIZE, Wide, dep, 0.5*SIZE, 0.02, fogcolor,1, 0)
                
    return plants












