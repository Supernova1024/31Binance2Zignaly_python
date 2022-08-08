class BLVTNAVCandlestick:

    def __init__(self):
        self.openTime = 0
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.lev = 0.0  # Real leverage
        self.closeTime = 0
        self.numNAV = 0  # Number of NAV update

    @staticmethod
    def json_parse(json_data):
        result = BLVTNAVCandlestick()
        val = json_data.convert_2_list()
        result.openTime = val[0]
        result.open = val[1]
        result.high = val[2]
        result.low = val[3]
        result.close = val[4]
        result.lev = val[5]
        result.closeTime = val[6]
        result.numNAV = val[8]

        return result