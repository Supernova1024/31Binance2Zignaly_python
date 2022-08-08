class BalanceV2:

    def __init__(self):
        self.accountAlias = ""
        self.asset = ""
        self.balance = 0.0
        self.crossWalletBalance = 0.0
        self.crossUnPnl = 0.0
        self.availableBalance = 0.0
        self.maxWithdrawAmount = 0.0

    @staticmethod
    def json_parse(json_data):
        result = BalanceV2()
        result.accountAlias = json_data.get_string("accountAlias")
        result.asset = json_data.get_string("asset")
        result.balance = json_data.get_float("balance")
        result.crossWalletBalance = json_data.get_float("crossWalletBalance")
        result.crossUnPnl = json_data.get_float("crossUnPnl")
        result.availableBalance = json_data.get_float("availableBalance")
        result.maxWithdrawAmount = json_data.get_float("maxWithdrawAmount")

        return result