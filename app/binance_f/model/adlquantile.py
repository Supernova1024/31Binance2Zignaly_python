class AdlQuantile:

    def __init__(self):
        self.symbol = ""
        self.adlQuantile = ""

    @staticmethod
    def json_parse(json_wrapper):
        result = AdlQuantile()
        result.symbol = json_wrapper.get_string("symbol")
        result.adlQuantile = json_wrapper.get_string("adlQuantile")
        return result
