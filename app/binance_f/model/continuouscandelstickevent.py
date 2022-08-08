import copy
class ContinuousCandlestick:

    def __init__(self):
        self.startTime = 0
        self.closeTime = 0
        self.pair = ""
        self.contract_type = ""
        self.interval = ""
        self.firstTradeId = 0
        self.lastTradeId = 0
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.volume = 0.0
        self.numTrades = 0
        self.isClosed = False
        self.baseVolume = 0.0
        self.takerBuyQuoteAssetVolume = 0.0
        self.takerBuyBaseAssetVolume = 0.0
        self.ignore = 0.0

    @staticmethod
    def json_parse(json_data):
        data_obj = ContinuousCandlestick()
        data_obj.startTime = json_data.get_int("t")
        data_obj.closeTime = json_data.get_int("T")
        data_obj.interval = json_data.get_string("i")
        data_obj.firstTradeId = json_data.get_int("f")
        data_obj.lastTradeId = json_data.get_int("L")
        data_obj.open = json_data.get_float("o")
        data_obj.close = json_data.get_float("c")
        data_obj.high = json_data.get_float("h")
        data_obj.low = json_data.get_float("l")
        data_obj.volume = json_data.get_float("v")
        data_obj.numTrades = json_data.get_int("n")
        data_obj.isClosed = json_data.get_boolean("x")
        data_obj.baseVolume = json_data.get_float("q")
        data_obj.takerBuyQuoteAssetVolume = json_data.get_float("V")
        data_obj.takerBuyBaseAssetVolume = json_data.get_float("Q")
        data_obj.ignore = json_data.get_int("B")

        return data_obj


class ContinuousCandlestickEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.pair = ""
        self.data = ContinuousCandlestick()

    @staticmethod
    def json_parse(json_wrapper):
        continuous_candlestick_event = ContinuousCandlestickEvent()
        continuous_candlestick_event.eventType = json_wrapper.get_string("e")
        continuous_candlestick_event.eventTime = json_wrapper.get_int("E")
        continuous_candlestick_event.pair = json_wrapper.get_string("ps")
        continuous_candlestick_event.contract_type = json_wrapper.get_string("ct")
        data = ContinuousCandlestick.json_parse(json_wrapper.get_object("k"))
        continuous_candlestick_event.data = copy.deepcopy(data)
        return continuous_candlestick_event

