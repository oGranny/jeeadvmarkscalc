import time
from typing import Tuple
from flask import Flask, render_template, request,jsonify, make_response
from utilities import generate_response, getShiftData
import requests
import json

app = Flask(__name__, static_folder="./static")


def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)


@app.route('/')
def hello_world():
    # make_response("site temporarily down", 404)
    return render_template("index.html")

    
@app.route('/result', methods= ['POST', 'GET'])
def submit():
    try:
        if request.method == 'POST':
            data = (request.form.to_dict())
            link = data['response_link']
            req = (requests.get(link))
            meta = getShiftData(req.text)
            response = generate_response(req.text)
            print(link)
            shift = meta['shift']
            data = data['option']
            with open(f'static/json/{data}_p{shift}.json') as f:
                response, marks = checkAnswers(response, json.load(f))
            return render_template('result.html', response=response, meta=meta, marks=marks)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": str(e)}), 500)
    

def checkAnswers(solution:dict, answers:dict) -> Tuple[dict, int]:
    marks = 0
    paraques = [618074219,618074220,618074218,618074221,618074237,618074235,618074238,618074236,618074253,618074254,618074252,618074255]
    out = solution
    for key in answers:
        if solution[int(key)]["question_type"] != "MSQ":
            for id in answers[key] :
                if solution[int(key)]["option_ids"] == []:
                    out[int(key)]["marks"] = 0
                    marks += 0
                elif int(key) in paraques:
                    if float(id) in [float(i) for i in solution[int(key)]["option_ids"]]:
                        out[int(key)]["marks"] = 3
                        marks += 3
                    else:      
                        out[int(key)]["marks"] = 0
                elif solution[int(key)]["question_type"] == "SA":
                    if int(id) in [int(i) for i in solution[int(key)]["option_ids"]]:
                        out[int(key)]["marks"] = 4
                        marks += 4

                    elif int(id) not in [int(i) for i in solution[int(key)]["option_ids"]]:
                        out[int(key)]["marks"] = 0
                        marks += 0

                elif id in solution[int(key)]["option_ids"] and solution[int(key)]["question_type"] == "MCQ":
                    out[int(key)]["marks"] = 3
                    marks += 3

                elif id not in solution[int(key)]["option_ids"] and solution[int(key)]["question_type"] == "MCQ":
                    out[int(key)]["marks"] = -1
                    marks += -1
        else: 
            a = sorted(solution[int(key)]["option_ids"])
            b = sorted(answers[key])
            negative = False
            for elt in a:
                if elt not in b:
                    negative = True
                    break
            if negative:
                out[int(key)]["marks"] = -2
                marks += -2
            elif not a:
                out[int(key)]["marks"] = 0
                marks += 0
            elif a == b:
                out[int(key)]["marks"] = 4
                marks += 4
            elif (set(a).issubset(set(b))):
                out[int(key)]["marks"] = len(a)
                marks += len(a) 
    return out, marks
            


if __name__ == '__main__':
    app.run()
