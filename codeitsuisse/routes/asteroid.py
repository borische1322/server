import logging
import json

from flask import request, jsonify

from codeitsuisse import app

text = ""
logger = logging.getLogger(__name__)





def Convert(string):
    list1=[]
    list1[:0]=string
    return list1


def score_multiplicity(x):
    if (x >= 10):
        return x*2
    if (x >= 7):
        return int(x * 1.5)
    return x

def simplify_score(xdx):
    global text
    max_score = 0
    score = 0
    temp = [[text[0],1]]
    current_char = text[0]
    current_index = 0
    origin_position = 0
    max_origin = 0
    for i in range(len(text)):
        if (i == 0):
            continue
        if (text[i] == current_char):
            temp[current_index][1] = temp[current_index][1] + 1
        else:
            current_char = text[i]
            current_index = current_index + 1
            temp.append([current_char,1])
    for i in range(len(temp)):

        if (temp[i][1] < 3):
            origin_position += temp[i][1]
            continue
        score += score_multiplicity(temp[i][1])
        
        for j in range(i):
            if (i-(j+1) <0 or i+(j+1) >= len(temp)):
                break
            if (temp[i-(j+1)][0] == temp[i+(j+1)][0]):
                score += score_multiplicity(temp[i-(j+1)][1] + temp[i+(j+1)][1])

        if (score > max_score):
            max_score = score
            max_origin = origin_position
            max_origin += 1
        score = 0
        origin_position += temp[i][1]
    return {"input": xdx, "score": max_score,"origin": max_origin}
        
@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    global text
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    result = []
    
    l = 0
    for test_cases in data['test_cases']:
        text = Convert(str(test_cases))
        result.append(simplify_score(test_cases))
        ##logging.info("input :{}".format(test_cases))
        logging.info("score :{}".format(result[l]["score"]))
        logging.info("origin :{}".format(result[l]["origin"]))
        l += 1
    return json.dumps(result)



