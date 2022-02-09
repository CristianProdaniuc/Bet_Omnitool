import sys, datetime
import urllib, urllib.request, urllib.error
import json

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

    def openAdjustBookmakerOdds(self):
        self.widgetAdjustBookmakerOdds = AdjustBookmakerOdds('gui\\adjust_bookmaker_odds.ui')

    def APItest(self):
        URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        jsonrpc_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': 'BhyTj0xci9nZLskepj+/e0lVRdgvKcfstaBYTWGUba0=', 'content-type': 'application/json'}
                                                                            
        try:
            req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            jsonResponse = response.read()
            return jsonResponse.decode('utf-8')
        except urllib.error.URLError as e:
            print (e.reason) 
            print ('Oops no service available at ' + str(url))
            exit()
        except urllib.error.HTTPError:
            print ('Oops not a valid operation from the service ' + str(url))
            exit()
