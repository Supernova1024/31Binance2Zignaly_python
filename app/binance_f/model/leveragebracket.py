class Bracket:

    def __init__(self):
        self.bracket = 0
        self.initialLeverage = 0
        self.notionalCap = 0.0
        self.notionalFloor = 0.0
        self.maintMarginRatio = 0.0
        self.cum = 0.0
        
    @staticmethod
    def json_parse(json_data):
        result = Bracket()
        result.bracket = json_data.get_int("bracket")
        result.initialLeverage = json_data.get_int("initialLeverage")
        result.notionalCap = json_data.get_float("notionalCap")
        result.notionalFloor = json_data.get_float("notionalFloor")
        result.maintMarginRatio = json_data.get_float("maintMarginRatio")
        result.cum = json_data.get_float("cum")
        return result

class LeverageBracket:

    def __init__(self):
        self.symbol = ""
        self.brackets = list()
    
    @staticmethod
    def json_parse(json_data):
        result = LeverageBracket()
        result.symbol = json_data.get_string("symbol")

        element_list = list()
        data_list = json_data.get_array("brackets")
        for item in data_list.get_items():
            element = Bracket.json_parse(item)
            element_list.append(element)
        result.brackets = element_list

        return result
