class Composition:

    def __init__(self):
        self.baseAsset = ""
        self.wQty = 0.0  # Weight in quantity
        self.wPct = 0.0  # Weight in percentage

    @staticmethod
    def json_parse(json_data):
        data_obj = Composition()
        data_obj.baseAsset = json_data.get_string("b")
        data_obj.wQty = json_data.get_float("w")
        data_obj.wPct = json_data.get_float("W")

class CompositeIndexEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.price = 0.0
        self.composition = list()

    @staticmethod
    def json_parse(json_data):
        composite_index_event = CompositeIndexEvent()
        composite_index_event.eventType = json_data.get_string("e")
        composite_index_event.eventTime = json_data.get_int("E")
        composite_index_event.symbol = json_data.get_string("s")
        composite_index_event.price = json_data.get_folat("p")

        list_array = json_data.get_array("c")
        composition_list = list()
        for item in list_array.get_items():
            c = Composition.json_parse(item)
            composition_list.append(c)
        composite_index_event.composition = composition_list

        return composite_index_event