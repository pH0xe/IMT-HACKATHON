from cmath import log
import csv
from os import listdir
from os.path import isfile, join
import numpy as np

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
    timeMin = None
    for file in onlyfiles:
        with open(path + '/' + file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            row1 = next(spamreader)
            name = file.split(".")[0].split("-")[1]
            row1.append(name)
            res.append(row1)
            if timeMin is None or int(row1[0]) > int(timeMin):
                timeMin = row1[0]

            for row in spamreader:
                row.append(name)
                res.append(row)
    result = [a for a in res if int(a[0]) >= int(timeMin)]
    # [a for a in res if a[0] >= timeMin]
    return removeDuplicate(result)

def getCsvBMX(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []

    path = 'data/' + str(courseId) + '/bmx'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    res = []
    timeMin = None
    for file in onlyfiles:
        with open(path + '/' + file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

            row1 = next(spamreader)
            name = file.split(".")[0].split("-")[1]
            row1.append(name)
            res.append(row1)
            if timeMin is None or row1[0] > timeMin:
                timeMin = row1[0]

            for row in spamreader:
                row.append(name)
                res.append(row)

    result = [a for a in res if a[0] >= timeMin]
    return removeDuplicate(result)

def removeDuplicate(li):
    seen = []
    res = []
    for item in li:
        current = str(item[1]) + ', ' + str(item[2])
        if current not in seen:
            seen.append(current)
            res.append(item)
    return res


def getCalcul(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []

    path = 'data/' + str(courseId) + '/calcul.csv'

    if True or not isfile(path):
        print('File not exist. Compute it')
        fixe = getCsvFixe(courseId)
        # bmx = getCsvBMX(courseId)
        pathCalcul = 'data/' + str(courseId) + '/calcul.csv'
        with open(pathCalcul, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in fixe:
                if int(row[0]) < 5000:
                    row[0] = int(row[0])*1000 + 1643204079878
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

@app.route('/count', methods=['GET'])
def getCount():
    path = 'data'
    l = [f for f in listdir(path)]
    response = jsonify(l)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def getJson(id):
    res = getCalcul(id)
    resp = []
    tmp = None
    for item in res:
        if tmp is not None and tmp['name'] != item[3]:
            resp.append(tmp)
            tmp = None
        if tmp is None:
            tmp = {'name': item[3], 'times': [], 'latlngs': []}
        tmp['times'].append(item[0])
        tmp['latlngs'].append([item[1], item[2]])
    if tmp is not None:
        resp.append(tmp)
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def getCSV(courseId):
    if courseId is None:
        courseId = getMax()
        if courseId is None:
            return []
    getCalcul(courseId)
    response = send_file('data/' + str(courseId) + '/calcul.csv')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
