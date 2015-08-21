
from numba import jit

def Color(C):
    x=C+rand()*0.03
    if x<0.5:
        return ([0.2+0.1*x,0.1+0.4*x,0.])
    else: 
        return([0.3-0.25*x,0.9*x,0.1])

@jit
def anaf(matrix,size,starti,startj,L,W,angel,C1,C2):
    for a in range(int(2*L)):
        for b in range(-int(W),int(W)):
            i=starti-0.5*a*cos(angel)-0.5*b*sin(angel)
            j=startj-0.5*a*sin(angel)+0.5*b*cos(angel)
	    Ctemp=[0,0,0]
            for k in range(3):
            	Ctemp[k]=C1[k]+(C2[k]-C1[k])*a/(2*L)
            if (0<i<size) and (0<j<size):
                matrix[i][j]=[Ctemp[0],Ctemp[1], Ctemp[2]]
                if (C2==-1):
                    matrix[i][j]=[0.7+0.3*rand(), 0.6*rand(), 0.7+0.3*rand()]

def make_tree(matrix,size,starti,startj,startL,startW,startangel,level,childnum,prop,maxangel,C1,C2,LF):
    if (level<0):
        return
    if (level==0):
        if rand()<0.0: # chance for flower 
            LF(matrix,size,starti,startj,startangel,1)
        else:
            LF(matrix,size,starti,startj,startangel,0)
        return
    tprop=prop
    L=(startL*tprop)
    W=(startW*tprop)
    if (W<1): 
        W=1
    startL=startL*(0.3+0.7*rand())
    endi=starti-startL*cos(startangel)
    endj=startj-startL*sin(startangel)
    endC=C1+(C2-C1)/level
    anaf(matrix,size,starti,startj,startL,startW,startangel,C1,endC)
    for c in range(childnum):
        angel=startangel+(2*rand()-1)*maxangel
        # tprop=prop*(0.7+0.3*sqrt(rand()))
        make_tree(matrix,size,endi,endj,L,W,angel,level-1,childnum,prop,maxangel,endC,C2,LF)
        

def make_sarach(matrix,size,starti,startj,startL,startW,startangel,level,angels,props,C1,C2,leafsize):
    if (level<0):
        return
    if (level==0):
        if rand()<0.0: # chance for flower 
            anaf(matrix,size,starti,startj,leafsize,leafsize,startangel,C1,-1)
        else:
            anaf(matrix,size,starti,startj,leafsize,leafsize,startangel,C1,C2)
        return
    #startL=startL*(0.9+0.2*rand())
    endi=starti-startL*cos(startangel)
    endj=startj-startL*sin(startangel)
    endC=[0,0,0]
    for k in range(3):
	endC[k]=C1[k]+(C2[k]-C1[k])/level
    anaf(matrix,size,starti,startj,startL,startW,startangel,C1,endC)
    for c in range(3):
        L=startL*props[c]
        W=startW*props[1]
        if (W<1): 
            W=1
        angel=startangel+angels[c]+(rand()*0.3-0.15)
        # tprop=prop*(0.7+0.3*sqrt(rand()))
        make_sarach(matrix,size,endi,endj,L,W,angel,level-1-(1-c%2),[angels[0],angels[1]/(2-c%2),angels[2]],props,endC,C2,leafsize)
        

def new_sarach():
    plants=restart_background(400)
    make_sarach(plants,400,360,200,30,2,0.,15,[1.,0.0,-1.],[0.3,0.95,0.3],[0,0.2,0],[0.2,0.4,0.2],1)
    imshow(plants)


def TREE(matrix,size,starti,startj,startL,startW,level,startangel,childnum,P,maxangel,C1,C2,LF,ChanceForFlower):
    if (level<0):
        return
    if (level==0):
        if rand()<ChanceForFlower:
            LF(matrix,size,starti,startj,startangel,1)
        else:
            LF(matrix,size,starti,startj,startangel,0)
        return
    origL=startL
    startL=startL*(0.7+0.3*rand())
    endi=starti-startL*cos(startangel)
    endj=startj-startL*sin(startangel)
    endC=[0,0,0]
    for k in range(3):
	endC[k]=C1[k]+(C2[k]-C1[k])/level
    anaf(matrix,size,starti,startj,startL,startW,startangel,C1,endC)
    for c in range(childnum):
	addangel=(2*rand()-1)*maxangel
        angel=startangel+addangel
	prop=P(addangel)
	L=origL*prop
    	W=startW*prop
    	if (W<1): 
        	W=1
        TREE(matrix,size,endi,endj,L,W,level-1,angel,childnum,P,maxangel,endC,C2, LF, ChanceForFlower)

#--------------------------
        
# pine:
def LFpine(matrix,size,starti,startj,startangel,IsFlower):
    DRY=rand()
    for alpha in (int(7*startangel-2), int(7*startangel+2)):
        for r in range(12):
            j=startj-r*sin(alpha/7.)
            i=starti-r*cos(alpha/7.)
            if (0<i<size) and (0<j<size):
                matrix[i][j]=[0.15+DRY*0.05,0.25-DRY*0.05,0.05]

def Proppine(angel):
    return (0.95-0.4*(sqrt(abs(angel))))

def pine(matrix,size,starti,startj,startL,startW,level): #recomended level: 7
	C1=[0.2,0.1,0.05]
	C2=[0.15,0.15,0.1]
	TREE(matrix,size,starti,startj,startL,startW,level,rand()*0.06-0.03,3,Proppine,0.6,C1,C2,LFpine,0.0)

#----------------------------

#shkedia
def LFshkedia(matrix,size,starti,startj,startangel,IsFlower):
    if (IsFlower==1):
    	for x in range (-2,2):
		for y in range(-2,2):
			i=starti-x*cos(startangel)-y*sin(startangel)
			j=startj-x*sin(startangel)+y*cos(startangel)
        		if (0<i<size) and (0<j<size):
                		matrix[i][j]=[1,0.4+0.3*sqrt(sqrt(x*x+y*y)),0.7+0.1*sqrt(sqrt(x*x+y*y))]
    else:
	if rand()<0.3:
	    for x in range(0,10):
		for y in range(-1,2):
			i=starti-x*cos(startangel)-y*sin(startangel)
			j=startj-x*sin(startangel)+y*cos(startangel)
			if (0<i<size) and (0<j<size):
                		matrix[i][j]=[0.1,0.15,0.1]



def PropShkedia(angel):
    return (1.3-1.*sqrt(abs(angel)))*(0.8+rand()*0.2)

def shkedia(matrix,size,starti,startj,startL,startW,level): #recomended level: 6
	C1=[0.1,0.05,0.0]
	C2=[0.0,0.15,0.0]
	TREE(matrix,size,starti,startj,startL,startW,level,rand()*0.06-0.03,4,PropShkedia,0.7,C1,C2,LFshkedia,0.7)

#-----------------------------------
#orange

def LForange(matrix,size,starti,startj,startangel,IsFlower):
    if (IsFlower==1):
        R=rand()
        C=[1-0.1*R, 0.5+0.1*R,0]
        for x in range(-5,6):
            for y in range(-5,6):
                if (x*x+y*y<25):
                    i=int(starti+x)
                    j=int(startj+y)
                    if (0<i<size) and (0<j<size):
                        matrix[i][j]=C
                
    else:
        if (rand()<0.6):
            DRY=rand()
            W=rand()*0.7
            L=8
            H=int(L/2)
            for x in range(L):
                tempW=int(W*(H-(H-x)*(H-x)/double(H)))
                for y in range(-tempW,tempW+1):
                    i=int(starti-x*cos(startangel)-y*sin(startangel))
                    j=int(startj+y*cos(startangel)-x*sin(startangel))
                    if (0<i<size) and (0<j<size):
                        matrix[i][j]=[DRY*0.1,0.1+DRY*0.2,DRY*0.05]

def PropOrange(angel):
    return 0.7-0.2*abs(angel)+(rand()*0.5-0.3)

def orange(matrix,size,starti,startj,startL,startW,level): #recomended level: 6
    C1=[0.1,0.05,0]
    C2=[0.05,0.15,0]
    TREE(matrix,size,starti,startj,startL,startW,level,rand()*0.06-0.03,5,PropOrange,0.8,C1,C2,LForange,0.01)


#-----------------------------------
#olive
def anaf_for_olive(matrix,size,starti,startj,L,W,angel):
    R=rand()*20
    for a in range(int(2*L)):
        BR=4*cos(R+starti+startj+a*a*0.0002)
        Left=1.3+0.3*cos(R+starti+a*0.001+a*a*0.0002)
        for b in range(-int(W*Left)+int(BR),int(W)+int(BR)):
            i=starti-0.5*a*cos(angel)-0.5*b*sin(angel)
            j=startj-0.5*a*sin(angel)+0.5*b*cos(angel)
	    Ctemp=[0,0,0]
            if (0<i<size) and (0<j<size):
                T=abs(sin(0.1*b*(1+a/W)+R)+sin(0.1*b*(1-a/W)+R))
                T=T/2.
                matrix[i][j]=[0.1+0.15*T,0.05+0.015*T,0.+0.15*T]
                
def TREE_FOR_OLIVE(matrix,size,starti,startj,startL,startW,level,startangel,ChanceForFlower=0.01):
    if (level<0):
        return
    if (level<=1):
        if rand()<ChanceForFlower:
            LFolive(matrix,size,starti,startj,startangel,1)
        else:
            LFolive(matrix,size,starti,startj,startangel,0)
        if (level==0):
            return
    origL=startL
    startL=startL*(0.1+0.9*rand())
    endi=starti-startL*cos(startangel)
    endj=startj-startL*sin(startangel)
    
    anaf_for_olive(matrix,size,starti,startj,startL,startW,startangel)
    if(rand()<0.0): # impossible for now
        addangel=(2*rand()-1)*0.2
        angel=startangel+addangel
        TREE_FOR_OLIVE(matrix,size,endi,endj,origL*0.8,startW,level,angel,ChanceForFlower)
    else:
        childnum=randint(2)+3
        for c in range(childnum):
            angel=startangel+(2*c-double(childnum-1))/(2.4*childnum) + 0.4*rand()-0.2
            L=origL*(0.8+rand()*0.1)
            L=L*(1-abs(c-(childnum-1)/2.)*0.05)
            W=startW*(1-0.12*childnum)
            SIGN=sign(c-(childnum-1)/2.)
            ei=endi+sin(angel)*startW*SIGN/3.2
            ej=endj-cos(angel)*startW*SIGN/3.2
            if (W<1): 
                W=1
            TREE_FOR_OLIVE(matrix,size,ei,ej,L,W,level-1-randint(2),angel,ChanceForFlower)


def olive_internal_leaf(matrix,size,starti,startj,startangel):
            Light=0.8*rand()+0.2
            W=rand()*0.6
            L=7
            H=int(L/2)
            for x in range(L):
                tempW=int(W*(H-(H-x)*(H-x)/double(H)))
                for y in range(-tempW,tempW+1):
                    i=int(starti-x*cos(startangel)-y*sin(startangel))
                    j=int(startj+y*cos(startangel)-x*sin(startangel))
                    if (0<i<size) and (0<j<size):
                        matrix[i][j]=[0.4*Light,0.5*Light,0.3*Light]
    



def LFolive(matrix,size,starti,startj,startangel,IsFlower):
    if (IsFlower==1):
        R=0.7*rand()+0.3
        C=[0.15*R, 0.25*R,0.1*R]
        for x in range(-5,6):
            for y in range(-5,6):
                if (x*x+2*y*y<16):
                    i=int(starti+x)
                    j=int(startj+y)
                    if (0<i<size) and (0<j<size):
                        matrix[i][j]=C
                
    else:
        olive_internal_leaf(matrix,size,starti,startj,startangel)

def olive(matrix,size,starti,startj,startL,startW,level): #recomended level: 10
    TREE_FOR_OLIVE(matrix,size,starti,startj,startL,startW,level,0.0,0.0)
    #TREE_FOR_OLIVE(matrix,size,starti,startj,startL*0.9,startW*0.7,level-1,0.0) # yes, twice


#-------------------------------------
#klil hahoresh

picklil=zeros((21,21,3))+1
for i in range(21):
    for j in range(21):
        picklil[i][j]=[1,1,1]
        x=i-10
        y=j-10
        R2=x*x+y*y
        if ((R2*R2)/4+(x-abs(y))*(x-abs(y))*(x-abs(y))<300):
            picklil[i][j]=[0,0.2,0]
            
def LFKlil(matrix,size,starti,startj,startangel,IsFlower):
    if (IsFlower==1):
        for k in range(randint(4)+2):
            base=(starti+3*k*cos(startangel)+randint(5)-2,startj+3*k*sin(startangel)+randint(5)-2)
            R=rand()
            C=[1,0.1+0.3*R, 0.8+0.2*R]
            for x in range(-1,2):
                for y in range(-1,2):
                    i=int(base[0]+x)
                    j=int(base[1]+y)
                    if (0<i<size) and (0<j<size):
                        matrix[i][j]=C
                
    else:
        DRY=rand()*0.2
        #for i in range(21):
         #   for j in range(21):
          #      ni=int(starti-(i-10)*cos(startangel)+(j-10)*sin(startangel))
           #     nj=int(startj+(i-10)*sin(startangel)+(j-10)*cos(startangel))
                #if (picklil[i][j][0]!=1) and (0<ni<400) and (0<nj<400):
                 #   matrix[ni][nj]=picklil[i][j]+DRY

                #if not((i>10) and abs(i-10)>abs(j-10)):
                    #matrix[ni][nj]=[DRY,DRY+0.2,DRY]
        starti=int(starti)
        startj=int(startj)
        for i in range(-6,7):
            for j in range(-6,7):
                x=i+starti
                y=j+startj
                if  (0<x<400) and (0<y<400) and (i*i+j*j<37):
                    matrix[x][y]=[DRY,DRY+0.2,DRY]
                    
                    


def PropKlil(angel):
    return 0.7+rand()*0.2
 #TREE(plants,400,400,200,70,10,8,0.0,3,PropKlil,0.8,[0.1,0,0],[0.0,0.2,0],LFKlil,0.1)
#-------------------------------------
# grass


def LFgrass(matrix,size,starti,startj,startangel,IsFlower):
  return

def PropGrass(angel):
    return 0.9-0.1*abs(angel)+(rand()*0.5-0.3)

def grass(matrix,size,starti,startj,startL,startW,level): #recomended level: 2
    C1=[0.05,0.15+rand()*0.3,0]
    C2=[0.15,C1[1]+0.05,0]
    TREE(matrix,size,starti,startj,startL,startW,level,rand()*0.6-0.3,3,PropGrass,1.1,C1,C2,LFgrass,0.0)



#------------------------------------------------
# anemone

Ane=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/pics/anemone.png")
Ane=img_as_float(Ane)
temp=zeros((85,105,3))+1
for i in range(85):
    for j in range(105):
        for k in range(3):
            temp[i][j][k]=Ane[i][j][k]
Ane=temp

a2=zeros((85,105,3))+1
for i in range(85):
    for j in range(105):
        a2[i][j]=Ane[i][104-j]
        

def anemone():
    a3=zeros((170,105,3))+1
    R=min(max(rand()*3-1,0),0.9)
    #C=[1,R*rand(),R]
    C=[1,0.9,0.9]
    if (R==0.9):
        C[1]=0.85
    for i in range(85):
        for j in range(105):
            a3[i][j]=Ane[i][j]
    strech=4*rand()-1
    if (strech>0):
        strech=strech/3
        
    if (strech<0):
        for i in range(80):
            for j in range(105):
                R=((i-80)*(i-80)+(j-52)*(j-52))/10000.
                if (a3[i][j][0]!=a3[i][j][1]): #which means it's red
                    for k in range(3):
                        a3[i][j][k]=C[k]+(1-C[k])*(1-R)**10/2
        for i in range(80):
            for j in range(105):
                R=((i-80)*(i-80)+(j-52)*(j-52))/10000.
                x=80-(80-i)*strech
                y=j
                a3[x][y]=a2[i][j]
                if (a3[x][y][0]!=a3[x][y][1]): #which means it's red
                    for k in range(3):
                        a3[x][y][k]=C[k]+(1-C[k])*(1-R)**10/2             
    else:
        for i in range(85):
            for j in range(105):
                R=((i-85)*(i-85)+(j-52)*(j-52))/10700.
                if (a3[i][j][0]!=a3[i][j][1]): #which means it's red
                   for k in range(3):
                        a3[i][j][k]=C[k]+(1-C[k])*(1-R)**10/2
        for i in range(85):
            for j in range(105):
                R=((i-85)*(i-85)+(j-52)*(j-52))/10700.
                x=85-(85-i)*strech
                y=j
                if (a2[i][j][1]==0.):
                    for k in range(3):
                        a3[x][y][k]=0.7*C[k]+0.6*(1-C[k])*(1-R)**10/2
    return a3



#-------------------------------------

def old_butterfly(high,angel=0):
    orig=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/pics/buterfly.png")
    orig=img_as_float(orig)
    shape(orig)
    dest=zeros((high+81,high+81,3))+1
    R=rand()
    G=rand()
    #C=[rand(),min(2*R,1),min(2-R*2,1)]
    C=[rand(),rand(),rand()]
    T=max(C)
    for k in range(3):
        if (C[k]==T):
            C[k]=1

    #colorlines=zeros(32)
    #for i in range(32):
    #    colorlines[i]=rand()
    C2=[(rand()+1)/2.,(rand()+1)/2.,(rand()+1)/2.]
    T=max(C2)
    for k in range(3):
        if (C2[k]==T):
            C2[k]=1

    for x in range(81):
        for y in range(81):
            i=(x-40)*cos(angel)+(y-40)*sin(angel)+16
            j=-(x-40)*sin(angel)+(y-40)*cos(angel)
            if (j<0):
                j=-j
            if (0<i<32) and (0<=j<25):
                if (orig[i][j][0]==0):
                    R1=(i-7)*(i-7)+(j-12)*(j-12)+5
                    R2=(i-20)*(i-20)+(j-7)*(j-7)+5
                    for k in range(3):
                        dest[x][y+high/2][k]=C[k]+(C2[k]-C[k])*(3/R1+3/R2)
                if (0.4<orig[i][j][0]<0.5):
                        dest[x][y+high/2]=[C[1],C[2],1-C[0]]
                if (0.7<orig[i][j][0]<0.8):
                        dest[x][y+high/2]=[rand()*0.5,G,rand()*0.5]

    return dest 

          

#-------------------------------------
# 3D placing

def plant_grass_for_10_percent_ground(size=1000,num=10000):
    OS=size
    M=restart_background(size, 0.93)
    for i in range(int(size*9/10),size):
        for j in range(size):
            M[i][j]=[0.15+(size-i)/(0.3*size),0.05+(size-i)/(0.3*size),0+(size-i)/(0.2*size)]
    for i in range(num):    
            OS=20
            TRY=zeros((OS,OS,3))+1
            grass(TRY,OS,OS,OS/2,15+randint(5),3,2)
            if (i%200==0):
                print i,
            place(TRY,OS,M,size,randint(size), 25-25.*i/num, 0.16*size, 0.04, [0.8,0.8,0.9],1)
    TRY=zeros((SIZE,SIZE,3))+1
    return M 
        
def build_buterfly_old_ignore():	
    S=100
    C=zeros((3,3))
    for i in range(3):
        for j in range(3):
            C[i][j]=rand()
        C[i][argmax(C[i])]=1.
        for j in range(3):
            C[i][j]=i/2

    B=zeros((S,S,3))+1
    Param=rand()
    Param2=rand()
    for i in range(S):
        for j in range(S):
            #B[i][j]=[0.8,0.8,1]
            if ((i-S)**2+j**2<0.35*S*S) and ((i-0.9*S)**2+(j-S*4/5.)**2>0.35*S*S) and ((i-0.6*S)-1.5*j<0):
                #temp=(sin(((i-0.6*S)**2+(j-S)**2)/(12*S))+sin(((i-0.8*S)**2+(j-0.5*S)**2)/(2*S))+(i*i/100.+j*j/100.)%1++2)/5.
                temp=abs(0.5*sin(((i-0.4*S)**2+(j+0.2*S)**2+j)/400.-1)+0.7*(((i-0.4*S)**2/(j+0.2*S))%0.5))
                for k in range(3):
                    B[i][j][k]=temp#(0.5-0.5*temp)*(C[1][k]+C[1][k])+temp*C[2][k]
            if ((i-S*0.6)**2+(j-S*0.4)**2<S*S*0.3) and ((i+0.1*S)**2+(j+S*0.3)**2<S*S*0.8) and ((i+0.4*S)**2+(j-0.4*S)**2<0.8*S*S):
                temp=(abs(sqrt((1.8*(i+3*(Param+0.5)-0.2*S))**2+(j-0.3*S)**2)/45.-0.1) + (((i-60)/50.)**2+((j+11)/(70.+3*Param2))**2)+(i*i/100.+j*j/200.)%0.05)
                #temp=temp+0.1*(((i-0.2*S)**2/(5*j+0.01*S))%3)
                if (temp>1) or (temp<0):
                    temp==0.99
                for k in range(3):
                    B[i][j][k]=temp#*C[2][k]+C[1][k]*(1-temp)*0.5
            if (j**2+0.01*(i-0.4*S)**2<S/15.):
                B[i][j]=[0.5,0.5,0.5]#[0,0.6,0]
    B2=zeros((S,2*S,3))+1
    for i in range(S):
        for j in range(S): 
            B2[i][S+j]=B[i][j]
            B2[i][S-j]=B[i][j]          
    imshow(B2)

@jit
def Buterfly(Size):
    A1=2*rand()-1
    A2=2*rand()-1
    if max(abs(A1),abs(A2))<0.2:
        A1=1.
    Angel=rand()*pi*sign(A1)
    direction=randint(2)
    orig=skimage.io.imread(u"C:/Users/myPc/Documents/graphics_2015/pics/buterfly.png")
    orig=img_as_float(orig)
    B=zeros((Size,Size,3))+1
    C2=[rand(),0.7*rand(),rand()]
    #C2[argmax(C2)]=1.
    #C2[argmin(C2)]=0.
    C=[1,1,1]
    C[randint(3)]=1-rand()*0.2
    C[randint(3)]=1-rand()*0.3

    for i in range(Size):
        for j in range(Size):
            x=int(((i-Size/2.)*cos(Angel)+(j-Size/2.)*sin(Angel))*170./Size+50)
            y=int(((j-Size/2.)*cos(Angel)-(i-Size/2.)*sin(Angel))*170./(A1*Size))
            x=x*direction+(119-x)*(1-direction)
            if (0<x<170) and (0<y<170):
                if (orig[x][y][0]!=1):
                    if (orig[x][y][0]==orig[x][y][1]):
                        for k in range(3):
                            B[i][j][k]=orig[x][y][0]*C[k]+(1-orig[x][y][0])*C2[k]
                    else:
                        B[i][j]=[0,0.4,0]
    for i in range(Size):
        for j in range(Size):
            x=int(((i-Size/2.)*cos(Angel)+(j-Size/2.)*sin(Angel))*170./Size+50)
            y=int(((j-Size/2.)*cos(Angel)-(i-Size/2.)*sin(Angel))*170./(A2*Size))
            x=x*direction+(119-x)*(1-direction)
            if (0<x<170) and (0<y<170):
                if (orig[x][y][0]!=1):
                    if (orig[x][y][0]==orig[x][y][1]):
                        for k in range(3):
                            B[i][j][k]=orig[x][y][0]*C[k]+(1-orig[x][y][0])*C2[k]
                    else:
                        B[i][j]=[0,0.4,0]
    return B

def Buterfly2(Size):
    S=Size/3
    C=zeros((3,3))
    for i in range(3):
        for j in range(3):
            C[i][j]=rand()
        C[i][argmax(C[i])]=1.
        for j in range(3):
            C[i][j]=i/2
    #X1=randint(3)
    #X2=randint(3)
    B=zeros((S,S,3))+1 
    Param2=0.3+rand()
    Param=0.7+Param2+rand()
    Param3=0.04+0.04*rand()*rand()
    I1=randint(3)
    I2=(I1+randint(2)+1)%3
    I3=randint(3)
    Param4=rand()
    Param5=rand()
    for i in range(S):
        for j in range(S):
            if ((i-S)**2+j**2<0.35*S*S) and ((i-0.55*S)**2+(j+0.0*S)**2<0.13*S*S) and ((i-0.5*S)-1.2*j<0): #((i-0.9*S)**2+(j-S*4/5.)**2>0.35*S*S)
                #temp=abs((abs((Param*(i-0.35*S)/(j+0.2*S))%0.4-0.2)+abs((Param2*((i-0.9*S)**2+(j-S*4/5.)**2)/(S*S))%0.4-0.2))%0.2-0.1)
                temp=((i-0.57*S)**2+(j-0.15*S)**2)/(0.6*S*S)
                temp=(1-temp)
                for k in range(3):             
                    B[i][j][I3]=abs((temp*8)%2-1)
                    B[i][j][(I3+1)%3]=abs((temp*8-0.5)%2-1)
                    B[i][j][(I3+2)%3]=abs((temp*8-0.2)%2-1)
            if ((i-S*0.6)**2+(j-S*0.4)**2<S*S*0.3) and ((i+0.1*S)**2+(j+S*0.3)**2<S*S*0.8) and ((i+0.4*S)**2+(j-0.4*S)**2<0.8*S*S):
                for k in range(3):
                    B[i][j][k]=0
                #if ((i+0.1*S)**2+(j+S*0.3)**2<S*S*0.65) and ((i-S*0.6)**2/(S*S*0.3-(j-S*0.4)**2))%0.15<0.04:
                temp=19*abs((((i-S*0.6)**2/(S*S*0.3-(j-S*0.4)**2))%Param3)-Param3/2.)+0.7
                temp=sqrt(temp)
                temp=temp-1*((i+0.005*S)**2+(j+S*0.3)**2)/(S*S*0.85)
                if (temp<0):
                    temp=-0.0
                temp=temp+0.0
                if (temp>1): 
                    temp=1
                #B[i][j][0]=temp
                #B[i][j][1]=temp
                #B[i][j][2]=temp
                B[i][j][I1]=min(temp*2,1)
                B[i][j][I2]=min((temp*5)%3,1)
                B[i][j][(I2+1)%3]=Param4*max(1-temp,0)
                if (temp==0):
                    B[i][j][I1]=temp 
                    B[i][j][I2]=temp
            if (j**2+0.01*(i-0.4*S)**2<S/15.):
                B[i][j]=[0.1,0.4+0.6*double(i)/S,0.1]#[0,0.6,0]
    B2=zeros((Size,Size,3))+1
    angel=rand()*2*pi
    for i in range(S):
        for j in range(S):
            i2=i*cos(angel)+j*sin(angel)
            j2=j*cos(angel)-i*sin(angel)
            B2[S+i2][S+j2]=B[i][j]
            i2=i*cos(angel)-j*sin(angel)
            j2=-j*cos(angel)-i*sin(angel)
            B2[S+i2][S+j2]=B[i][j]
    return B2


