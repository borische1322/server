import logging
import json

from flask import request, jsonify

from codeitsuisse import app
logger = logging.getLogger(__name__)

def riskCat(x):
    if (x%3 == 0):
        return "L"
    if (x%3 == 1):
        return "M"
    return "S"

def subtotal(xcor, ycor,x ,y, gridmap):
    subtotal_cost = 0
    num_move = 0
    for i in range(xcor, x):
        for j in range(ycor, y):
            if (gridmap[j][i] == "S"):
                subtotal_cost += 1
            elif (gridmap[j][i] == "M"):
                subtotal_cost += 2
            else:
                subtotal_cost += 3
            num_move += 1
    return float(float(subtotal_cost)/float(num_move))



def get_cost(input):
    x = input["targetPoint"]["first"] + 1
    y = input["targetPoint"]["second"] + 1
    gridmap = [[0 for i in range(x)] for j in range(y)]
    gridmapindex = [[0 for i in range(x)] for j in range(y)]
    gridDepth = input["gridDepth"]
    gridKey = input["gridKey"]
    hstepper = input["horizontalStepper"]
    vstepper = input["verticalStepper"]


        
    for i in range(y):
        for j in range(x):
            print(j,"",i)
            if ((i == 0 and j == 0) or (i == y-1 and j == x-1)):
                gridmap[i][j] = riskCat(gridDepth % gridKey)
            elif (j == 0):
                gridmapindex[i][j] = (((i * vstepper) + gridDepth) % gridKey)
                gridmap[i][j] = riskCat(((gridmapindex[i][j]) + gridDepth) % gridKey)
            elif (i == 0):
                gridmapindex[i][j] = (((j * hstepper) + gridDepth) % gridKey)
                gridmap[i][j] = riskCat(((gridmapindex[i][j]) + gridDepth) % gridKey)

            else:
               gridmapindex[i][j] = ((gridmapindex[i][j-1] * gridmapindex[i-1][j]) + gridDepth) % gridKey
               gridmap[i][j] = riskCat(((gridmapindex[i][j]) + gridDepth) % gridKey)
    movement = [0,0]
    target = [x-1, y-1]
    min_cost = 0
    while(movement != target):
        print(movement)
        if (movement[0] == target[0]):
            movement[1] += 1
            
            if (gridmap[movement[1]][movement[0]] == "S"):
                min_cost += 1
            elif (gridmap[movement[1]][movement[0]] == "M"):
                min_cost += 2
            else:
                min_cost += 3
            gridmap[movement[1]][movement[0]] = "\033[1m" + gridmap[movement[1]][movement[0]] + "\033[0m"
            continue
        if (movement[1] == target[1]):
            movement[0] += 1
            
            if (gridmap[movement[1]][movement[0]] == "S"):
                min_cost += 1
            elif (gridmap[movement[1]][movement[0]] == "M"):
                min_cost += 2
            else:
                min_cost += 3
            gridmap[movement[1]][movement[0]] = "\033[1m" + gridmap[movement[1]][movement[0]] + "\033[0m"
            continue
        right = subtotal(movement[0] + 1, movement[1],x ,y,gridmap)
        down = subtotal(movement[0], movement[1] + 1,x ,y,gridmap)
        if (right < down):
            movement[0] += 1
            
            if (gridmap[movement[1]][movement[0]] == "S"):
                min_cost += 1
            elif (gridmap[movement[1]][movement[0]] == "M"):
                min_cost += 2
            else:
                min_cost += 3
            gridmap[movement[1]][movement[0]] = "\033[1m" + gridmap[movement[1]][movement[0]] + "\033[0m"
        else:
            movement[1] += 1
            
            if (gridmap[movement[1]][movement[0]] == "S"):
                min_cost += 1
            elif (gridmap[movement[1]][movement[0]] == "M"):
                min_cost += 2
            else:
                min_cost += 3
            gridmap[movement[1]][movement[0]] = "\033[1m" + gridmap[movement[1]][movement[0]] + "\033[0m"
        print(min_cost)
    return {"gridMap": gridmap, "minimumCost": min_cost}

@app.route('/stock-hunter', methods=['POST'])
def evaluate_stock_hunter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    result = []
    
    l = 0
    for test_cases in data:
        result.append(get_cost(test_cases))
        logging.info("gridMap :{}".format(result[l]["gridMap"]))
        logging.info("minimumCost :{}".format(result[l]["minimumCost"]))
        l += 1
    return json.dumps(result)
