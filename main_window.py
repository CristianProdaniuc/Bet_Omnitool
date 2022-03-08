import sys, datetime
import urllib, urllib.request, urllib.error
import json
import requests
import queue, threading

import betfairlightweight
from betfairlightweight.filters import streaming_market_filter, streaming_market_data_filter
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow

from adjust_bookmaker_odds import AdjustBookmakerOdds

class Main(QMainWindow):

    def __init__(self, ui_file):
        super(Main, self).__init__()
        self.window = uic.loadUi(ui_file, self)
        self.window.show()

        self.window.buttonAdjustBookmakerOdds.clicked.connect(self.openAdjustBookmakerOdds)
        self.window.buttonListEventTypes.clicked.connect(self.listEventTypes)
        self.window.buttonDisplayResults.clicked.connect(self.displayResults)
        self.window.buttonLoginTest.clicked.connect(self.loginTest)
        self.window.buttonListEvents.clicked.connect(self.listEvents)
        self.window.buttonListMarketTypes.clicked.connect(self.listMarketTypes)
        self.window.buttonLogoutTest.clicked.connect(self.logoutTest)
        self.window.buttonStreamAPI.clicked.connect(self.testStreamAPI)

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

    def listEventTypes(self):
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
                          "marketStartTime": { "from": "2022-03-08T19:55:00Z", "to": "2022-03-08T20:03:00Z"} } }, "id": 1}'
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

    def listMarketTypes(self):
        URL = url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        jsonrpc_req =  '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketTypes", "params": { "filter": { "eventTypeIds": ["1"], "eventIds":["31244947"] } }, "id": 1}'
        headers = {'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': self.resp_json['sessionToken'], 'content-type': 'application/json'}

        try:
            req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), headers)
            response = urllib.request.urlopen(req)
            self.marketTypes = response.read()
        except urllib.error.URLError as e:
            print (e.reason) 
            print ('Oops no service available at ' + str(url))
            exit()
        except urllib.error.HTTPError:
            print ('Oops not a valid operation from the service ' + str(url))
            exit()

    def testStreamAPI(self):
        with open('E:\\Software\\openssl-3.0.1\\apps\\client-2048.txt') as f:
            lines = f.readlines()

        payload = lines[0]
        username = payload[9:27]
        password = payload[37:]

        trading = betfairlightweight.APIClient(username, password, app_key="h3wqckK1N6QPkUrC", certs='E:\\Software\\openssl-3.0.1\\apps\\certificates', locale="romania")
        trading.login()
        
        print(trading.session_token)

        headers = {'Accept': 'application/json', 'X-Application': 'h3wqckK1N6QPkUrC', 'X-Authentication': trading.session_token}
        logout_req = requests.post('https://identitysso.betfair.ro/api/logout', headers=headers)

        # create queue
        output_queue = queue.Queue()

        # create stream listener
        listener = betfairlightweight.StreamListener(output_queue=output_queue)

        # create stream
        stream = trading.streaming.create_stream(listener=listener)

        # create filters (GB WIN racing)
        market_filter = streaming_market_filter(
            event_type_ids=["31273133"], country_codes=["GB"], market_types=["WIN"]
        )
        market_data_filter = streaming_market_data_filter(
            fields=["EX_BEST_OFFERS", "EX_MARKET_DEF"], ladder_levels=3
        )

        # subscribe
        streaming_unique_id = stream.subscribe_to_markets(
            market_filter=market_filter,
            market_data_filter=market_data_filter,
            conflate_ms=1000,  # send update every 1000ms
        )

        # start stream in a new thread (in production would need err handling)
        t = threading.Thread(target=stream.start, daemon=True)
        t.start()

        # check for updates in output queue
        while True:
            market_books = output_queue.get()
            print(market_books)

            for market_book in market_books:
                print(
                    market_book,
                    market_book.streaming_unique_id,  # unique id of stream (returned from subscribe request)
                    market_book.streaming_update,  # json update received
                    market_book.market_definition,  # streaming definition, similar to catalogue request
                    market_book.publish_time,  # betfair publish time of update
                )

        print('test stream API')

        #if logout_req.status_code == 200:
        #  logout_json = logout_req.json()
        #  print(logout_json['status'])
        #  print(logout_json['token'])
        #else:
        #  print("Request failed.")


    def displayResults(self):
        print(self.eventTypes)
        print(self.events)
        print(self.marketTypes)