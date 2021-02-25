import pandas as pd
from zeep import Client
import requests

# df = pd.read_csv('codes-all_csv.csv')
# currCodes = df['AlphabeticCode'].to_list()
# currCodes = [x for x in currCodes if type(x) is not float]

def currConvert(fromCurr, toCurr, amount):
    resturl = "https://free.currconv.com/api/v7/convert?q="+fromCurr+"_"+toCurr+"&compact=ultra&apiKey=789314263e83aa353fc0"
    response1 = requests.get(resturl)
    data = response1.json()
    currency = data['USD_PHP']
    return currency*amount

def calculator_add(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.add(op1Amount,currency)
    return currConvert(op1Curr, outCurr, outAmount)

def calculator_substract(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.substract(op1Amount,currency)
    return currConvert(op1Curr, outCurr, outAmount)

def calculator_multiply(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.multiply(op1Amount,currency)
    return currConvert(op1Curr, outCurr, outAmount)

def calculator_divide(op1Curr, op1Amount, op2Curr, op2Amount, outCurr):
    wsdl = "calc.wsdl"
    client = Client(wsdl)
    curr2 = currConvert(op2Curr, op1Curr, op2Amount)
    outAmount = client.service.divide(op1Amount,currency)
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

data = getPlaces(*getCityLatLong('new york city,ny,us'))
print([x["name"] for x in data])