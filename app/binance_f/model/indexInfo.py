class BaseAsset:

    def __init__(self):
        self.baseAsset = ""
        self.weightInQuantity = 0.0
        self.weightInPercentage = 0.0
        
    @staticmethod
    def json_parse(json_data):
        result = BaseAsset()
        result.baseAsset = json_data.get_string("baseAsset")
        result.weightInQuantity = json_data.get_float("weightInQuantity")
        result.weightInPercentage = json_data.get_float("weightInPercentage")
        return result

class IndexInfo:

    def __init__(self):
        self.symbol = ""
        self.time = 0
        self.baseAssetList = list()
    
    @staticmethod
    def json_parse(json_data):
        result = IndexInfo()
        result.symbol = json_data.get_string("symbol")
        result.time = json_data.get_int("time")

        element_list = list()
        data_list = json_data.get_array("baseAssetList")
        for item in data_list.get_items():
            element = BaseAsset.json_parse(item)
            element_list.append(element)
        result.baseAssetList = element_list

        return result
