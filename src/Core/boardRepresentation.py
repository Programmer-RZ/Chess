class BoardRepresentation:
    a1 = 0
    b1 = 1
    c1 = 2
    d1 = 3
    e1 = 4
    f1 = 5
    g1 = 6
    h1 = 7

    a8 = 56
    b8 = 57
    c8 = 58
    d8 = 59
    e8 = 60
    f8 = 61
    g8 = 62
    h8 = 63

    def RankIndex(square):
        return square >> 3
    
    def FileIndex(square):
        return square & 0b000111