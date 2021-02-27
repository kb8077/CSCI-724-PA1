# CSCI-724-PA1

This is a demo application to consume SOAP and RESTful APIs. It was a part of coursework of CSCI-724 Programming Assignment 1.

This application is build using these APIs:

1. (SOAP - WSDL)http://it.bmc.uu.se/andlov/php/uup-soap/example/demo/calculator.php?docs=text
2. (REST)https://opentripmap.io/product
3. (REST)https://opencagedata.com/api
4. (REST)https://www.currencyconverterapi.com/

**Note**: Please do not use the same API keys that are in the code. You can get the API keys from the respective websites given above. **Its free**

## Installation
Create a virtual environment

`python3 -m venv /path/to/new/virtual/environment`

Activate the virtual environment

`source /path/to/new/virtual/environment/bin/activate`

Install the required packages from `requirements.txt`

`pip install -r requirements.txt`

## Running web app in local host
Run the following command to start the local server

`python3 client.py`

Go to your favourite browser and go to the following url
`http://localhost:5000`