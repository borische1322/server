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

def simplify_score():
    score = 0
    temp = [[text[0],1]]
    current_char = text[0]
    current_index = 0
    origin_position = 0
    for i in range(len(text)):
        if (i == 0):
            continue
        if (text[i] == current_char):
            temp[current_index][1] = temp[current_index][1] + 1
        else:
            current_char = text[i]
            current_index = current_index + 1
            temp.append([current_char,1])
        if (text[i] == '0'):
            origin_position = current_index

    for i in range(3):
        if (origin_position -(i+1) <0 or origin_position +(i+1)>=len(temp)):
            break
        if (temp[origin_position -(i+1)][0] == temp[origin_position +(i+1)][0]):
            score += score_multiplicity(temp[origin_position -(i+1)][1] + temp[origin_position +(i+1)][1])
        else:
            break
    return score


def find_origin():
    max_score = 0
    origin_position = 0
    for i in range(len(text)):
        text.insert(i, '0')
        if (max_score < simplify_score()):
            max_score = simplify_score()
            origin_position = i
        text.remove('0')
    return {"input": text, "Score": max_score,"origin": origin_position}
        
@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    result = []
    for test_case in data:
        text = Convert(test_case)
        result.append(find_origin(test_case))
    
    logging.info("input :{}".format(inputValue))
    logging.info("score :{}".format(max_score))
    logging.info("origin :{}".format(origin_position))
    return json.dumps(result)



