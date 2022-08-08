class BLVTInfoEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.circulation = 0.0
        self.baskets = 0.0
        self.NAV = 0.0
        self.lev = 0.0  # Real Leverage
        self.target = 0.0  #  Target Leverage
        self.fundingRate = 0.0

    @staticmethod
    def json_parse(json_data):
        result = BLVTInfoEvent()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.symbol = json_data.get_string("s")
        result.circulation = json_data.get_float("m")
        result.baskets = json_data.get_string("b")
        result.NAV = json_data.get_float("n")
        result.lev = json_data.get_float("l")
        result.target = json_data.get_float("t")
        result.fundingRate = json_data.get_float("f")
        return result
