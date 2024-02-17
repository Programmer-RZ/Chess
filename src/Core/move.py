class Move:
    START_SQUARE = None
    TARGET_SQUARE = None

    EN_PASSANT_FLAG = 1
    CASTLING_FLAG = 2

    def __init__(self, START_SQUARE, TARGET_SQUARE):
        self.START_SQUARE = START_SQUARE
        self.TARGET_SQUARE = TARGET_SQUARE
        self.FLAG = None