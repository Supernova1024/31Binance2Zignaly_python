class AssetV2:

    def __init__(self):
        self.asset = ""
        self.initialMargin = 0.0
        self.maintMargin = 0.0
        self.marginBalance = 0.0
        self.maxWithdrawAmount = 0.0
        self.openOrderInitialMargin = 0.0
        self.positionInitialMargin = 0.0
        self.unrealizedProfit = 0.0
        self.walletBalance = 0.0
        self.crossWalletBalance = 0.0
        self.crossUnPnl = 0.0
        self.availableBalance = 0.0

    @staticmethod
    def json_parse(json_data):
        result = AssetV2()
        result.asset = json_data.get_string("asset")
        result.initialMargin = json_data.get_float("initialMargin")
        result.maintMargin = json_data.get_float("maintMargin")
        result.marginBalance = json_data.get_float("marginBalance")
        result.maxWithdrawAmount = json_data.get_float("maxWithdrawAmount")
        result.openOrderInitialMargin = json_data.get_float("openOrderInitialMargin")
        result.positionInitialMargin = json_data.get_float("positionInitialMargin")
        result.unrealizedProfit = json_data.get_float("unrealizedProfit")
        result.walletBalance = json_data.get_float("walletBalance")
        result.crossWalletBalance = json_data.get_float("crossWalletBalance")
        result.crossUnPnl = json_data.get_float("crossUnPnl")
        result.availableBalance = json_data.get_float("availableBalance")
        return result


class PositionV2:

    def __init__(self):
        self.initialMargin = 0.0
        self.maintMargin = 0.0
        self.openOrderInitialMargin = 0.0
        self.positionInitialMargin = 0.0
        self.symbol = ""
        self.leverage = 0.0
        self.unrealizedProfit = 0.0
        self.isolated = False
        self.positionSide = ""
        self.entryPrice = 0.0
        self.maxNotional = 0.0

    @staticmethod
    def json_parse(json_data):
        result = PositionV2()
        result.initialMargin = json_data.get_float("initialMargin")
        result.maintMargin = json_data.get_float("maintMargin")
        result.leverage = json_data.get_float("leverage")
        result.openOrderInitialMargin = json_data.get_float("openOrderInitialMargin")
        result.positionInitialMargin = json_data.get_float("positionInitialMargin")
        result.symbol = json_data.get_string("symbol")
        result.unrealizedProfit = json_data.get_float("unrealizedProfit")
        result.isolated = json_data.get_boolean("isolated")
        result.positionSide = json_data.get_string("positionSide")
        result.entryPrice = json_data.get_float("entryPrice")
        result.maxNotional = json_data.get_float("maxNotional")
        return result


class AccountInformationV2:
    def __init__(self):
        self.canDeposit = False
        self.canTrade = False
        self.canWithdraw = False
        self.feeTier = 0
        self.maxWithdrawAmount = 0.0
        self.totalInitialMargin = 0.0
        self.totalMaintMargin = 0.0
        self.totalMarginBalance = 0.0
        self.totalOpenOrderInitialMargin = 0.0
        self.totalPositionInitialMargin = 0.0
        self.totalCrossWalletBalance = 0.0
        self.totalCrossUnPnl = 0.0
        self.availableBalance = 0.0
        self.totalUnrealizedProfit = 0.0
        self.totalWalletBalance = 0.0
        self.updateTime = 0
        self.assets = list()
        self.positions = list()

    @staticmethod
    def json_parse(json_data):
        result = AccountInformationV2()
        result.canDeposit = json_data.get_boolean("canDeposit")
        result.canTrade = json_data.get_boolean("canTrade")
        result.canWithdraw = json_data.get_boolean("canWithdraw")
        result.feeTier = json_data.get_float("feeTier")
        result.maxWithdrawAmount = json_data.get_float("maxWithdrawAmount")
        result.totalInitialMargin = json_data.get_float("totalInitialMargin")
        result.totalMaintMargin = json_data.get_float("totalMaintMargin")
        result.totalMarginBalance = json_data.get_float("totalMarginBalance")
        result.totalOpenOrderInitialMargin = json_data.get_float("totalOpenOrderInitialMargin")
        result.totalCrossWalletBalance = json_data.get_float("totalCrossWalletBalance")
        result.totalCrossUnPnl = json_data.get_float("totalCrossUnPnl")
        result.availableBalance = json_data.get_float("availableBalance")
        result.totalPositionInitialMargin = json_data.get_float("totalPositionInitialMargin")
        result.totalUnrealizedProfit = json_data.get_float("totalUnrealizedProfit")
        result.totalWalletBalance = json_data.get_float("totalWalletBalance")
        result.updateTime = json_data.get_int("updateTime")
        
        element_list = list()
        data_list = json_data.get_array("assets")
        for item in data_list.get_items():
            element = AssetV2.json_parse(item)
            element_list.append(element)
        result.assets = element_list
        
        element_list = list()
        data_list = json_data.get_array("positions")
        for item in data_list.get_items():
            element = PositionV2.json_parse(item)
            element_list.append(element)
        result.positions = element_list

        return result
