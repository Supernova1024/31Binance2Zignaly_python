class SymbolPrice:

    def __init__(self):
        self.symbol = ""
        self.price = 0.0
        self.time = 0

    @staticmethod
    def json_parse(json_data):
        result = SymbolPrice()
        result.symbol = json_data.get_string("symbol")
        result.price = json_data.get_float("price")
        result.time = json_data.get_int("time")
        return result