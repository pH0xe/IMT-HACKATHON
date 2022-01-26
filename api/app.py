import csv
from os import listdir
from os.path import isfile, join

from flask import Flask, request, make_response, jsonify, send_file

app = Flask(__name__)
HOST = 'localhost'
PORT = 5000

def getMax():
    path = 'data'
    res = None
    dirs = [f for f in listdir(path)]
    for dirName in dirs:
        if res is None:
            res = int(dirName)
        else:
            if int(dirName) > res:
                res = int(dirName)
    return res

def getCsvFixe(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []

    path = 'data/' + str(courseId) + '/fixe'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    res = []
    for file in onlyfiles:
        with open(path + '/' + file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                row.append(file)
                res.append(row)
    return res

def getCsvBMX(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []

    path = 'data/' + str(courseId) + '/bmx'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    res = []
    for file in onlyfiles:
        with open(path + '/' + file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                row.append(file)
                res.append(row)
    return res

def getCalcul(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []

    path = 'data/' + str(courseId) + '/calcul.csv'

    if not isfile(path):
        print('File not exist. Compute it')
        fixe = getCsvFixe(courseId)
        bmx = getCsvBMX(courseId)
        pathCalcul = 'data/' + str(courseId) + '/calcul.csv'
        with open(pathCalcul, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in fixe:
                spamwriter.writerow(row)

    res = []
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            res.append(row)
    return res

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/data', methods=['GET'])
def getData():
    type = request.args.get('type')
    courseId = request.args.get('id')

    if (type is None) or (type == 'json'):
        return getJson(courseId)
    else:
        return getCSV(courseId)

def getJson(id):
    res = getCalcul(id)
    resp = []
    tmp = None
    for item in res:
        if tmp is not None and tmp['name'] != item[3]:
            print("change File")
            resp.append(tmp)
            tmp = None
        if tmp is None:
            tmp = {'name': item[3], 'times': [], 'latlngs': []}
        tmp['times'].append(item[0])
        tmp['latlngs'].append([item[1], item[2]])
    if tmp is not None:
        resp.append(tmp)
    return make_response(jsonify(resp))

def getCSV(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []
    getCalcul(courseId)
    return send_file('data/' + str(courseId) + '/calcul.csv')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
