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

def RequestStock(CoNm) :
        data = FindStock(CoNm)
        StockNo = data[0]['srtnCd']
        itmsNm = data[0]['itmsNm']

        if data[0]['mrktCtg'] == 'KOSPI':
            mrktCtg = 'KRX'
        else :
            mrktCtg = 'KOSDAQ'

        ## 기준일자 구하기 - 성공
        url1 = "https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701"
        res1 = requests.get(url1)
        soup1 = BeautifulSoup(res1.text, "html.parser")
        baseDate = (soup1.select_one('#compBody > div.section.ul_de > div:nth-child(3) > div.um_table > table > thead > tr > th.cle').text)
        print(baseDate)

        ## 자기자본 구하기 - 성공
        res2 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701")
        soup2 = BeautifulSoup(res2.text, "html.parser")
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
        res3 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701")
        soup3 = BeautifulSoup(res3.text, "html.parser")
        if soup3.select_one('#p_grid1_18 > td.r.cle') is None:
            ts3 = soup3.select_one('#p_grid1_13 > td.r.cle').text
        else:
            ts3 = soup3.select_one('#p_grid1_18 > td.r.cle').text
        print(ts3)
        ts31 = float(ts3)
        ROE = "%0.1f%%"%ts31
        print(ROE)
        print(type(ROE))

        ## 할인율(BBB- 회사채 5년 수익률) 구하기
        res4 = requests.get("https://www.kisrating.com/ratingsStatistics/statics_spread.do")
        soup4 = BeautifulSoup(res4.text, "html.parser")
        ts4 = soup4.select_one('#con_tab1 > div.table_ty1 > table > tbody > tr:nth-child(11) > td:nth-child(9)').text
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
        res5 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN=")
        soup5 = BeautifulSoup(res5.text, "html.parser")
        ts51 = (((soup5.select_one('#svdMainGrid1 > table > tbody > tr:nth-child(6)')).find("td", class_="r").text).split(sep='/', maxsplit=1))[0].replace(",","")
        shareOutstanding = int(ts51)
        print(shareOutstanding)
        print(type(shareOutstanding))

        ## 자기주식 구하기 - 성공
        res6 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_shareanalysis.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=109&stkGb=701")
        soup6 = BeautifulSoup(res6.text, "html.parser")
        ts61 = (soup6.select_one('#dataTable > tbody > tr:nth-child(5) > td:nth-child(3)').text).replace(",","")

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
        res7 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701")
        soup7 = BeautifulSoup(res7.text, "html.parser")
        ts71 = (soup7.select_one('#divDaechaY > table > tbody > tr:nth-child(12) > td.r.cle').text).replace(",","")
        cashEquivalents = int(ts71)*100000000
        cashEquivalentsShare = cashEquivalents/(shareOutstanding-ts62)
        print(cashEquivalentsShare)

        ## 주당 (가치 + 현금성자산) 구하기 - 성공
        valuePerShareCash = valuePerShare + cashEquivalentsShare
        print(valuePerShareCash)

        ## PER 구하기 - 성공
        res8 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701")
        soup8 = BeautifulSoup(res8.text, "html.parser")
        ts81 = (soup8.select_one('#corp_group2 > dl:nth-child(1) > dd').text)
        if ts81 == '-':
                PER = 0
        else :
                PER = float(ts81)
        print(PER)

        ## 연간이익률 구하기 = EBITDA증가율 + 배당수익률 - 성공
        res9 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701")
        soup9 = BeautifulSoup(res9.text, "html.parser")
        try:
            ts91 = (soup9.select_one('#p_grid1_11 > td.r.cle > span').text)
        except:
            ts91 = (soup9.select_one('#p_grid1_11 > td.r.cle').text)

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

        res10 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode="+StockNo+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701")
        soup10 = BeautifulSoup(res10.text, "html.parser")
        ts101 = ((soup10.select_one('#corp_group2 > dl:nth-child(5) > dd').text).split(sep='%', maxsplit=1))[0]
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
        url11 = "https://www.google.com/finance/quote/"+StockNo[1:]+":"+mrktCtg
        res11 = requests.get(url11)
        soup11 = BeautifulSoup(res11.text, "html.parser")
        # print("=============================================")
        # print(soup11.find_all("div", class_="rPF6Lc"))
        ts111 = (soup11.find("div", class_="YMlKec fxKbKc").text[1:]).replace(",","")
        currentPrice = float(ts111)
        print(currentPrice)
        currentPriceURL = url11

        ## 데이터 존재여부 판별
        if findStock(itmsNm, baseDate) is False:

            print("인서트")
            print(findStock(itmsNm, baseDate))

            insertStock(baseDate, itmsNm, DCRate, PER, currentPrice, currentPriceURL, ROE, EBITDARate, dividendRate, annualRateOfReturn,
                            annualRateOfReturnPER, cashEquivalents, cashEquivalentsShare, equity, excessEarnings,
                            shareOutstanding, totalValue, valuePerShare, valuePerShareCash)

        else:

            print("업데이트")
            print(findStock(itmsNm, baseDate))

            updateStock(baseDate, itmsNm, DCRate, PER, currentPrice, currentPriceURL, ROE, EBITDARate, dividendRate, annualRateOfReturn,
                            annualRateOfReturnPER, cashEquivalents, cashEquivalentsShare, equity, excessEarnings,
                            shareOutstanding, totalValue, valuePerShare, valuePerShareCash)


