class Indicator:

    def __init__(self):
        self.isLocked = False
        self.plannedRecoverTime = 0
        self.indicator = ""
        self.value = 0.0
        self.triggerValue = 0.0

    @staticmethod
    def json_parse(json_data):
        result = Indicator()
        result.isLocked = json_data.get_boolean("isLocked")
        result.plannedRecoverTime = json_data.get_int("plannedRecoverTime")
        result.indicator = json_data.get_float("indicator")
        result.value = json_data.get_float("value")
        result.triggerValue = json_data.get_float("triggerValue")
        return result

class ApiTradingStatus:
    def __init__(self):
        self.indicators = object()

    @staticmethod
    def json_parse(json_data):
        result = ApiTradingStatus()
        
        element_list = list()
        data_list = json_data.get_array("indicators")
        for item in data_list.get_items():
            element = Indicator.json_parse(item)
            element_list.append(element)
        result.positions = element_list

        return result
