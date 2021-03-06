from src.stocks.abstract_platform import AbstractStockTradingPlatform
from src.stocks.trade import Trade
from src.stocks.trade_tree import TradeTree


# noinspection PyPep8Naming
# This class implements a hash table ADT using a Python's built-in dictionary data structure
# The keys are the stock names and the values are references to TradeTree objects
# Each method in this class does thorough error checking before calling operations on the TradeTree objects
class StockTradingPlatform(AbstractStockTradingPlatform):
    def __init__(self) -> None:
        # noinspection SpellCheckingInspection
        self.STOCKS = ["Barclays", "HSBA", "Lloyds Banking Group", "NatWest Group", "Standard Chartered", "3i",
                       "Abrdn", "Hargreaves Lansdown", "London Stock Exchange Group", "Pershing Square Holdings",
                       "Schroders", "St. James's Place plc."]

        self.__trade_trees = {}

        for stock in self.STOCKS:
            self.__trade_trees[stock] = TradeTree(stock)

    def logTransaction(self, transactionRecord: list) -> None:
        trade = Trade(*transactionRecord)
        self.__validate_trade(trade)
        self.__trade_trees[trade.name].put_trade(trade)

    def sortedTransactions(self, stockName: str) -> list:
        if stockName not in self.STOCKS:
            raise ValueError("sortedTransactions: Invalid Stock Name: " + stockName)

        return self.__trade_trees[stockName].get_all_trades()

    def minTransactions(self, stockName: str) -> list:
        if stockName not in self.STOCKS:
            raise ValueError("minTransactions: Invalid Stock Name: " + stockName)

        return self.__trade_trees[stockName].get_min_trades()

    def maxTransactions(self, stockName: str) -> list:
        if stockName not in self.STOCKS:
            raise ValueError("maxTransactions: Invalid Stock Name: " + stockName)

        return self.__trade_trees[stockName].get_max_trades()

    def floorTransactions(self, stockName: str, thresholdValue: float) -> list:
        if stockName not in self.STOCKS:
            raise ValueError("floorTransactions: Invalid Stock Name: " + stockName)

        if thresholdValue < 0:
            raise ValueError("floorTransactions: Invalid Transaction Value: " + str(thresholdValue))

        return self.__trade_trees[stockName].get_floor_trades(thresholdValue)

    def ceilingTransactions(self, stockName: str, thresholdValue: float) -> list:
        if stockName not in self.STOCKS:
            raise ValueError("ceilingTransactions: Invalid Stock Name: " + stockName)

        if thresholdValue < 0:
            raise ValueError("ceilingTransactions: Invalid Transaction Value: " + str(thresholdValue))

        return self.__trade_trees[stockName].get_ceil_trades(thresholdValue)

    def rangeTransactions(self, stockName: str, fromValue: float, toValue: float) -> list:
        if stockName not in self.STOCKS:
            raise ValueError("rangeTransactions: Invalid Stock Name: " + stockName)

        if fromValue > toValue or fromValue < 0 or toValue < 0:
            raise ValueError(
                "rangeTransactions: Invalid Range Bounds: fromValue: " + str(fromValue) + " toValue: " + str(toValue)
            )

        return self.__trade_trees[stockName].get_trades_in_range(fromValue, toValue)

    # Ensures that the transaction records to be inserted are valid
    def __validate_trade(self, trade: Trade) -> None:
        if trade.name not in self.STOCKS:
            raise ValueError("Invalid Stock Name: " + trade.name)

        if trade.quantity < 1:
            raise ValueError("Invalid Stock Quantity: " + str(trade.quantity))

        if trade.price <= 0.0:
            raise ValueError("Invalid Stock Price: " + str(trade.price))
