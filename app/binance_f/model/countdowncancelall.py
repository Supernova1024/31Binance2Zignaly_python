class CountdownCancelAll:

    def __init__(self):
        self.symbol = ""
        self.countdownTime = 0

    @staticmethod
    def json_parse(json_data):
        result = CountdownCancelAll()
        result.symbol = json_data.get_string("symbol")
        result.countdownTime = json_data.get_int("countdownTime")

        return result
