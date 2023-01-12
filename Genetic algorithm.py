import random
import math
import pygame
import time

####Fix co-ords to match the pygame stuff


#pygame stuff for the screen
width,height=400,400
bgcolour=150,150,150
screen=pygame.display.set_mode((width,height))
screen.fill((bgcolour))
goalsprite=pygame.draw.circle(screen,(210,190,0),[50,200],15,0)
wallsprite=pygame.image.load("square.png")
popsize=100
#dotsprite=pygame.draw.circle(screen,(0,0,0),[200,200],10,0)
pygame.display.update()

goalpos=[50,200]
gen=0
def RANDvector(magRANGE):
  mag=random.random()*magRANGE#A random float between 0 and magRANGE
  angle=random.random()*2*math.pi#A random angle
  newx=math.cos(angle)*mag#The x compnent of the vector
  newy=math.sin(angle)*mag#The y compnent of the vector
  return [newx,newy]
class wall:
  def __init__(self,pos,height,width):
    self.pos=pos
    self.height=height
    self.width=width
    self.sprite=pygame.transform.scale(wallsprite,(width,height))
  def collide(self,dotpos):
    print(self.pos[0],dotpos)
    if self.pos[0]<=dotpos[0]<=self.pos[0]+self.width and self.pos[1]<=dotpos[1]<=self.pos[1]+self.height:
      return True
    else:
      return False
#The dot and how it moves
class dot:
  def __init__(self,pos,vel,acc,mind,steps,dead,goal):
    self.pos=pos#List containing an x and y co-ordinate
    self.vel=vel#List containing an x and y velocity
    self.acc=acc#List containing an x and y acceleration
    self.mind=mind#List of the random accelerations
    self.steps=steps#Time counter
    self.dead=dead#Whether or not it is alive
    self.goal=goal#Whether or not it has reached its goal
    self.dotsprite=pygame.draw.circle(screen,(0,0,0),self.pos,5,0)
  def move(self):
    #Reducing the velocity so that it does not accelerate into the distance.
    if self.vel[0]!=0:#Validation check (divide by zero)
      sign=self.vel[0]/abs(self.vel[0])#Find the direction
      if sign==1:#IF it is going forward
        self.vel[0]=self.vel[0]%100#Take the velocity mod 5
      else:#If it is going backwards
        self.vel[0]=self.vel[0]%100-100#Take the velocity mod 5 and subtact five to get the equivilant of the positive velocity mod 5 negated

    #Same code for the other axis
    if self.vel[1]!=0:
      sign=self.vel[1]/abs(self.vel[1])
      if sign==1:
        self.vel[1]=self.vel[1]%100
      else:
        self.vel[1]=self.vel[1]%100-100
      
    self.pos[0]+=self.vel[0]#Add the velocity to the position
    self.pos[1]+=self.vel[1]
    self.vel[0]+=self.acc[0]#Add the acceleration to the velocity
    self.vel[1]+=self.acc[1]
    #print(len(self.mind))
    self.acc=self.mind[self.steps]#Get a new acceleration
    self.steps+=1#Increase the time (nbumber of steps)
    
  def update(self):
    if self.goal==False:#If it has not reached the goal
      if self.dead==False:#If it has not died
        self.move()#Move
        if self.pos[0]<=0 or self.pos[1]<=0 or self.pos[0]>=400 or self.pos[1]>=400:#If it is out of bounds
          self.dead=True #Kill it
        #print(self.pos)
        for i in walls:
          
          if i.collide(self.pos):
            self.dead=True
            print("f")
        if 35<=self.pos[0]<=65 and 185<=self.pos[1]<=215:#If it reaches the goal
          self.goal=True#It has reached the goal
          print("GG")
  def fitness(self):
    fit=0
    if self.goal==True:
      fit=1/16+1000000/self.steps**2
    else:
      d2=(50-self.pos[0])**2+(200-self.pos[1])**2
      d=math.sqrt(d2)
      fit=1/(d**2)#The fitnesss function is inversely proportional to distance squared
    return fit
    
  def show(self):#Come back to this
    #screen.fill(bgcolour)
    self.dotsprite=pygame.draw.circle(screen,(0,0,0),self.pos,5,0)
class brain:
  def randacc(self):
    list=[]#List of random accelerations
    for i in range(150):#Repeat thirty times
      newVector=RANDvector(5)#Create a new vector between 0 and 5 in length
      list.append(newVector)#Adding the vector to the list of accelerations
    return list
    
  def mutate(self,brainlist):#FIX
    prob=0.01#
    for i in range(len(brainlist)):#Repeat for each item in the list to see if it should be mutated
      num=random.randint(1,50)#Random number: will be used to determine whether or not to mutate
      if num==7:#If true then it will mutate
        mutation=RANDvector(5)#Create a new random acceleration vector
        brainlist[i]=mutation#Replace this item with the new vector
    returning=[]#List of the brainlists
    for i in brainlist:
      returning.append(i)
    return returning
class population:
  def __init__(self,size,brainlist):
    self.size=size
    self.dots=[]
    for i in range(self.size):
      self.dots.append(dot([390,200],[0,0],[0,0],brainlist[i],0,False,False))
    self.newdots=[]
    for i in range(len(self.dots)):
      self.newdots.append(0)
    self.brainlist=brainlist
  
  def sumfit(self):
    sum=0
    for i in self.dots:
      sum+=i.fitness()
    return sum

  def selectparent(self):
    list=[]
    print(self.newdots)
    for i in self.newdots:
      num=random.random()
      runningsum=0
      for j in self.dots:#Create a running
        rs=runningsum#Placeholder
        runningsum+=j.fitness()
        #print(runningsum)
        lower=rs/self.sumfit()
        upper=runningsum/self.sumfit()
        if lower<=num<=upper:
          list.append(j.mind)
          #print("g")
      #print("h")
    return list
    
  def popupdate(self):
    for i in self.dots:
      i.update()

  def popshow(self):
    screen.fill((150,150,150))
    pygame.draw.circle(screen,(210,190,0),[50,200],15,0)
    for i in walls:
      screen.blit(i.sprite,(i.pos[0],i.pos[1]))
    #self.bestdot().show()
    for i in self.dots:
      i.show()
    pygame.display.update()
    time.sleep(0.1)
  def popfit(self):
    fits=[]
    for i in self.dots:
      fits.append(i.fitness())
    return fits

  def deaddots(self):
    popdead=True#All dots so far are dead
    for i in self.dots:#check every dot
      if i.dead!=True and i.goal!=True:#Check if they are not dead
        popdead=False#Tell them they are alive
    return popdead#Return
      
  def bestdot(self):
    bestfit=0
    bestdot=0
    for i in self.dots:
      newfit=i.fitness()
      if newfit>bestfit:
        bestfit=newfit
        bestdot=i
    #print(bestdot)
    return bestdot
    
  def meandot(self):
    sumx=0
    sumy=0
    fitsum=0
    for i in self.dots:
      sumx+=i.pos[0]
      sumy+=i.pos[1]
      fitsum+=i.fitness()
    avx=sumx/len(self.dots)
    avy=sumy/len(self.dots)
    avfit=fitsum/len(self.dots)
    return [avx,avy],avfit
def poprun(pop1):
  for i in pop1.dots:###FLAG
    if pop1.dots.index(i)==2:
      print(len(i.mind))
      
  for i in range(149):#Run for 150 steps
    if pop1.deaddots()==False:#If there are dots alive
      pop1.popupdate()
      pop1.popshow()
      #pygame.display.update()


    



      
  list=pop1.selectparent()
  lists=[]
  lists.append(pop1.bestdot().mind)
  
  print(len(list[0]))
      
  for i in range(len(pop1.dots)):
    nextgen=brain1.mutate(list[i])
    lists.append(nextgen)
   
  #print(pop1.bestdot().brain)
  
  #pop1.bestdot().steps=0
  #print(pop1.bestdot().pos,pop1.bestdot().fitness())
  for i in range(499):
    #print(i)
    pop1.bestdot().update()
    pop1.bestdot().show()
  pop1.size+=1
  
  return lists

def run():
  brain1=brain()
  dot1=dot([390,200],[0,0],[0,0],brain1.randacc(),0,False,False)
  for i in range(150):
    #print(dot1.pos,dot1.fitness())
    dot1.update()
    dot1.show()
    print(dot1.dead)
  return dot1.fitness()
#run()

#run()

#Running the actual code

#run()


brain1=brain()
lists=[]
for i in range(popsize):
  list=brain1.randacc()
  lists.append(list)

walls=[wall([200,200],200,30),wall([300,0],200,30)]
#walls=[]

for i in range(50):#Repeat for each generation
  pop1=population(popsize,lists)
  lists=poprun(pop1)#Run the code
  #print(len(lists[0]))  
  #poprun(pop1)
