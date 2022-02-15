import sys, datetime
import urllib, urllib.request, urllib.error
import json
import requests

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow

from adjust_bookmaker_odds import AdjustBookmakerOdds

class Main(QMainWindow):

    def __init__(self, ui_file):
        super(Main, self).__init__()
        self.window = uic.loadUi(ui_file, self)
        self.window.show()

        self.window.buttonAdjustBookmakerOdds.clicked.connect(self.openAdjustBookmakerOdds)
        self.window.buttonAPItest.clicked.connect(self.APItest)
        self.window.buttonDisplayResults.clicked.connect(self.displayResults)
        self.window.buttonLoginTest.clicked.connect(self.loginTest)

    def openAdjustBookmakerOdds(self):
        self.widgetAdjustBookmakerOdds = AdjustBookmakerOdds('gui\\adjust_bookmaker_odds.ui')

    def loginTest(self):
        with open('E:\\Software\\openssl-3.0.1\\apps\\client-2048.txt') as f:
            lines = f.readlines()

        payload = lines[0]
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'Content-Type': 'application/x-www-form-urlencoded'}
 
        resp = requests.post('https://identitysso-cert.betfair.ro/api/certlogin', data=payload, cert=('E:\\Software\\openssl-3.0.1\\apps\\client-2048.crt', 'E:\\Software\\openssl-3.0.1\\apps\\client-2048.key'), headers=headers)
 
        if resp.status_code == 200:
          resp_json = resp.json()
          print(resp_json['loginStatus'])
          print(resp_json['sessionToken'])
        else:
          print("Request failed.")

    def APItest(self):
        URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        jsonrpc_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': 'nryTHQP6r56YUKlMHEIDwASkdYpYToxQMG8sg7qQlvY=', 'content-type': 'application/json'}
                                                                            
        try:
            req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            self.jsonResponse = response.read()
            self.jsonResponse = self.jsonResponse.decode('utf-8')
            return self.jsonResponse
        except urllib.error.URLError as e:
            print (e.reason) 
            print ('Oops no service available at ' + str(url))
            exit()
        except urllib.error.HTTPError:
            print ('Oops not a valid operation from the service ' + str(url))
            exit()

    def displayResults(self):
        print(self.jsonResponse)
