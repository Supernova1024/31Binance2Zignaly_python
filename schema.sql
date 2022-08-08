DROP TABLE IF EXISTS signal_order;
CREATE TABLE signal_order (
	id integer primary key autoincrement,
	orderId string not null,
	symbol string not null,
	side string not null,
	positionSide string not null,
	origQty integer  not null,
	avgPrice integer not null,
	orderTradeTime string not null
);

DROP TABLE IF EXISTS position;
CREATE TABLE position (
	id integer primary key autoincrement,
	signalId string not null,
	pair string not null,
	side string not null,
	quantity integer not null,
	maxQuantity integer not null,
	positionSize integer not null,
	createDate text not null,
	updateDate text not null,
	lastEventTime text not null,
	isClosed string not null,
	isCorrupted string not null
);

DROP TABLE IF EXISTS last_order_event;
CREATE TABLE last_order_event (
	id integer primary key autoincrement,
	orderKey string not null,
	lastorderevent integer not null
);

DROP TABLE IF EXISTS positionString;
CREATE TABLE PositionString (
	id integer primary key autoincrement,
	positionKey string not null,
	positionString text not null
);

DROP TABLE IF EXISTS CreateSignalRequest;
CREATE TABLE CreateSignalRequest (
	id integer primary key autoincrement,
	key string not null,
	exchange string not null,
	exchangeAccountType string not null,
	leverage string not null,
	signalId string not null,
	pair string not null,
	type string not null,
	side string not null,
	orderType string not null,
	positionSizePercentage string not null,
	reduceOrderType string not null,
	reduceAvailablePercentage string not null,
	limitPrice string not null,
	stopLossFollowsTakeProfit string not null
);


