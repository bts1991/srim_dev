import os
import json
import re
from flask import Flask, render_template, request, redirect, jsonify
from bson import json_util
from bson.json_util import dumps
# from flask_pymongo import PyMongo
from flask import Flask, render_template, request, redirect
from flask.json import jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
# import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from urllib.parse import urlencode, unquote
import requests
# import pandas as pd
import math
import xmltodict
import numpy
from findStock import FindStock
from request import RequestStock
from StockMange import deleteStock
from pymongo.server_api import ServerApi

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
# client = MongoClient("mongodb://localhost:27017/")
uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

# db = client.test_database
db = client['SRIM'] # test-db라는 이름의 데이터베이스에 접속
main = db.main


data = main.find()
# print(type(data))

data_list = list(data)
# print(type(data_list))
# print(data_list)
# print(len(data_list))

dump = dumps(data_list)
# print(type(dump))

def formatChange(x):
    x = float(x)
    rounding = round(x,2)
    formatting = format(rounding, ',')
    string = str(formatting)
    return string

@app.route('/write', methods=["POST"])
def write():
    CoNm = request.form.get('CoNm')
    RequestStock(CoNm)

    return redirect('/')

@app.route("/delete", methods=["POST"])
def list_delete():
    CoID = request.form['CoID']
    baseDate = request.form['baseDate']
    deleteStock(CoID, baseDate)

    return jsonify({'msg': '삭제 완료!'})


@app.route('/')
def get():
    res = requests.get("https://comp.fnguide.com/XML/Market/CompanyList.txt")
    res.encoding = 'UTF-8'
    companylist = res.text

    print(companylist)

    f = open('.\static\companylist.txt', 'w', encoding='UTF-8')
    f.write(companylist)
    f.close()

    uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    # client = MongoClient("mongodb://localhost:27017/")
    db = client['SRIM']
    main = db.main
    data = main.find()

    data_list = list(data)

    result_list = []

    for i in range(len(data_list)):

        # for k in range(len(data_list)):
        data_dic = data_list[i]
        baseDate = data_dic['baseDate']
        CoID = data_dic['CoID']
        DCRate = formatChange(data_dic['DCRate']) + "%"
        PER = data_dic['PER']
        currentPrice = formatChange(data_dic['currentPrice'])
        currentPriceURL = data_dic['currentPriceURL']
        ROE = data_dic['ROE']
        EBITDARate = formatChange(data_dic['EBITDARate']) + "%"
        dividendRate = formatChange(data_dic['dividendRate']) + "%"
        annualRateOfReturn = formatChange(data_dic['annualRateOfReturn']) + "%"
        annualRateOfReturnPER = formatChange(data_dic['annualRateOfReturnPER'])
        cashEquivalents = formatChange(data_dic['cashEquivalents'])
        cashEquivalentsShare = formatChange(data_dic['cashEquivalentsShare'])
        equity = formatChange(data_dic['equity'])
        excessEarnings = formatChange(data_dic['excessEarnings'])
        shareOutstanding = formatChange(data_dic['shareOutstanding'])
        totalValue = formatChange(data_dic['totalValue'])
        valuePerShare = formatChange(data_dic['valuePerShare'])
        valuePerShareCash = formatChange(data_dic['valuePerShareCash'])
        EBITDARateURL = data_dic['EBITDARateURL']
        PERURL = data_dic['PERURL']
        ROEURL = data_dic['ROEURL']
        cashEquivalentsURL = data_dic['cashEquivalentsURL']
        dividendRateURL = data_dic['dividendRateURL']
        equityURL = data_dic['equityURL']
        shareOutstandingURL = data_dic['shareOutstandingURL']


        result = {}
        result['baseDate'] = baseDate
        result['CoID'] = CoID
        result['DCRate'] = DCRate
        result['PER'] = PER
        result['currentPrice'] = currentPrice
        result['currentPriceURL'] = currentPriceURL
        result['ROE'] = ROE
        result['EBITDARate'] = EBITDARate
        result['dividendRate'] = dividendRate
        result['annualRateOfReturn'] = annualRateOfReturn
        result['annualRateOfReturnPER'] = annualRateOfReturnPER
        result['cashEquivalents'] = cashEquivalents
        result['cashEquivalentsShare'] = cashEquivalentsShare
        result['equity'] = equity
        result['excessEarnings'] = excessEarnings
        result['shareOutstanding'] = shareOutstanding
        result['totalValue'] = totalValue
        result['valuePerShare'] = valuePerShare
        result['valuePerShareCash'] = valuePerShareCash
        result['EBITDARateURL'] = EBITDARateURL
        result['PERURL'] = PERURL
        result['ROEURL'] = ROEURL
        result['cashEquivalentsURL'] = cashEquivalentsURL
        result['dividendRateURL'] = dividendRateURL
        result['equityURL'] = equityURL
        result['shareOutstandingURL'] = shareOutstandingURL

        print(result)

        result_list.append(result)
        print(result_list)

    return render_template('index.html', result_list=result_list)





# @app.route('/get', methods=["GET"])
# def get2():
#     result = dumps(list(main.find()))
#     return result
        # jsonify({
        # "CoID": result.get('CoID'),
        # "DCRate": result.get('DCRate'),
        # "PER": result.get('PER'),
        # "currentPrice": result.get('currentPrice'),
        # "ROE": result.get('ROE'),
        # "annualRateOfReturn": result.get('annualRateOfReturn'),
        # "annualRateOfReturnPER": result.get('annualRateOfReturnPER'),
        # "cashEquivalents": result.get('cashEquivalents'),
        # "cashEquivalentsShare": result.get('cashEquivalentsShare'),
        # "equity": result.get('equity'),
        # "excessEarnings": result.get('excessEarnings'),
        # "shareOutstanding": result.get('shareOutstanding'),
        # "totalValue": result.get('totalValue'),
        # "valuePerShare": result.get('valuePerShare'),
        # "valuePerShareCash": result.get('valuePerShareCash')
    # })


if __name__ == '__main__':
    app.run(host="127.0.0.1", port='80')
