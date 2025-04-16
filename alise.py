from flask import Flask, request, jsonify
import logging
import random


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

cities = {
    'москва': ['937455/e855d632b8278de4b6ff',
               '937455/88c4a22f1898ca6f18e7'],
    'нью-йорк': ['937455/2e149ef6f8e56ea55a84',
                 '937455/3c1a9c20030ebad86bdb'],
    'париж': ["965417/8ce4a981de03ba40153a",
              '937455/26b1f9bd6a8e52c58451']
}


sessionStorage = {}


@app.route("/post", methods=["POST"])
def main():
    logging.info(f"Request: {request.json!r}")
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req["session"]["user_id"]

    if req["session"]["new"]:
        res["response"]["text"] = "Привет! Назови свое имя!"

        sessionStorage[user_id] = {
            "first_name": None
        }
        return

    if sessionStorage[user_id]["first_name"] is None:
        first_name = get_first_name(req)

        if first_name is None:
            res["response"]["text"] = "Не расслышала имя, повтори пожалуйста!"

        else:
            sessionStorage[user_id]["first_name"] = first_name
            res['response']['text'] = (
                f'Приятно познакомиться, {first_name.title()}. Я - Алиса. Какой город хочешь увидеть?'
            )
            res["response"]["buttons"] = [
                {
                    "title": city.title(),
                    "hide": True
                } for city in cities
            ]
    else:
        city = get_city(req)
        
        if city in cities:
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = 'Этот город я знаю.'
            res['response']['card']['image_id'] = random.choice(cities[city])
            res['response']['text'] = 'Я угадал!'
        else:
            res['response']['text'] = 'Первый раз слышу об этом городе. Попробуй еще разок!'

            
def get_city(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.GEO":
            return entity["value"].get("city", None)
        
def get_first_name(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.FIO":
            return entity["value"].get("first_name", None)
        
app.run()