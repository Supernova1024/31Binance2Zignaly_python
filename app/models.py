from start import db

class SignalOrder(db.Model):
	__tablename__ = 'signal_order'
	id = db.Column(db.Integer, primary_key = True)
	orderId = db.Column(db.String(255))
	symbol = db.Column(db.String(255))
	side = db.Column(db.String(255))
	positionSide = db.Column(db.String(255))
	origQty = db.Column(db.Integer)
	avgPrice = db.Column(db.Integer)
	orderTradeTime = db.Column(db.String(255))

class OpenPosition(db.Model):
	__tablename__ = 'position'
	id = db.Column(db.Integer, primary_key = True)
	signalId = db.Column(db.String(255))
	pair = db.Column(db.String(255))
	side = db.Column(db.String(255))
	quantity = db.Column(db.Integer)
	maxQuantity = db.Column(db.Integer)
	positionSize = db.Column(db.Integer)
	createDate = db.Column(db.DateTime)
	updateDate = db.Column(db.DateTime)
	lastEventTime = db.Column(db.String(255))
	isClosed = db.Column(db.Boolean, default=False)
	isCorrupted = db.Column(db.Boolean, default=False)

class LastOrderEvent(db.Model):
	__tablename__ = 'last_order_event'
	id = db.Column(db.Integer, primary_key = True)
	orderKey = db.Column(db.String(255))
	lastorderevent = db.Column(db.Integer)

class PositionString(db.Model):
	__tablename__ = 'positionString'
	id = db.Column(db.Integer, primary_key = True)
	positionKey = db.Column(db.String(255))
	positionString = db.Column(db.Text)

class CreateSignalRequest:
	__tablename__ = 'CreateSignalRequest'
	id = db.Column(db.Integer, primary_key = True)
	key = db.Column(db.String(255))
	exchange = db.Column(db.String(255))
	exchangeAccountType = db.Column(db.String(255))
	leverage = db.Column(db.String(255))
	signalId = db.Column(db.String(255))
	pair = db.Column(db.String(255))
	type = db.Column(db.String(255))
	side = db.Column(db.String(255))
	orderType = db.Column(db.String(255))
	positionSizePercentage = db.Column(db.String(255))
	reduceOrderType = db.Column(db.String(255))
	reduceAvailablePercentage = db.Column(db.String(255))
	limitPrice = db.Column(db.String(255))
	stopLossFollowsTakeProfit = db.Column(db.Boolean, default=False)

		
