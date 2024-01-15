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
import math
import xmltodict
from pymongo.server_api import ServerApi

def deleteStock(CoID):
    # client = MongoClient('localhost', 27017)
    # client = MongoClient("mongodb://localhost:27017/")
    uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    # db = client.test_database
    db = client['SRIM'] # test-db라는 이름의 데이터베이스에 접속
    main = db.main

    main.delete_one({'CoID' : CoID})



def deleteStock(CoID, baseDate):
    # client = MongoClient('localhost', 27017)
    # client = MongoClient("mongodb://localhost:27017/")
    uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    # db = client.test_database
    db = client['SRIM'] # test-db라는 이름의 데이터베이스에 접속
    main = db.main

    main.delete_one({'CoID' : CoID, 'baseDate':baseDate})

def insertStock(baseDate, itmsNm, DCRate, PER, currentPrice, currentPriceURL, ROE, EBITDARate, dividendRate, annualRateOfReturn, annualRateOfReturnPER, cashEquivalents, cashEquivalentsShare, equity, excessEarnings, shareOutstanding, totalValue, valuePerShare, valuePerShareCash, EBITDARateURL ,PERURL, ROEURL, cashEquivalentsURL, dividendRateURL, equityURL, shareOutstandingURL):
    # client = MongoClient('localhost', 27017)
    # client = MongoClient("mongodb://localhost:27017/")
    uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    # db = client.test_database
    db = client['SRIM']  # test-db라는 이름의 데이터베이스에 접속
    main = db.main

    main.insert_one({
        "baseDate": baseDate,
        "CoID": itmsNm,
        "DCRate": DCRate,
        "PER": PER,
        "currentPrice": currentPrice,
        "currentPriceURL" : currentPriceURL,
        "ROE": ROE,
        "EBITDARate": EBITDARate,
        "dividendRate": dividendRate,
        "annualRateOfReturn": annualRateOfReturn,
        "annualRateOfReturnPER": annualRateOfReturnPER,
        "cashEquivalents": cashEquivalents,
        "cashEquivalentsShare": cashEquivalentsShare,
        "equity": equity,
        "excessEarnings": excessEarnings,
        "shareOutstanding": shareOutstanding,
        "totalValue": totalValue,
        "valuePerShare": valuePerShare,
        "valuePerShareCash": valuePerShareCash,
        "EBITDARateURL": EBITDARateURL,
        "PERURL": PERURL,
        "ROEURL" : ROEURL,
        "cashEquivalentsURL": cashEquivalentsURL,
        "dividendRateURL" : dividendRateURL,
        "equityURL": equityURL,
        "shareOutstandingURL": shareOutstandingURL
    })

def updateStock(baseDate, itmsNm, DCRate, PER, currentPrice, currentPriceURL, ROE, EBITDARate, dividendRate, annualRateOfReturn, annualRateOfReturnPER, cashEquivalents, cashEquivalentsShare, equity, excessEarnings, shareOutstanding, totalValue, valuePerShare, valuePerShareCash, EBITDARateURL ,PERURL, ROEURL, cashEquivalentsURL, dividendRateURL, equityURL, shareOutstandingURL):
    # client = MongoClient('localhost', 27017)
    # client = MongoClient("mongodb://localhost:27017/")
    uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    # db = client.test_database
    db = client['SRIM']  # test-db라는 이름의 데이터베이스에 접속
    main = db.main

    main.update_one({"baseDate":baseDate, "CoID":itmsNm},{"$set" : {
        "baseDate": baseDate,
        "CoID": itmsNm,
        "DCRate": DCRate,
        "PER": PER,
        "currentPrice": currentPrice,
        "currentPriceURL" : currentPriceURL,
        "ROE": ROE,
        "EBITDARate": EBITDARate,
        "dividendRate": dividendRate,
        "annualRateOfReturn": annualRateOfReturn,
        "annualRateOfReturnPER": annualRateOfReturnPER,
        "cashEquivalents": cashEquivalents,
        "cashEquivalentsShare": cashEquivalentsShare,
        "equity": equity,
        "excessEarnings": excessEarnings,
        "shareOutstanding": shareOutstanding,
        "totalValue": totalValue,
        "valuePerShare": valuePerShare,
        "valuePerShareCash": valuePerShareCash,
        "EBITDARateURL": EBITDARateURL,
        "PERURL": PERURL,
        "ROEURL": ROEURL,
        "cashEquivalentsURL": cashEquivalentsURL,
        "dividendRateURL": dividendRateURL,
        "equityURL": equityURL,
        "shareOutstandingURL": shareOutstandingURL
    }})

def findStock(itmsNm, baseDate):
    # client = MongoClient('localhost', 27017)
    # client = MongoClient("mongodb://localhost:27017/")
    uri = "mongodb+srv://btsy7331:dmadkr753!@cluster0.dw6olvv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))


    # db = client.test_database
    db = client['SRIM']  # test-db라는 이름의 데이터베이스에 접속
    main = db.main

    data = main.find({
        'CoID': itmsNm,
        'baseDate': baseDate
        })

    return bool(list(data))

#
# if findStock('삼성전자', '2023/03') is False:
#     print("Fasle")
# else:
#     print("True")
#
# print(findStock('LG전자', '2023/03'))

