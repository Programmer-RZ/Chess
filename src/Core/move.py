class Move:
    START_SQUARE = None
    TARGET_SQUARE = None

    EN_PASSANT = 1
    CASTLING = 2
    DOUBLE_PAWN_MOVE = 3
    PROMOTION = 4

    def __init__(self, START_SQUARE, TARGET_SQUARE):
        self.START_SQUARE = START_SQUARE
        self.TARGET_SQUARE = TARGET_SQUARE

        self.FLAG = None
        self.CAPTURED_PIECE = None