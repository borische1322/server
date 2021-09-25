import logging
import json

from flask import request, jsonify

from codeitsuisse import app

text = ""
logger = logging.getLogger(__name__)





def Convert(string):
    list1=[]
    list1[:0]=string
    print(len(list1))
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
    logging.info("input :{}".format(temp))
    for i in range(3):
        if (origin_position -(i+1) <0 or origin_position +(i+1)>=len(temp)):
            break
        if (temp[origin_position -(i+1)][0] == temp[origin_position +(i+1)][0]):
            score += score_multiplicity(temp[origin_position -(i+1)][1] + temp[origin_position +(i+1)][1])
        else:
            break
    return score


def find_origin(xdx):
    print("hi2")
    max_score = 0
    origin_position = 0
    print(text)
    print(len(text))
    for i in range(len(text)):
        print("HIIIII")
        text.insert(i, '0')
        if (max_score < simplify_score()):
            max_score = simplify_score()
            origin_position = i
        logging.info("input :{}".format(max_score))
        text.remove('0')
    return {"input": xdx, "Score": max_score,"origin": origin_position}
        
@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    result = []
    text = Convert(data)
    print("hi")
    print(len(text))
    print(text)
    result.append(find_origin(data))
    print("hi1")
    logging.info("input :{}".format(data))
    logging.info("score :{}".format(result[0]["Score"]))
    logging.info("origin :{}".format(result[0]["origin"]))
    return json.dumps(result)



