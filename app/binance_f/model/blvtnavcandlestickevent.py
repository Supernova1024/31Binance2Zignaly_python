class BLVTNAVCandlestick:

    def __init__(self):
        self.startTime = 0
        self.closeTime = 0
        self.symbol = ""
        self.interval = ""
        self.firstUpdateTime = 0
        self.lastUpdateTime = 0
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.lev = 0.0
        self.numUpdates = 0

    @staticmethod
    def json_parse(json_data):
        data_obj = BLVTNAVCandlestick()
        data_obj.startTime = json_data.get_int("t")
        data_obj.closeTime = json_data.get_int("T")
        data_obj.symbol = json_data.get_string("s")
        data_obj.interval = json_data.get_string("i")
        data_obj.firstUpdateTime = json_data.get_int("f")
        data_obj.lastUpdateTime = json_data.get_int("L")
        data_obj.open = json_data.get_float("o")
        data_obj.close = json_data.get_float("c")
        data_obj.high = json_data.get_float("h")
        data_obj.low = json_data.get_float("l")
        data_obj.lev = json_data.get_float("v")
        data_obj.numUpdates = json_data.get_int("n")
  
        return data_obj


class BLVTNAVCandlestickEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.data = BLVTNAVCandlestick()

    @staticmethod
    def json_parse(json_wrapper):
        candlestick_event = BLVTNAVCandlestickEvent()
        candlestick_event.eventType = json_wrapper.get_string("e")
        candlestick_event.eventTime = json_wrapper.get_int("E")
        candlestick_event.symbol = json_wrapper.get_string("s")
        data = BLVTNAVCandlestick.json_parse(json_wrapper.get_object("k"))
        candlestick_event.data = data
        return candlestick_event

