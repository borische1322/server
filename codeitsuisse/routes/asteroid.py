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
    temp_score = 0
    temp_position = 0
    max_position = 0
    temp = [[text[0],1]]
    current_char = text[0]
    current_index = 0
    
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
            temp_position += temp[i][1]
            continue
        temp_score += score_multiplicity(temp[i][1])

        j = 1
        while( (i-j) >= 0 and (i+j) < len(temp)):
            if (temp[i-j][0] != temp[i+j][0]):
                break
            else:
                temp_score += score_multiplicity(temp[i-j][1] + temp[i+j][1])
            j += 1
            
        if (temp_score > max_score):
            max_score = temp_score
            max_position = temp_position + 1
        temp_score = 0
        temp_position += temp[i][1]

    return {"input": xdx, "score": max_score,"origin": max_position}
        
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
        logging.info("input :{}".format(test_cases))
        logging.info("score :{}".format(result[l]["score"]))
        logging.info("origin :{}".format(result[l]["origin"]))
        l += 1
    return json.dumps(result)



