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
# import numpy as np
import xmltodict
from findStock import FindStock
import time
from datetime import datetime
from StockMange import insertStock, updateStock, findStock


def request(StockNo, mrktCtg):
    url1 = "https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=" + StockNo + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701"
    res1 = requests.get(url1)
    soup1 = BeautifulSoup(res1.text, "html.parser")

    url2 = "https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=" + StockNo + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701"
    res2 = requests.get(url2)
    soup2 = BeautifulSoup(res2.text, "html.parser")

    url3 = "https://www.kisrating.com/ratingsStatistics/statics_spread.do"
    res3 = requests.get(url3)
    soup3 = BeautifulSoup(res3.text, "html.parser")

    url4 = "https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=" + StockNo + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN="
    res4 = requests.get(url4)
    soup4 = BeautifulSoup(res4.text, "html.parser")

    url5 = "https://comp.fnguide.com/SVO2/ASP/SVD_shareanalysis.asp?pGB=1&gicode=" + StockNo + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=109&stkGb=701"
    res5 = requests.get(url5)
    soup5 = BeautifulSoup(res5.text, "html.parser")

    url6 = "https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=" + StockNo + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
    res6 = requests.get(url6)
    soup6 = BeautifulSoup(res6.text, "html.parser")

    url7 = "https://www.google.com/finance/quote/" + StockNo[1:] + ":" + mrktCtg
    res7 = requests.get(url7)
    soup7 = BeautifulSoup(res7.text, "html.parser")

    return [soup1, url1, soup2, url2, soup3, url3, soup4, url4, soup5, url5, soup6, url6, soup7, url7]


def RequestStock(CoNm) :
        data = FindStock(CoNm)
        StockNo = data[0]['srtnCd']
        itmsNm = data[0]['itmsNm']

        if data[0]['mrktCtg'] == 'KOSPI':
            mrktCtg = 'KRX'
        else :
            mrktCtg = 'KOSDAQ'

        requestResult = request(StockNo, mrktCtg)

        ## 기준일자 구하기 - 성공
        soup1 = requestResult[0]
        url1 = requestResult[1]

        baseDate = (soup1.select_one('#compBody > div.section.ul_de > div:nth-child(3) > div.um_table > table > thead > tr > th.cle').text)
        print(baseDate)


        ## 자기자본 구하기 - 성공
        soup2 = requestResult[2]
        url2 = requestResult[3]
        equityURL = url2

        if soup2.select_one('#p_grid2_10 > td.r.cle') is None :
            ts2 = soup2.select_one('#divDaechaY > table > tbody > tr:nth-child(45) > td.r.cle').text
            # if oup2.select_one('#divDaechaY > table > tbody > tr:nth-child(45) > td.r.cle') is None
            #
        else:
           ts2 = soup2.select_one('#p_grid2_10 > td.r.cle').text

        print("equity는???")
        print(ts2)
        ts21 = ts2.replace(",","")


        try:
            equity = int(ts21)*100000000
        except:
            ts22 = soup2.select_one('#divDaechaY > table > tbody > tr:nth-child(58) > td.r.cle').text
            ts23 = ts22.replace(",", "")
            equity = int(ts23) * 100000000

        print(equity)
        print(type(equity))

        ## ROE 구하기 - 성공
        soup1 = requestResult[0]
        url1 = requestResult[1]
        ROEURL = url1

        if soup1.select_one('#p_grid1_18 > td.r.cle') is None:
            ts3 = soup1.select_one('#p_grid1_13 > td.r.cle').text
        else:
            ts3 = soup1.select_one('#p_grid1_18 > td.r.cle').text
        print(ts3)
        ts31 = float(ts3)
        ROE = "%0.1f%%"%ts31
        print(ROE)
        print(type(ROE))

        ## 할인율(BBB- 회사채 5년 수익률) 구하기
        soup3 = requestResult[4]
        url3 = requestResult[5]
        ts4 = soup3.select_one('#con_tab1 > div.table_ty1 > table > tbody > tr:nth-child(11) > td:nth-child(9)').text
        DCRate = float(ts4)
        print(DCRate)
        print(type(DCRate))

        ## 기업가치 구하기
        ## 기업가치 = 자기자본 + 초과이익/할인율
        ## 초과이익 = 자기자본 * (ROE - 할인율)
        excessEarnings = equity*(ts31-DCRate)
        totalValue = equity+excessEarnings/DCRate
        print(totalValue)
        print(type(totalValue))


        ## 발행주식수 구하기 - 성공
        soup4 = requestResult[6]
        url4 = requestResult[7]
        shareOutstandingURL = url4
        ts51 = (((soup4.select_one('#svdMainGrid1 > table > tbody > tr:nth-child(6)')).find("td", class_="r").text).split(sep='/', maxsplit=1))[0].replace(",","")
        shareOutstanding = int(ts51)
        print(shareOutstanding)
        print(type(shareOutstanding))

        ## 자기주식 구하기 - 성공
        soup5 = requestResult[8]
        url5 = requestResult[9]
        ts61 = (soup5.select_one('#dataTable > tbody > tr:nth-child(5) > td:nth-child(3)').text).replace(",","")

        try:
            ts62 = int(ts61)
            print(ts62)
            print(type(ts62))
        except:
            ts62 = 0

        ## 주당 가치 구하기 - 성공
        valuePerShare = totalValue/(shareOutstanding-ts62)
        print(valuePerShare)

        ## 현금 현금성자산 구하기 - 성공
        soup2 = requestResult[2]
        url2 = requestResult[3]
        cashEquivalentsURL = url2
        ts71 = (soup2.select_one('#divDaechaY > table > tbody > tr:nth-child(12) > td.r.cle').text).replace(",","")
        cashEquivalents = int(ts71)*100000000
        cashEquivalentsShare = cashEquivalents/(shareOutstanding-ts62)
        print(cashEquivalentsShare)

        ## 주당 (가치 + 현금성자산) 구하기 - 성공
        valuePerShareCash = valuePerShare + cashEquivalentsShare
        print(valuePerShareCash)

        ## PER 구하기 - 성공
        soup6 = requestResult[10]
        url6 = requestResult[11]
        PERURL = url6
        ts81 = (soup6.select_one('#corp_group2 > dl:nth-child(1) > dd').text)
        if ts81 == '-':
                PER = 0
        else :
                PER = float(ts81)
        print(PER)

        ## 연간이익률 구하기 = EBITDA증가율 + 배당수익률 - 성공
        soup1 = requestResult[0]
        url1 = requestResult[1]
        EBITDARateURL = url1
        try:
            ts91 = (soup1.select_one('#p_grid1_11 > td.r.cle > span').text)
        except:
            ts91 = (soup1.select_one('#p_grid1_11 > td.r.cle').text)

        print("EBITDA는?")
        print(ts91)
        print(type(ts91))
        # print(float(ts91))
        # print(type(float(ts91)))

        try:
            ts92 = float(ts91)

            if type(ts92) == str:
                EBITDARate = 0
            else:
                EBITDARate = float(ts92)  ## EBITDA증가율

        except:
            EBITDARate = 0

        print(EBITDARate)

        soup6 = requestResult[10]
        url6 = requestResult[11]
        dividendRateURL = url6
        ts101 = ((soup6.select_one('#corp_group2 > dl:nth-child(5) > dd').text).split(sep='%', maxsplit=1))[0]
        if ts101 == '-':
              dividendRate = 0
        else :
           dividendRate = float(ts101) ## 배당수익률

        print(dividendRate)

        annualRateOfReturn = EBITDARate+dividendRate
        print(annualRateOfReturn)

        ## 연간이익률/PER 구하기 - 성공 (성장하는 기업지만 저평가 되어 있음)
        if PER == 0:
                annualRateOfReturnPER = 0
        else:
                annualRateOfReturnPER = annualRateOfReturn/PER
        print(annualRateOfReturnPER)

        ## 현재 주가 구하기 - 성공
        soup7 = requestResult[12]
        url7 = requestResult[13]
        # print("=============================================")
        # print(soup7.find_all("div", class_="rPF6Lc"))
        ts111 = (soup7.find("div", class_="YMlKec fxKbKc").text[1:]).replace(",","")
        currentPrice = float(ts111)
        print(currentPrice)
        currentPriceURL = url7

        ## 데이터 존재여부 판별
        if findStock(itmsNm, baseDate) is False:

            print("인서트")
            print(findStock(itmsNm, baseDate))

            insertStock(baseDate, itmsNm, DCRate, PER, currentPrice, currentPriceURL, ROE, EBITDARate, dividendRate, annualRateOfReturn, annualRateOfReturnPER, cashEquivalents, cashEquivalentsShare, equity, excessEarnings, shareOutstanding, totalValue, valuePerShare, valuePerShareCash, EBITDARateURL ,PERURL, ROEURL, cashEquivalentsURL, dividendRateURL, equityURL, shareOutstandingURL)

        else:

            print("업데이트")
            print(findStock(itmsNm, baseDate))

            updateStock(baseDate, itmsNm, DCRate, PER, currentPrice, currentPriceURL, ROE, EBITDARate, dividendRate, annualRateOfReturn, annualRateOfReturnPER, cashEquivalents, cashEquivalentsShare, equity, excessEarnings, shareOutstanding, totalValue, valuePerShare, valuePerShareCash, EBITDARateURL ,PERURL, ROEURL, cashEquivalentsURL, dividendRateURL, equityURL, shareOutstandingURL)


