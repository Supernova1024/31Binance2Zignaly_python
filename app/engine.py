# from entity.OpenPosition import OpenPosition
import requests
import time
from datetime import datetime, timezone
from binance_f import RequestClient
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *
import json
from dateutil import parser

from models import *
from start import app, db
  
# Opening JSON file
with open('config.json', 'r') as openfile:
	json_object = json.load(openfile)

keys = json_object["master"]
zignaly_keys = json_object["slave"]
binance_futures_leverage = json_object["leverage"]

def resolvePositionKey(order):
	return order

def sendPost(request, zignaly_keys):
	try:
		position_str = json.dumps(request.__dict__)
		position_json = json.loads(position_str)

		print("========This request will be sent to :", zignaly_keys["url"])
		print(position_json, type(position_json))
		r = requests.post(zignaly_keys["url"], 
				data = position_json
			 )
		print("=========Sent to zignaly successfully=============")
		print("===Response :===", r)
		

	except Exception as e:
		print("====Error in sendPost function==========", e)

def savePosition(order, position):
	try:
		position.updateDate = datetime.now(timezone.utc)

		position_dict = {}
		position_dict["signalId"] = position.signalId
		position_dict["pair"] = position.pair
		position_dict["side"] = position.side
		position_dict["quantity"] = position.quantity
		position_dict["maxQuantity"] = position.maxQuantity
		position_dict["positionSize"] = position.positionSize
		position_dict["createDate"] = str(position.createDate)
		position_dict["updateDate"] = str(position.updateDate)
		position_dict["lastEventTime"] = position.lastEventTime
		position_dict["isClosed"] = position.isClosed
		position_dict["isCorrupted"] = position.isCorrupted

		position_str = json.dumps(position_dict)
		q = PositionString(positionKey=resolvePositionKey(order), positionString=position_str)
		db.session.add(q)
		db.session.commit()
	except Exception as e:
		print("====Error in savePosition function==========", e)

def createSignal(position, side, otype, positionSizePercentage):
	try:
		request = CreateSignalRequest()
		request.leverage = str(binance_futures_leverage)
		request.signalId = position.signalId
		request.pair = position.pair
		reduce1 = "World" in otype
		request.type = "update" if reduce1 else otype
		request.side = side
		request.orderType = "MARKET"

		if reduce1:
			request.reduceOrderType = "MARKET";
			request.reduceAvailablePercentage = str(positionSizePercentage)
		elif positionSizePercentage != None:
			request.positionSizePercentage = str(positionSizePercentage)

		# zignalyService.createSignal(request)
		request.key = zignaly_keys["api_key"]
		request.exchange = "zignaly"
		request.exchangeAccountType = "futures"
		request.stopLossFollowsTakeProfit = "True"

	except Exception as e:
		print("====Error in createSignal function==========", e)

	sendPost(request, zignaly_keys)

def resolvePositionKey(order):
	try:
		return order.positionSide + "-" + order.symbol;
	except Exception as e:
		print("====Error in resolvePositionKey function==========", e)

def processOrderUpdate(order):
	try:
		if order.orderStatus != "FILLED":
			print("Order is not FILLED")
			return False

		positionKey = resolvePositionKey(order)  # LONG-TRXUSDT
		
		orderKey = "ORDER-" + positionKey  # ORDER-LONG-TRXUSDT

		# Check if this order is in last order list of DB by order key
		orderKey_lastOrderEvent = LastOrderEvent.query.filter_by(orderKey=orderKey).first()

		if orderKey_lastOrderEvent != None:
			lastorderevent = orderKey_lastOrderEvent.lastorderevent
			# check eventTime to prevent double processing
			if lastorderevent >= order.orderTradeTime:
				print("This order already processed for position", positionKey)
				return False
			else:
				# Instead of Redis
				q = LastOrderEvent(orderKey=orderKey, lastorderevent=order.orderTradeTime)
				db.session.add(q)
				db.session.commit()

		else:
			q = LastOrderEvent(orderKey=orderKey, lastorderevent=order.orderTradeTime)
			db.session.add(q)
			db.session.commit()
		
		positionSizePercentage = None
		positionSize = round(order.origQty * order.avgPrice / binance_futures_leverage, 2)

		# Check whether it is a new postion or exsited position
		positionKey_positionString = PositionString.query.filter_by(positionKey=positionKey).first()

		if positionKey_positionString == None:
			position = OpenPosition()
			position.side = "LONG" if order.side == "BUY" else "SHORT"
			unique_random_id = str(int(round(time.time() * 1000)))
			position.signalId=unique_random_id
			position.pair=order.symbol
			position.quantity=order.origQty
			position.maxQuantity=order.origQty
			position.positionSize=positionSize
			position.createDate=datetime.now(timezone.utc)
			position.updateDate=datetime.now(timezone.utc)
			position.lastEventTime=order.orderTradeTime

			otype = "entry" # Type of signal
			positionSizePercentage = round(positionSize * 100 / walletBalance, 2)

		else:
			# todo create take profit order for position
			positionString = positionKey_positionString.positionString
			position = OpenPosition()
			position_json = json.loads(positionString)
			if position_json["isCorrupted"] == True:
				print("Open position is corrupted, order unable to open new position")
				# todo: check zignaly order if still open
				return true

			if position_json["side"] != order.positionSide:
				print("Stored position side does not match to order side")
				return True

			increase = order.side == "BUY" if position_json["side"] == "LONG" else order.side == "SELL"

			if increase :
				# todo: if position was not reduced yet - recreate take profit
				position_json["quantity"] = position_json["quantity"] + order.origQty
				position.quantity = position_json["quantity"]
				if position_json["quantity"] > position_json["maxQuantity"]:
					position_json["maxQuantity"] = position_json["maxQuantity"] + order.origQty
					position.maxQuantity = position_json["maxQuantity"]

				otype = "update"
				positionSizePercentage = round(positionSize * 100 / walletBalance, 2)
				position_json["positionSize"] = position_json["positionSize"] + positionSize
				position.positionSize = position_json["positionSize"]

				position.signalId=position_json["signalId"]
				position.side=position_json["side"]
				position.pair=position_json["pair"]
				position.maxQuantity=position_json["maxQuantity"]
				position.createDate=parser.parse(position_json["createDate"])
				position.updateDate=parser.parse(position_json["updateDate"])
				position.lastEventTime=position_json["lastEventTime"]
				position.isClosed=position_json["isClosed"]

			else:
				if position_json["quantity"] == position_json["maxQuantity"]:
					# todo: if first reduce order - create stop loss order
					print("Quantity equals with maxQuantity.")
				result = position_json["quantity"] - order.origQty
				if float(result) < 0:
					print(position_json["side"] + " position " + position_json["pair"] + " quantity is negative.")
					position_json["isCorrupted"] = True
					position.isCorrupted = position_json["isCorrupted"]

					position.signalId=position_json["signalId"]
					position.side=position_json["side"]
					position.pair=position_json["pair"]
					position.quantity=position_json["quantity"]
					position.maxQuantity=position_json["maxQuantity"]
					position.positionSize=position_json["positionSize"]
					position.createDate=parser.parse(position_json["createDate"])
					position.updateDate=parser.parse(position_json["updateDate"])
					position.lastEventTime=position_json["lastEventTime"]
					position.isClosed=position_json["isClosed"]

					savePosition(order, position)
					return True
				elif float(result) == 0:
					 position_json["isClosed"] = True
					 position.isClosed=position_json["isClosed"]
					 otype = "exit"
				else:
					otype = "update_reduce"
					positionSizePercentage = round(positionSize * 100 / walletBalance, 2)
					position_json["positionSize"] = position_json["positionSize"] - positionSize
					position.positionSize = position_json["positionSize"]

				position_json["quantity"] = result
				position.quantity = position_json["quantity"]

		createSignal(position, position.side, otype, positionSizePercentage)
		# update position with order
		if position.isClosed == True:
			print("Closing postion " + position.pair)
			db.session.add(position)
			db.session.commit()

			# Instead of Redis
			positionString.query.filter_by(positionKey=positionKey).delete()
			db.session.commit()
		else:
			savePosition(order, position)
	except Exception as e:
		print("====Error in processOrderUpdate function==========", e)
	return True


def callback(data_type: 'SubscribeMessageType', event: 'any'):
	if data_type == SubscribeMessageType.RESPONSE:
		print("Event ID: ", event)
	elif  data_type == SubscribeMessageType.PAYLOAD:
		if(event.eventType == "ORDER_TRADE_UPDATE"):
			### store filled order to db
			print("Event Type: ", event.eventType)
			print("Event time: ", event.eventTime)
			print("Transaction Time: ", event.transactionTime)
			print("Symbol: ", event.symbol)
			print("Client Order Id: ", event.clientOrderId)
			print("Side: ", event.side)
			print("Order Type: ", event.type)
			print("Time in Force: ", event.timeInForce)
			print("Original Quantity: ", event.origQty)
			print("Position Side: ", event.positionSide)
			print("Price: ", event.price)
			print("Average Price: ", event.avgPrice)
			print("Stop Price: ", event.stopPrice)
			print("Execution Type: ", event.executionType)
			print("Order Status: ", event.orderStatus)
			print("Order Id: ", event.orderId)
			print("Order Last Filled Quantity: ", event.lastFilledQty)
			print("Order Filled Accumulated Quantity: ", event.cumulativeFilledQty)
			print("Last Filled Price: ", event.lastFilledPrice)
			print("Commission Asset: ", event.commissionAsset)
			print("Commissions: ", event.commissionAmount)
			print("Order Trade Time: ", event.orderTradeTime)
			print("Trade Id: ", event.tradeID)
			print("Bids Notional: ", event.bidsNotional)
			print("Ask Notional: ", event.asksNotional)
			print("Is this trade the maker side?: ", event.isMarkerSide)
			print("Is this reduce only: ", event.isReduceOnly)
			print("stop price working type: ", event.workingType)
			print("Is this Close-All: ", event.isClosePosition)
			# print("RealizedProfit: ", event.realizedProfit, type(event.realizedProfit))
			if not event.activationPrice is None:
				print("Activation Price for Trailing Stop: ", event.activationPrice)
			if not event.callbackRate is None:
				print("Callback Rate for Trailing Stop: ", event.callbackRate)

			order = OrderUpdate()
			order = event
			if order != None:
				if processOrderUpdate(order):
					# store filled order to db
					q = SignalOrder(orderId=event.orderId, symbol=event.symbol, side=event.side, positionSide=event.positionSide, origQty=int(event.origQty), avgPrice=event.avgPrice, orderTradeTime=event.orderTradeTime)
					db.session.add(q)
					db.session.commit()

		elif(event.eventType == "listenKeyExpired"):
			print("Event: ", event.eventType)
			print("Event time: ", event.eventTime)
			print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
			print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
			print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
	else:
		print("Unknown Data:")
	print()

def error(e: 'BinanceApiException'):
	print(e.error_code + e.error_message)

def run():
	try:
		# Start a new user data stream. The stream will close after 60 minutes unless a keepalive is sent. If the account has an active listenKey, that listenKey will be returned and its validity will be extended for 60 minutes.
		request_client = RequestClient(api_key=keys["api_key"], secret_key=keys["secret_key"])
		listen_key = request_client.start_user_data_stream()

		accountInformation = request_client.get_account_information_v2()
		assets = accountInformation.assets
		for asset in assets:
			if asset.asset == "USDT":
				global walletBalance
				walletBalance = asset.walletBalance
				print("==walletBalance: ", asset.walletBalance)
				if walletBalance == 0:
					print("Wallet balance is 0")

		# Keepalive a user data stream to prevent a time out.
		result = request_client.keep_user_data_stream()

		# Create the subscription client to subscribe the update from server.
		client = SubscriptionClient(api_key=keys["api_key"], secret_key=keys["secret_key"])
	except Exception as e:
		print("====Error in run function==========", e)
	client.subscribe_user_data_event(listen_key, callback, error)