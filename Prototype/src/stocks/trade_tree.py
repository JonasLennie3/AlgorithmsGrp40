from src.stocks.trade import Trade
from src.stocks.trade_node import TradeNode


# This class models all information for a single stock name
# All transactions on a given stock will be stored here
# This has no model of any other stock names
# It implements a balanced search tree ADT using a left-leaning red-black binary search tree
# Each node in the tree is a TradeNode object
class TradeTree:
    # Initialize stock name and root node
    def __init__(self, stock_name: str) -> None:
        self.stock_name = stock_name
        self.root = None

    def put_trade(self, trade: Trade) -> None:
        # Ensure that the Trade object to be inserted matches the stock name of the current TradeTree object
        if trade.name != self.stock_name:
            raise ValueError("Invalid Stock Name")

        # Reassign root with updated TradeNode object
        self.root = self.__insert(trade, self.root)

        # Maintain invariant of coloring root node black
        self.root.color = TradeNode.BLACK

    def __insert(self, trade: Trade, node: TradeNode) -> TradeNode:
        # Recursive base case which inserts a new TradeNode object
        if node is None:
            return TradeNode(trade)

        # Use trade value as the key for inserting TradeNode objects into the TradeTree
        trade_val = trade.get_trade_val()

        # Recursive step case to determine appropriate insertion position
        if trade_val == node.trade_val:
            node.trades.append(trade)
        elif trade_val < node.trade_val:
            node.left = self.__insert(trade, node.left)
        elif trade_val > node.trade_val:
            node.right = self.__insert(trade, node.right)

        # Balance the TradeTree to maintain logarithmic height
        return TradeTree.__balance(node)

    def get_all_trades(self, node: TradeNode = None) -> list:
        # Base case where the root of the TradeTree has not been initialized
        if self.root is None:
            return []

        # Optional node parameter used to traverse some subtree
        if node is None:
            node = self.root

        # In order traversal of nodes
        all_trades = []
        if node.left is not None:
            all_trades = self.get_all_trades(node.left)
        all_trades.extend(node.trades)
        if node.right is not None:
            all_trades.extend(self.get_all_trades(node.right))

        return all_trades

    def get_min_trades(self) -> list:
        if self.root is None:
            return []

        # Iteratively traverse left until the bottom of the tree
        node = self.root
        while node.left is not None:
            node = node.left

        return node.trades

    def get_max_trades(self) -> list:
        if self.root is None:
            return []

        # Iteratively traverse right until the bottom of the tree
        node = self.root
        while node.right is not None:
            node = node.right

        return node.trades

    def get_floor_trades(self, high: float) -> list:
        node = self.root
        floor_trades = []

        while node is not None:
            # If trade value equal to threshold is found
            if node.trade_val == high:
                # Return transactions
                return node.trades

            # Else if trade value less than threshold
            elif node.trade_val < high:
                # Store transactions and go right
                floor_trades = node.trades
                node = node.right

            # Else if trade value greater than threshold
            elif node.trade_val > high:
                # Go left
                node = node.left

        return floor_trades

    def get_ceil_trades(self, low: float) -> list:
        node = self.root
        ceil_trades = []

        while node is not None:
            # If trade value equal to threshold is found
            if node.trade_val == low:
                # Return transactions
                return node.trades

            # Else if trade value greater than threshold
            elif node.trade_val > low:
                # Store transactions and go left
                ceil_trades = node.trades
                node = node.left

            # Else if trade value less than threshold
            elif node.trade_val < low:
                # Go right
                node = node.right

        return ceil_trades

    def get_trades_in_range(self, low: float, high: float, node: TradeNode = None) -> list:
        # Ensure that the low and high parameters are valid
        if low > high or low < 0:
            raise ValueError("Invalid Range")

        if self.root is None:
            return []

        if node is None:
            node = self.root

        trades_in_range = []

        # In order traversal if trade value is in range
        if low <= node.trade_val <= high:
            if node.left is not None:
                trades_in_range = self.get_trades_in_range(low, high, node.left)
            trades_in_range.extend(node.trades)
            if node.right is not None:
                trades_in_range.extend(self.get_trades_in_range(low, high, node.right))

        # Go right if trade value is less than lower bound
        elif node.trade_val < low and node.right is not None:
            trades_in_range = self.get_trades_in_range(low, high, node.right)

        # Go left if trade value is greater than higher bound
        elif node.trade_val > high and node.left is not None:
            trades_in_range = self.get_trades_in_range(low, high, node.left)

        return trades_in_range

    @staticmethod
    def __rotate_left(node: TradeNode) -> TradeNode:
        x = node.right
        node.right = x.left
        x.left = node
        x.color = node.color
        node.color = TradeNode.RED
        return x

    @staticmethod
    def __rotate_right(node: TradeNode) -> TradeNode:
        x = node.left
        node.left = x.right
        x.right = node
        x.color = node.color
        node.color = TradeNode.RED
        return x

    @staticmethod
    def __flip_colors(node: TradeNode) -> None:
        node.color = TradeNode.RED
        node.left.color = TradeNode.BLACK
        node.right.color = TradeNode.BLACK

    @staticmethod
    def __is_red(node: TradeNode) -> bool:
        return node.color == TradeNode.RED if node is not None else False

    # Maintains the structural invariants of a left-leaning red-black binary search tree
    @staticmethod
    def __balance(node: TradeNode) -> TradeNode:
        # Perform rotations if required
        if TradeTree.__is_red(node.right) and not TradeTree.__is_red(node.left):
            node = TradeTree.__rotate_left(node)
        if TradeTree.__is_red(node.left) and TradeTree.__is_red(node.left.left):
            node = TradeTree.__rotate_right(node)

        # Flip colors if required
        if TradeTree.__is_red(node.left) and TradeTree.__is_red(node.right):
            TradeTree.__flip_colors(node)

        return node
