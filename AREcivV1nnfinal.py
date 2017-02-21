###############################################################################
#                                  ಠ_ಠ  CIV  ಠ_ಠ                              #
###############################################################################

# from pylab import *
import numpy as np
from random import *
from tkinter import *
from PIL import Image, ImageTk

#legend of the map
legend={4:"dry",2:"basic",1:"fertil",6:"desert",5:"mountains",3:"mine"}
#on a map, unit digit gives you the type of field and the other remaining 
#digits give you the civilisation that control the land(if there's no other 
#digit then the field is free).

###############################################################################
#                             ಠ_ಠ  IMPORTANT VARIABLES  ಠ_ಠ                   #
###############################################################################

print("enter the standard productivity")
productivity = int(input())  #between 1 and 100
print("enter the standard agressivity")
agressivity = int(input())   #between 0 and 100

expansion = 1 #expansion rate

food = 0        #ressources
iron = 0

civ_counter = 0 #counts civ
list_civ = [] #civ list containing all civs

###############################################################################
#                                ಠ_ಠ  THE MAP  ಠ_ಠ                            #
###############################################################################
def create_map_random():
    '''
    generate a random map with a certain percentage of each type of biome.
    '''
    m=np.random.randint(0, 1, (40,40))
    for i in range(0,len(m)):
        for j in range(0,len(m[i])):   
            rand=random()
            if rand<=0.1:
                m[i][j]=4               #generate a desert
            elif rand<=0.15:
                m[i][j]=5               #generate a mountain
            elif rand<=0.25:
                m[i][j]=6               #generate a mine
            elif rand<=0.5:
                m[i][j]=1               #generate an arid field
            elif rand<=0.85:
                m[i][j]=2               #generate a basic field
            elif rand<=1:
                m[i][j]=3               #generate a fertil field
    return m
    
def test_map_generation(m):
    '''
    give the presence's percentage of every biome.
    '''
    count={1:0,2:0,3:0,4:0,5:0,6:0}
    for i in range(0,len(m)):
        for j in range(0,len(m[i])):
            if m[i][j]==1:
                count[1]+=1
            elif m[i][j]==2:
                count[2]+=1
                
            elif m[i][j]==3:
                count[3]+=1
                
            elif m[i][j]==4:
                count[4]+=1
                
            elif m[i][j]==5:
                count[5]+=1
                
            elif m[i][j]==6:
                count[6]+=1
    print("dry:")
    print(int(100*(count[1]/(len(m)*len(m)))))
    print("basic")
    print(int(100*(count[2]/(len(m)*len(m)))))
    print("fertil")
    print(int(100*(count[3]/(len(m)*len(m)))))
    print("desert")
    print(int(100*(count[4]/(len(m)*len(m)))))
    print("mountains")
    print(int(100*(count[5]/(len(m)*len(m)))))
    print("mine")
    print(int(100*(count[6]/(len(m)*len(m)))))
    return count
    
###############################################################################
#                           ಠ_ಠ  THE CIVILISATIONS  ಠ_ಠ                       #
###############################################################################

def create_civ(t):
    '''
    t is the type of civilisation : expert,warrior or moderate
    return a civilisation caracteristics :
    [civname,agressivity,productivity,expansion rate,civ_number,expand_next_iteration,scientific_level]
    '''
    global civ_counter
    if t == "expert":
        new_productivity = 5*productivity
        new_agressivity = agressivity
        new_expansion = expansion
        civ_counter += 1
        expand_next_iteration = 0
        civ = [t,new_agressivity,new_productivity,new_expansion,civ_counter,expand_next_iteration]
        list_civ.append(civ)
        return civ
        
    elif t == "warrior":
        new_productivity = productivity
        new_agressivity = 10*agressivity
        new_expansion = 3*expansion
        civ_counter += 1
        expand_next_iteration = 0
        civ = [t,new_agressivity,new_productivity,new_expansion,civ_counter,expand_next_iteration]
        list_civ.append(civ)
        return civ
        
    elif t == "moderate":
        new_productivity = 2*productivity
        new_agressivity = 2*agressivity
        new_expansion = 2*expansion
        civ_counter += 1
        expand_next_iteration = 0
        civ = [t,new_agressivity,new_productivity,new_expansion,civ_counter,expand_next_iteration]
        list_civ.append(civ)
        return civ
    
    else:
        print("the type of civilisation enterred isn't supported please retry by relaunching the function")
    
def spawn_civ(civ,m,x,y):
    '''
    spawns a civilisation on the map. Returns the new map.
    '''
    m[x][y] = m[x][y]+civ[4]*10  #adds a second digit containing civ number
    return m
###############################################################################
#                             ಠ_ಠ  THE DYNAMICS  ಠ_ಠ                          #
###############################################################################

def dynamics_civ(civ,m):
    """moves a civ on a map m, depending on many factors :
    if the civ is warrior : 3 squares conquered.
    if the civ is expert : 1 squares conquered.
    if the civ is moderate : 2 squares conquered
    then, depending on the square conquered, civ will have to wait some turns to be able to reconquer a new square:
    if mountain : 50turns
    if desert : 30 turns
    if anything else : 10 turns
    """
    global list_civ
    new_m = m
    next_turn = 1  # depends on expansion rate, allowing multiple moves
    skip = True # same
    if (new_m>=10).all():  # this comparison checks if all elements in m are above 10, and if it does, m is filled so we don't want to change anything.
        return new_m
    elif list_civ[civ[4] - 1][5] > 0:  # this comparison is to check that the civ is allowed to move again.
        list_civ[civ[4] - 1][5] -= 1
    else:                               # here we allow the civ to expand
        while next_turn > 0:
            new_pos_x = "fix"  # to fix a bug(civ2 having no place to move then no value for new_pos)
            new_pos_y = "fix"  # same
            k = 0  # index for first new place for comparison purpose
            for i in range(len(new_m)):   # going through all the map
                for j in range(len(new_m[i])):
                    [x,y] = check_surroundings(new_m,i,j)  # getting m[i][j] best surroundings pos.
                    if new_m[i][j] >= civ[4]*10 and new_m[i][j]<=9 + civ[4]*10 and new_m[x][y]<10:  # checks if the square is occupied by civ, and that the best surroundings aren't occupied.
                        if k == 0:  # gives initial value
                            new_pos_x = x  # sets new pos to affect, initial one
                            new_pos_y = y
                            k += 1
                        elif m[new_pos_x][new_pos_y]> m[x][y]:  # comparison for best place
                            new_pos_x = x  # sets new pos to affect, not initial one
                            new_pos_y = y
            next_turn -= 1          # removes a step from expanding
            if civ[3] == 2 and skip:  # this if allows one more step for moderate civ
                next_turn += 1
                skip = False
            elif civ[3] == 3 and skip:  # this if allows 2 more steps for warrior civ, expert civ won't get extra move.
                next_turn += 2
                skip = False
            if new_pos_x != "fix" and new_pos_y != "fix":    # to fix the bug above
                if civ[5] == 0:                            # this if allows waiting for next expand, depending on biome.
                    if new_m[new_pos_x][new_pos_y] == 5:
                        list_civ[civ[4] - 1][5] = 50
                    elif new_m[new_pos_x][new_pos_y] == 6:
                        list_civ[civ[4] - 1][5] = 30
                    elif new_m[new_pos_x][new_pos_y] == 1 or new_m[new_pos_x][new_pos_y] == 2 or new_m[new_pos_x][new_pos_y] == 3 or new_m[new_pos_x][new_pos_y] == 4:
                        list_civ[civ[4] - 1][5] = 10

                new_m[new_pos_x][new_pos_y] += civ[4]*10 # gives new value

    #print(new_m)  # for tests
    #print("\n")   # for tests
    return new_m


#max land

def check_surroundings(m,x,y):   # checks best surroundings in + shape with m[x][y] at middle. Allows spheric map(returning to left if at right and moving left, same vertically)

    if x+1<len(m) and m[x+1][y] == 1:
        return [x+1, y]
    elif y-1<len(m) and m[x][y-1] == 1:
        return [x,y-1]
    elif x-1<len(m) and m[x-1][y] == 1:
        return [x-1,y]
    elif y+1<len(m) and m[x][y+1] == 1:
        return [x,y+1]

    elif x+1<len(m) and m[x+1][y] == 2:
        return [x+1,y]
    elif y-1<len(m) and m[x][y-1] == 2:
        return [x,y-1]
    elif x-1<len(m) and m[x-1][y] == 2:
        return [x-1,y]
    elif y+1<len(m) and m[x][y+1] == 2:
        return [x,y+1]

    elif x+1<len(m) and m[x+1][y] == 3:
        return [x+1, y]
    elif y-1<len(m) and m[x][y-1] == 3:
        return [x, y-1]
    elif x-1<len(m) and m[x-1][y] == 3:
        return [x-1, y]
    elif y+1<len(m) and m[x][y+1] == 3:
        return [x, y+1]

    elif x+1<len(m) and m[x+1][y] == 4:
        return [x+1,y]
    elif y-1<len(m) and m[x][y-1] == 4:
        return [x,y-1]
    elif x-1<len(m) and m[x-1][y] == 4:
        return [x-1,y]
    elif y+1<len(m) and m[x][y+1] == 4:
        return [x,y+1]

    elif x+1<len(m) and m[x+1][y] == 5:
        return [x+1,y]
    elif y-1<len(m) and m[x][y-1] == 5:
        return [x,y-1]
    elif x-1<len(m) and m[x-1][y] == 5:
        return [x-1,y]
    elif y+1<len(m) and m[x][y+1] == 5:
        return [x,y+1]

    elif x+1<len(m) and m[x+1][y] == 6:
        return [x+1,y]
    elif y-1<len(m) and m[x][y-1] == 6:
        return [x,y-1]
    elif x-1<len(m) and m[x-1][y] == 6:
        return [x-1,y]
    elif y+1<len(m) and m[x][y+1] == 6:
        return [x,y+1]
    else:
        return [x,y]


def civ_color(civ_number):
    new_number = int(civ_number)
    if new_number == 1:
        return "red"
    elif new_number == 2 :
        return "blue"
    elif new_number == 3:
        return "black"

# for tests
m = create_map_random()
print(m)
print("\n")
create_civ("warrior")
m = spawn_civ(list_civ[0],m,0,0)
create_civ("expert")
m = spawn_civ(list_civ[1],m,15,15)
create_civ("moderate")
m = spawn_civ(list_civ[2],m,30,30)   # 3 civs
print(m)
print("\n")
for z in range(1000):
    m = dynamics_civ(list_civ[0], m)
    m = dynamics_civ(list_civ[1], m)
    m = dynamics_civ(list_civ[2], m)
print(m)

# tests result : 1000 turns one square left, for 3civs

# tests for image

root = Tk()
image1 = Image.open("image1.gif")
image1 = image1.resize((20, 20), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)
image2 = Image.open("image2.gif")
image2 = image2.resize((20, 20), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(image2)
image3 = Image.open("image3.gif")
image3 = image3.resize((20, 20), Image.ANTIALIAS)
image3 = ImageTk.PhotoImage(image3)
image4 = Image.open("image4.gif")
image4 = image4.resize((20, 20), Image.ANTIALIAS)
image4 = ImageTk.PhotoImage(image4)
image5 = Image.open("image5.gif")
image5 = image5.resize((20, 20), Image.ANTIALIAS)
image5 = ImageTk.PhotoImage(image5)
image6 = Image.open("image6.gif")
image6 = image6.resize((20, 20), Image.ANTIALIAS)
image6 = ImageTk.PhotoImage(image6)
# same with borders possible
bor_image1 = Image.open("image1.gif")
bor_image1 = bor_image1.resize((16, 16), Image.ANTIALIAS)
bor_image1 = ImageTk.PhotoImage(bor_image1)
bor_image2 = Image.open("image2.gif")
bor_image2 = bor_image2.resize((16, 16), Image.ANTIALIAS)
bor_image2 = ImageTk.PhotoImage(bor_image2)
bor_image3 = Image.open("image3.gif")
bor_image3 = bor_image3.resize((16, 16), Image.ANTIALIAS)
bor_image3 = ImageTk.PhotoImage(bor_image3)
bor_image4 = Image.open("image4.gif")
bor_image4 = bor_image4.resize((16, 16), Image.ANTIALIAS)
bor_image4 = ImageTk.PhotoImage(bor_image4)
bor_image5 = Image.open("image5.gif")
bor_image5 = bor_image5.resize((16, 16), Image.ANTIALIAS)
bor_image5 = ImageTk.PhotoImage(bor_image5)
bor_image6 = Image.open("image6.gif")
bor_image6 = bor_image6.resize((16, 16), Image.ANTIALIAS)
bor_image6 = ImageTk.PhotoImage(bor_image6)

for i in range(len(m)):
    for j in range(len(m[i])):
        if m[i][j]%10 == 1:
            if m[i][j]%100 < 10:
                Label(root,image=image1,bd=0).grid(row=i,column=j,sticky = NW)
            else:
                Label(root, image=bor_image1, bd=2,bg=civ_color(((m[i][j]%100)-(m[i][j]%10))/10)).grid(row=i, column=j, sticky=NW)
        elif m[i][j] % 10 == 2:
            if m[i][j]%100 < 10:
                Label(root,image=image2,bd=0).grid(row=i,column=j,sticky = NW)
            else:
                Label(root, image=bor_image2, bd=2,bg=civ_color(((m[i][j]%100)-(m[i][j]%10))/10)).grid(row=i, column=j, sticky=NW)
        elif m[i][j] % 10 == 3:
            if m[i][j]%100 < 10:
                Label(root,image=image3,bd=0).grid(row=i,column=j,sticky = NW)
            else:
                Label(root, image=bor_image3, bd=2,bg=civ_color(((m[i][j]%100)-(m[i][j]%10))/10)).grid(row=i, column=j, sticky=NW)
        elif m[i][j] % 10 == 4:
            if m[i][j]%100 < 10:
                Label(root,image=image4,bd=0).grid(row=i,column=j,sticky = NW)
            else:
                Label(root, image=bor_image4, bd=2,bg=civ_color(((m[i][j]%100)-(m[i][j]%10))/10)).grid(row=i, column=j, sticky=NW)
        elif m[i][j] % 10 == 5:
            if m[i][j]%100 < 10:
                Label(root,image=image5,bd=0).grid(row=i,column=j,sticky = NW)
            else:
                Label(root, image=bor_image5, bd=2,bg=civ_color(((m[i][j]%100)-(m[i][j]%10))/10)).grid(row=i, column=j, sticky=NW)
        elif m[i][j] % 10 == 6:
            if m[i][j]%100 < 10:
                Label(root,image=image6,bd=0).grid(row=i,column=j,sticky = NW)
            else:
                Label(root, image=bor_image6, bd=2,bg=civ_color(((m[i][j]%100)-(m[i][j]%10))/10)).grid(row=i, column=j, sticky=NW)


root.mainloop()