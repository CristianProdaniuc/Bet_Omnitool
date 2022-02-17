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
        self.window.buttonListEvents.clicked.connect(self.listEvents)
        self.window.buttonLogoutTest.clicked.connect(self.logoutTest)

    def openAdjustBookmakerOdds(self):
        self.widgetAdjustBookmakerOdds = AdjustBookmakerOdds('gui\\adjust_bookmaker_odds.ui')

    def loginTest(self):
        with open('E:\\Software\\openssl-3.0.1\\apps\\client-2048.txt') as f:
            lines = f.readlines()

        payload = lines[0]
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'Content-Type': 'application/x-www-form-urlencoded'}
        self.resp = requests.post('https://identitysso-cert.betfair.ro/api/certlogin', data=payload, cert=('E:\\Software\\openssl-3.0.1\\apps\\client-2048.crt', 'E:\\Software\\openssl-3.0.1\\apps\\client-2048.key'), headers=headers)
 
        if self.resp.status_code == 200:
          self.resp_json = self.resp.json()
          print(self.resp_json['loginStatus'])
          print(self.resp_json['sessionToken'])
        else:
          print("Request failed.")

    def logoutTest(self):
        headers = {'Accept': 'application/json', 'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': self.resp_json['sessionToken']}
        self.resp2 = requests.post('https://identitysso.betfair.ro/api/logout', headers=headers)

        if self.resp2.status_code == 200:
          self.resp_json2 = self.resp2.json()
          print(self.resp_json2['status'])
          print(self.resp_json2['token'])
        else:
          print("Request failed.")

    def APItest(self):
        URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        jsonrpc_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': self.resp_json['sessionToken'], 'content-type': 'application/json'}
                                                                            
        try:
            req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            self.eventTypes = response.read()
        except urllib.error.URLError as e:
            print (e.reason) 
            print ('Oops no service available at ' + str(url))
            exit()
        except urllib.error.HTTPError:
            print ('Oops not a valid operation from the service ' + str(url))
            exit()

    def listEvents(self):
        URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        jsonrpc_req =  '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": { "filter": { "eventTypeIds": ["1"], \
                          "marketStartTime": { "from": "2022-02-17T00:00:00Z", "to": "2022-02-17T23:59:00Z"} } }, "id": 1}'
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': self.resp_json['sessionToken'], 'content-type': 'application/json'}

        try:
            req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            self.events = response.read()
        except urllib.error.URLError as e:
            print (e.reason) 
            print ('Oops no service available at ' + str(url))
            exit()
        except urllib.error.HTTPError:
            print ('Oops not a valid operation from the service ' + str(url))
            exit()

    def displayResults(self):
        print(self.eventTypes)
        print(self.events)
