import utils


DIAG_DIRECTIONS = [(1, 1), (1, -1)]
SQ_DIRECTION = [(1, 0), (0, 1)]


class Board(object):
    def __init__(self):
        raise NotImplementedError

class Square(object):
    # 0,0 is bottom left
    def __init__(self, pos_y, pos_x):
        assert pos_x <= 7
        assert pos_y <= 7
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = White() if self.is_white() else Black()
        self.piece = None

    def is_black(self):
        return (self.pos_x + self.pos_y) % 2 == 0

    def is_white(self):
        return not self.is_black()


class Color(object):
    def __init__(self):
        return

    def is_white(self):
        raise NotImplementedError

    def is_black(self):
        raise NotImplementedError

    def other_color(self):
        raise NotImplementedError


class Black(Color):
    def __init__(self):
        super(Black, self).__init__()

    def is_white(self):
        return False

    def is_black(self):
        return True

    def other_color(self):
        return White()


class White(Color):
    def __init__(self):
        super(White, self).__init__()

    def is_white(self):
        return True

    def is_black(self):
        return False

    def other_color(self):
        return Black()


class Piece(object):
    def __init__(self, color):
        self.color = color
        return

    def possible_moves(self, pos_y, pos_x):
        raise NotImplementedError

    def possible_capture_moves(self, pos_y, pos_x):
        raise NotImplementedError


class Pawn(Piece):
    def __init__(self, color):
        super(Pawn, self).__init__(color)
        self._direction = 1 if self.color.is_white else -1

    def possible_moves(self, pos_y, pos_x):
        return utils.filter_within_board_moves([(pos_y + self._direction, pos_x)])

    def possible_capture_moves(self, pos_y, pos_x):
        return [(pos_y + self._direction, new_x) for new_x in [pos_x+1, pos_x-1]]


class Knight(Piece):
    def __init__(self, color):
        super(Knight, self).__init__(color)

    def possible_moves(self, pos_y, pos_x):
        deltas = [(2, 1), (1, 2)]
        moves = utils.flatten([[(dy*dry, dx*drx) for (dry, drx) in DIRECTIONS] for (dy, dx) in deltas])
        return utils.filter_within_board_moves([(pos_y+dy, pos_x+dx) for (dy, dx) in moves])

    def possible_capture_moves(self, pos_y, pos_x):
        return self.possible_moves(pos_y=pos_y, pos_x=pos_x)


class Bishop(Piece):
    def __init__(self, color):
        super(Bishop, self).__init__(color)

    def possible_moves(self, pos_y, pos_x):
        rg = range(-7, 8)
        moves = utils.flatten([[(dry*i, drx*i) for i in rg] for (dry, drx) in DIAG_DIRECTIONS])
        return utils.filter_within_board_moves([(pos_y+dy, pos_x+dx) for (dy, dx) in moves])

    def possible_capture_moves(self, pos_y, pos_x):
        return self.possible_moves(pos_y=pos_y, pos_x=pos_x)


class Rook(Piece):
    def __init__(self, color):
        super(Rook, self).__init__(color)

    def possible_moves(self, pos_y, pos_x):
        rg = range(-7, 8)
        sq_dirs = [(1, 0), (0, 1)]
        moves = utils.flatten([[(dry*i, drx*i) for i in rg] for (dry, drx) in SQ_DIRECTION])
        return utils.filter_within_board_moves([(pos_y+dy, pos_x+dx) for (dy, dx) in moves])

    def possible_capture_moves(self, pos_y, pos_x):
        return self.possible_moves(pos_y=pos_y, pos_x=pos_x)


class Queen(Piece):
    def __init__(self, color):
        super(Queen, self).__init__(color)
        self._direction = 1 if self.color.is_white else -1

    def possible_moves(self, pos_y, pos_x):
        rook_moves = Rook(self.color).possible_moves(pos_y, pos_x)
        bishop_moves = Rook(self.color).possible_moves(pos_y, pos_x)
        return rook_moves + bishop_moves

    def possible_capture_moves(self, pos_y, pos_x):
        return self.possible_moves()


class King(Piece):
    def __init__(self, color):
        super(King, self).__init__(color)
        self._direction = 1 if self.color.is_white else -1

    def possible_moves(self, pos_y, pos_x):
        return [(pos_y + self._direction, pos_x)]

    def possible_capture_moves(self, pos_y, pos_x):
        return [(pos_y + self._direction, new_x) for new_x in [pos_x + 1, pos_x - 1]]


