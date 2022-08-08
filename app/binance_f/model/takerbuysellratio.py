

class TakerBuySellRatio:

    def __init__(self):
        self.buySellRatio = 0.0
        self.buyVol = 0.0
        self.sellVol = 0.0
        self.timestamp = 0
    
    @staticmethod
    def json_parse(json_data):
        result = TakerBuySellRatio()
        result.buySellRatio = json_data.get_float("buySellRatio")
        result.buyVol = json_data.get_float("buyVol")
        result.sellVol = json_data.get_float("sellVol")
        result.timestamp = json_data.get_int("timestamp")

        return result
