import pandas as pd
from zeep import Client
import requests

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/currConvert', methods = ['POST', 'GET'])
def currConvertAPI():
    df = pd.read_csv('codes-all_csv.csv')
    currCodes = df['AlphabeticCode'].to_list()
    currCodes = [x for x in currCodes if type(x) is not float]

    if request.method == 'POST':
        data = request.form
        fromCurr = data['Curr1']
        toCurr = data['Curr2']
        amount = float(data['curr1Amount'])

        resturl = "https://free.currconv.com/api/v7/convert?q="+fromCurr+"_"+toCurr+"&compact=ultra&apiKey=789314263e83aa353fc0"
        response1 = requests.get(resturl)
        data = response1.json()
        currency = data[fromCurr + '_' + toCurr]

        convertedCurr = float(currency)*amount
        return render_template('convertor.html',
                                currList=currCodes, 
                                curr1=fromCurr, 
                                curr2=toCurr, 
                                curr1Amount=amount, 
                                curr2Amount=convertedCurr)
    
    else:
        return render_template('convertor.html', currList=currCodes)


def currConvert(fromCurr, toCurr, amount):
    resturl = "https://free.currconv.com/api/v7/convert?q="+fromCurr+"_"+toCurr+"&compact=ultra&apiKey=789314263e83aa353fc0"
    response1 = requests.get(resturl)
    data = response1.json()
    currency = data[fromCurr + '_' + toCurr]

    convertedCurr = float(currency)*amount
    return convertedCurr

@app.route('/currCalculate', methods = ['POST', 'GET'])
def calculator():
    df = pd.read_csv('codes-all_csv.csv')
    currCodes = df['AlphabeticCode'].to_list()
    currCodes = [x for x in currCodes if type(x) is not float]

    if request.method == 'POST':
        
        data = request.form
        op1Curr = data['Curr1']
        op2Curr = data['Curr2']
        outCurr = data['OutCurr']
        op1Amount = float(data['curr1Amount'])
        op2Amount = float(data['curr2Amount'])
        optr = data['operator']

        if optr == '+':
            result = calculator_add(op1Curr, op1Amount, op2Curr, op2Amount, outCurr)
        elif optr == '-':
            result = calculator_substract(op1Curr, op1Amount, op2Curr, op2Amount, outCurr)
        elif optr == '*':
            result = calculator_multiply(op1Curr, op1Amount, op2Curr, op2Amount, outCurr)
        elif optr == '/':
            result = calculator_divide(op1Curr, op1Amount, op2Curr, op2Amount, outCurr)

        return render_template('calculator.html',
                                currList=currCodes, 
                                curr1=op1Curr, 
                                curr2=op2Curr, 
                                curr1Amount=op1Amount, 
                                curr2Amount=op2Amount,
                                outCurr=outCurr,
                                outAmount=result)

    else:
        return render_template('calculator.html', currList=currCodes)

def calculator_add(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.add(op1Amount,curr2)
    return currConvert(op1Curr, outCurr, outAmount)

def calculator_substract(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.substract(op1Amount,curr2)
    return currConvert(op1Curr, outCurr, outAmount)

def calculator_multiply(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.multiply(op1Amount,curr2)
    return currConvert(op1Curr, outCurr, outAmount)

def calculator_divide(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.divide(op1Amount,curr2)
    return currConvert(op1Curr, outCurr, outAmount)

def getCityLatLong(searchQuery):
    resturl = "https://api.opencagedata.com/geocode/v1/json?key=9469c4d644aa4bc28a8b73ed9942b442&q="+searchQuery+"&pretty=1&no_annotations=1"
    response = requests.get(resturl)
    data = response.json()
    maxLat = str(data["results"][0]["bounds"]["northeast"]["lat"]) 
    minLat = str(data["results"][0]["bounds"]["southwest"]["lat"])
    maxLng = str(data["results"][0]["bounds"]["northeast"]["lng"])
    minLng = str(data["results"][0]["bounds"]["southwest"]["lng"])
    return minLat, maxLat, minLng, maxLng

def getPlaces(minLat, maxLat, minLng, maxLng):
    API_key = "5ae2e3f221c38a28845f05b6d8894a067715a340bfd45a8efc4bd9b1"
    resturl = "https://api.opentripmap.com/0.1/en/places/bbox?lon_min="+minLng+"&lon_max="+maxLng+"&lat_min="+minLat+"&lat_max="+maxLat+"&rate=3h&limit=10&format=json&apikey=" + API_key
    response = requests.get(resturl)
    data = response.json()
    return [x["name"] for x in data]

if __name__ == "__main__":
    app.run(debug = False)