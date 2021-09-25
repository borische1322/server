import logging
import json

from flask import request, jsonify

from codeitsuisse import app

global p1ANS 
global test
p2Ans=0
again1=1
again2=1
test=0

logger = logging.getLogger(__name__)
@app.route('/parasite', methods=['POST'])
def evaluate_parasite():
    global text
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    result = []
   
    for test_case in data:
        result.append(main(test_case["room"],test_case["grid"],test_case["interestedIndividuals"]))
       
    return jsonify(result)
  

def target(inputTarget):
    targry_array=[]
    for i in inputTarget:
        x=i.rsplit(',')
        targry_array.append(x)
    return targry_array
  
def locationParasite(x):
    #x=[[0, 3],[0, 1]]
    parasite=[]
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j]==3:
                parasite.append(i)
                parasite.append(j)
    return parasite
  
def noHealth(inputGrid):
    i=0
    j=0
    while i<len(inputGrid):
        while j<len(inputGrid[i]):
            if inputGrid[i][j]==1:
                return False
            else:
                j+=1
        j=0
        i+=1
    return True
  
def make_stepForP2(m):
    global again1
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 3:
                if i>0 and m[i-1][j] == 1:
                    m[i-1][j] = 3
                    again1+=1
                if j>0 and m[i][j-1] == 1 :
                    m[i][j-1] = 3
                    again1+=1
                if i<len(m)-1 and m[i+1][j] == 1 :
                    m[i+1][j] = 3
                    again1+=1
                if j<len(m[i])-1 and m[i][j+1] == 1 :
                    m[i][j+1] = 3
                    again1+=1
                  
def isolatedForp2(m):
    for i in range(len(m)-1):
        for j in range(len(m[i])-1):
            if m[i][j]==1:
                if i==0 and j==0:
                    if m[i][j+1]==0 and m[i+1][j]==0:
                        return True
                elif i==len(m)-1 and j==0:
                    if m[i][j+1]==0 and m[i-1][j]==0:
                        return True
                elif i==0 and j==len(m[i])-1:
                    if m[i][j-1]==0 and m[i+1][j]==0:
                        return True
                elif i==len(m)-1 and j==len(m[i])-1:
                    return True
                else:
                    if (m[i-1][j] ==0 and i>0) and (m[i][j-1]==0 and j>0) and (m[i+1][j]==0 and i<len(m[1])-1) and (m[i][j+1]==0 and j<len(m[1])-1) :
                        return True
    return False 
  
def p2(grid):
    global p2Ans
    global again1
    if isolatedForp2(grid)==True:
        p2Ans=-1
    else:
        while noHealth(grid)==False and again1>0:
            make_stepForP2(grid)
            p2Ans+=1
            again1-=1
    return p2Ans


def p1(inputGrid, inputTarget):
    global p1_value
    p1 = target(inputTarget)
    #p1_ans[len(p1)]
    p1_ans=[]
    
    parasite = locationParasite(inputGrid)
    x = parasite[0]
    y = parasite[1]
    #print(x)
    #print(y)
    i=0
    while i<len(p1):
        p1_value = 0
        if solve(inputGrid,x,y,int(p1[i][0]),int(p1[i][1])) == True:
            #p1_ans[i] = p1_value
            p1_ans.append(p1_value)
            i+=1
        else:
            p1_ans.append(-1)
            i+=1
    p1_finalAns=dict(zip(inputTarget,p1_ans))
    return p1_finalAns

def solve(m,x,y,p1_x,p1_y):
    global p1_value
    global test
    #print(p1_value)
    #Base case  
    if y > len(m)-1 or x > len(m[0])-1:
        p1_value -= 1
        return False

    if x == p1_x and y == p1_y :
        return True

    if  m[x][y] != 1 and test != 0:
        p1_value -= 1
        return False
    test+=1
    #print("fuck")
    #recursive case
    if solve(m,x,y+1,p1_x,p1_y) == True :  #right
        p1_value += 1
        return True
    if solve(m,x+1,y,p1_x,p1_y) == True :  #down
        p1_value += 1
        return True     
    if solve(m,x,y-1,p1_x,p1_y) == True :  #left
        p1_value += 1
        return True     
    if solve(m,x-1,y,p1_x,p1_y) == True :  #up
        p1_value += 1
        return True     

    #Backtracking
    return False


def p1test(grid,inputTarget):
    global p1ANS
    global again1
    p1target=target()
    p1ANS=[]
    for i in p1target:
        steps=0
        if isolatedForp1(grid,int(i[0]),int(i[1]))==True:
            print(-1)
        else:
            while noHealth()==False and again1>0:
                if grid[int(i[0])][int(i[1])]!=3:
                    make_stepForP2(grid)
                    steps+=1
                    again1-=1
                else:
                    break
        p1ANS.append(steps)
    p1_finalAns=dict(zip(inputTarget,p1ANS))
    return p1_finalAnsdef p1test(grid,inputTarget):
    global p1ANS
    global again1
    p1target=target()
    p1ANS=[]
    for i in p1target:
        steps=0
        if isolatedForp1(grid,int(i[0]),int(i[1]))==True:
            print(-1)
        else:
            while noHealth()==False and again1>0:
                if grid[int(i[0])][int(i[1])]!=3:
                    make_stepForP2(grid)
                    steps+=1
                    again1-=1
                else:
                    break
        p1ANS.append(steps)
    p1_finalAns=dict(zip(inputTarget,p1ANS))
    return p1_finalAns


def isolatedForp1(m,i,j):
    if m[i][j]==1:
        if i==0 and j==0:
            if m[i][j+1]==0 and m[i+1][j]==0:
                return True
        elif i==len(m)-1 and j==0:
            if m[i][j+1]==0 and m[i-1][j]==0:
                return True
        elif i==0 and j==len(m[i])-1:
            if m[i][j-1]==0 and m[i+1][j]==0:
                return True
        elif i==len(m)-1 and j==len(m[i])-1:
            return True
        else:
            if (m[i-1][j] ==0 and i>0) and (m[i][j-1]==0 and j>0) and (m[i+1][j]==0 and i<len(m[1])-1) and (m[i][j+1]==0 and j<len(m[1])-1) :
                return True
    elif m[i][j]==0:
        return True
    else:
        return False 

def make_stepForP1(m):
    global again1
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 3:
                if i>0 and m[i-1][j] == 1:
                    m[i-1][j] = 3
                    again1+=1
                if j>0 and m[i][j-1] == 1 :
                    m[i][j-1] = 3
                    again1+=1
                if i<len(m)-1 and m[i+1][j] == 1 :
                    m[i+1][j] = 3
                    again1+=1
                if j<len(m[i])-1 and m[i][j+1] == 1 :
                    m[i][j+1] = 3
                    again1+=1 
                    
def main(inputRoom,inputGrid,inputTarget):
    p1_ans=p1(inputGrid, inputTarget)
    p2_ans=p2(inputGrid)
    p3_ans=-1
    p4_ans=1
    finalAns={'room':inputRoom,'p1':p1_ans,'p2':p2_ans,'p3':p3_ans,'p4':p4_ans}
    return finalAns 

