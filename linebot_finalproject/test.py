import datetime
import threading
from flask import Flask, request, abort, make_response
app = Flask(__name__)

@app.route("/check")
def hello():
    return "checked"


# http://127.0.0.1:5000/set?name=dog_name&time=1/3/12:20-13:20
@app.route("/set", methods=['GET'])
def getname():
    name = request.args.get('name')
    time = request.args.get('time')
    print(name, time)
    alert_door1_door2(time)
    return "set_finished"


def alert_door1_door2(set_time):
    date_list = set_time.split('/')
    time_list = date_list[2].split('-')
    now_time = datetime.datetime.now()
    next_year = now_time.year
    next_month = date_list[0]
    next_day = date_list[1]
    time1 = time_list[0] + ':00'
    time2 = time_list[1] + ':00'
    next_time1 = datetime.datetime.strptime(str(next_year) + '-' + str(next_month) + '-' + str(next_day) + ' ' + str(time1), "%Y-%m-%d %H:%M:%S")
    next_time2 = datetime.datetime.strptime(str(next_year) + '-' + str(next_month) + '-' + str(next_day) + ' ' + str(time2), "%Y-%m-%d %H:%M:%S")
    door1_time = (next_time1 - now_time).total_seconds()
    print(door1_time)
    door2_time = (next_time2 - now_time).total_seconds()

    timer = threading.Timer(door1_time, hello)
    timer.start()

def hello():
    print("hello")


if __name__ == '__main__':
    app.run(host='0.0.0.0')