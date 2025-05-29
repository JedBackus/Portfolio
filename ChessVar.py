# Author: Jedidiah Backus
# GitHub username: JedBackus
# Date: 8/16/2023
# Description:  A variation of Chess. Uses 6 pieces from a standard chess set. 1 king, 1 rook, 2 bishops, and 2 knights. The goal of the game is to get your king from the starting row
#                   (row 1) to the finishing row (row 8) before the other player. Each player gets the same number of turns, so a tie is possible. Additionally, intentional or accidental
#                   checking of your king or the opponent's king is not allowed. Pieces move as they would in regular chess. Good luck.

class ChessVar:
    """class for playing a variation of chess"""

    def __init__(
            self):  # initializes a game. uses the Pieces class to create the needed pieces and then adds them to the board.
        """method for adding new chess game"""
        row8 = [["a8"], ["b8"], ["c8"], ["d8"], ["e8"], ["f8"], ["g8"], ["h8"]]
        row7 = [["a7"], ["b7"], ["c7"], ["d7"], ["e7"], ["f7"], ["g7"], ["h7"]]
        row6 = [["a6"], ["b6"], ["c6"], ["d6"], ["e6"], ["f6"], ["g6"], ["h6"]]
        row5 = [["a5"], ["b5"], ["c5"], ["d5"], ["e5"], ["f5"], ["g5"], ["h5"]]
        row4 = [["a4"], ["b4"], ["c4"], ["d4"], ["e4"], ["f4"], ["g4"], ["h4"]]
        row3 = [["a3"], ["b3"], ["c3"], ["d3"], ["e3"], ["f3"], ["g3"], ["h3"]]
        row2 = [["a2"], ["b2"], ["c2"], ["d2"], ["e2"], ["f2"], ["g2"], ["h2"]]
        row1 = [["a1"], ["b1"], ["c1"], ["d1"], ["e1"], ["f1"], ["g1"], ["h1"]]
        self._game_state = 'UNFINISHED'  # game state will be unfinished until there is a winner or a tie (updated at the end of each BLACK turn)
        self._board = [row8, row7, row6, row5, row4, row3, row2, row1]
        self._turn = 'WHITE'  # used to ensure a player doesn't move an opponent's piece; replaced "which_turn" method from halfway report. simpler and easier to implement.
        self._captured = []  # pieces are moved here when captured. however is mainly not used outside of testing
        wk = Pieces('WK', 'a1', 'WHITE', 'KING')
        self.add_piece(wk, wk.get_location())
        wr = Pieces('WR', 'a2', 'WHITE', 'ROOK')
        self.add_piece(wr, wr.get_location())
        wb1 = Pieces('WB', 'b1', 'WHITE', 'BISHOP')
        self.add_piece(wb1, wb1.get_location())
        wb2 = Pieces('WB', 'b2', 'WHITE', 'BISHOP')
        self.add_piece(wb2, wb2.get_location())
        wn1 = Pieces('WN', 'c1', 'WHITE', 'KNIGHT')
        self.add_piece(wn1, wn1.get_location())
        wn2 = Pieces('WN', 'c2', 'WHITE', 'KNIGHT')
        self.add_piece(wn2, wn2.get_location())
        bk = Pieces('BK', 'h1', 'BLACK', 'KING')
        self.add_piece(bk, bk.get_location())
        br = Pieces('BR', 'h2', 'BLACK', 'ROOK')
        self.add_piece(br, br.get_location())
        bb1 = Pieces('BB', 'g1', 'BLACK', 'BISHOP')
        self.add_piece(bb1, bb1.get_location())
        bb2 = Pieces('BB', 'g2', 'BLACK', 'BISHOP')
        self.add_piece(bb2, bb2.get_location())
        bn1 = Pieces('BN', 'f1', 'BLACK', 'KNIGHT')
        self.add_piece(bn1, bn1.get_location())
        bn2 = Pieces('BN', 'f2', 'BLACK', 'KNIGHT')
        self.add_piece(bn2, bn2.get_location())

    def get_board(
            self):  # prints the board to the console. used mainly for testing. pieces on the board are the objects, so the names are not intuitive.
        """method for printing the current game board to show where the pieces are"""
        print("")
        for each in self._board:
            print(each)
        return ""

    def get_game_state(self):  # simple method for returning the current game state.
        """method for returning the current state of the game. Options are 'UNFINISHED', 'WHITE_WON', 'BLACK_WON', or 'TIE'"""
        return self._game_state

    def make_move(self, old_space,
                  new_space):  # this is the big one. most of the magic happens here, but there is some magic in other places that's just called from here.
        """method for moving a chess piece from one space on the board to another"""
        old = None
        new = None
        if self._game_state != 'UNFINISHED':  # first thing it checks is if the game is finished. if it's over, obviously no more moves can be made.
            return False
        for row in self._board:
            for space in row:
                if new_space in space:
                    new = space
        for row in self._board:
            for space in row:  # THE FOLLOWING COMMENTS EXPLAIN THE METHOD FOR THE KING, REPLACE KING WITH WHATEVER PIECE FOR THE REST OF IT. IT WORKS THE SAME WAY LOGICALLY
                if old_space in space:
                    old = space
        if len(old) == 1:  # checks that the space the user is trying to move a piece from actually contains a piece. if there's no piece there, a move can't be made
            return False
        elif old[
            1].get_color() != self._turn:  # checks the color of the piece against whose turn it is. if they don't match, returns false. you can't play with other people's pieces
            return False
        elif old[
            1].get_type() == 'KING':  # checks if the piece is a king, if so, calls the king_moves method to see if the player is attempting a valid move
            if self.king_moves(old_space, new_space):
                if len(new) > 1:  # checks if the destination already contains a piece, and then if the piece belongs to the same player. you can't capture yourself
                    if new[1].get_color() == self._turn:
                        return False
                    else:  # if it's an opponent piece, the capture is allowed and things are updated accordingly. pieces are moved, pieces are removed, etc...
                        temp = new[1]
                        self._captured.append(temp.get_name())
                        new.remove(new[1])
                        new.append(old[1])
                        old.remove(old[1])
                        self.update_turn()  # if the move/capture was valid, the game turn is updated to the next player
                        if self.king_in_check():  # once things are updated the king_in_check method is called to see if the move would cause either of the kings to be in check. if so the move is undone and the method returns false
                            self._captured.remove(temp.get_name())
                            new.append(temp)
                            old.append(new[1])
                            new.remove(new[1])
                            self.update_turn()  # if the move had put a king in check and is no longer valid, the turn tracker is reverted back to the original players turn, so they can try again
                            return False
                        else:
                            if self._turn == 'WHITE':  # at the end of BLACK's turn, the turn tracker will be changed to WHITE. so at this point at the end of BLACK's turn it will say WHITE. if it says white, the game state is updated as both players have moved the same number of times
                                self.update_game_state()
                            return True  # if everything has been valid up to this point the method returns true and the pieces will be in there new location
                if len(new) == 1:  # basically the same as above, except there was no piece to capture and the player's piece could just move there slightly more simply
                    new.append(old[1])
                    old.remove(old[1])
                    self.update_turn()
                    if self.king_in_check():
                        old.append(new[1])
                        new.remove(new[1])
                        self.update_turn()
                        return False
                    else:
                        if self._turn == 'WHITE':
                            self.update_game_state()
                        return True
            else:
                return False
        elif old[1].get_type() == 'ROOK':  # read all the comments for king, but replace king with rook in your mind
            if self.rook_moves(old_space, new_space):
                if len(new) > 1:
                    if new[1].get_color() == 'BLACK' and self._turn == 'BLACK':
                        return False
                    if new[1].get_color() == 'WHITE' and self._turn == 'WHITE':
                        return False
                    else:
                        temp = new[1]
                        self._captured.append(temp.get_name())
                        new.remove(new[1])
                        new.append(old[1])
                        old.remove(old[1])
                        self.update_turn()
                        if self.king_in_check():
                            self._captured.remove(temp.get_name())
                            new.append(temp)
                            old.append(new[1])
                            new.remove(new[1])
                            self.update_turn()
                            return False
                        else:
                            if self._turn == 'WHITE':
                                self.update_game_state()
                            return True
                if len(new) == 1:
                    new.append(old[1])
                    old.remove(old[1])
                    self.update_turn()
                    if self.king_in_check():
                        old.append(new[1])
                        new.remove(new[1])
                        self.update_turn()
                        return False
                    else:
                        if self._turn == 'WHITE':
                            self.update_game_state()
                        return True
            else:
                return False
        elif old[1].get_type() == 'BISHOP':  # read all the comments for king, but replace king with bishop in your mind
            if self.bishop_moves(old_space, new_space):
                if len(new) > 1:
                    if new[1].get_color() == 'BLACK' and self._turn == 'BLACK':
                        return False
                    if new[1].get_color() == 'WHITE' and self._turn == 'WHITE':
                        return False
                    else:
                        temp = new[1]
                        self._captured.append(temp.get_name())
                        new.remove(new[1])
                        new.append(old[1])
                        old.remove(old[1])
                        self.update_turn()
                        if self.king_in_check():
                            self._captured.remove(temp.get_name())
                            new.append(temp)
                            old.append(new[1])
                            new.remove(new[1])
                            self.update_turn()
                            return False
                        else:
                            if self._turn == 'WHITE':
                                self.update_game_state()
                            return True
                if len(new) == 1:
                    new.append(old[1])
                    old.remove(old[1])
                    self.update_turn()
                    if self.king_in_check():
                        old.append(new[1])
                        new.remove(new[1])
                        self.update_turn()
                        return False
                    else:
                        if self._turn == 'WHITE':
                            self.update_game_state()
                        return True
            else:
                return False
        elif old[1].get_type() == 'KNIGHT':  # read all the comments for king, but replace king with knight in your mind
            if self.knight_moves(old_space, new_space):
                if len(new) > 1:
                    if new[1].get_color() == 'BLACK' and self._turn == 'BLACK':
                        return False
                    if new[1].get_color() == 'WHITE' and self._turn == 'WHITE':
                        return False
                    else:
                        temp = new[1]
                        self._captured.append(temp.get_name())
                        new.remove(new[1])
                        new.append(old[1])
                        old.remove(old[1])
                        self.update_turn()
                        if self.king_in_check():
                            self._captured.remove(temp.get_name())
                            new.append(temp)
                            old.append(new[1])
                            new.remove(new[1])
                            self.update_turn()
                            return False
                        else:
                            if self._turn == 'WHITE':
                                self.update_game_state()
                            return True
                if len(new) == 1:
                    new.append(old[1])
                    old.remove(old[1])
                    self.update_turn()
                    if self.king_in_check():
                        old.append(new[1])
                        new.remove(new[1])
                        self.update_turn()
                        return False
                    else:
                        if self._turn == 'WHITE':
                            self.update_game_state()
                        return True
            else:
                return False

    def add_piece(self, piece,
                  space):  # method for adding a piece to the game board. only used in the initialization of the game
        """method for adding a piece to a board space"""
        for row in self._board:
            for position in row:
                if space in position:
                    position.append(piece)
                    return

    def capture_piece(self, space,
                      piece):  # method for placing a piece that was captured into the captured list, they could be just deleted, but I made this just to help keep track of everything during testing
        """method for capturing pieces"""
        for row in self._board:
            for each in row:
                if space in each:
                    each.remove(piece())
                    self._captured.append(piece)
                    return
                else:
                    return

    def king_moves(self, old,
                   new):  # called from the make_move method if the piece to be moved is a king. checks that the destination is consistent with the rules of chess for a kings moves
        """method for testing the validity of a move for a king, returns True or False"""  # one space in any direction from the king's current position
        old_row = None
        old_col = None
        new_row = None
        new_col = None
        for row in self._board:
            for each in row:
                if old in each:
                    old_col = row.index(each)
                    old_row = self._board.index(row)
        for row in self._board:
            for each in row:
                if new in each:
                    new_col = row.index(each)
                    new_row = self._board.index(row)
        if (old_row == new_row or old_row == new_row - 1 or old_row == new_row + 1) and (
                old_col == new_col or old_col == new_col - 1 or old_col == new_col + 1):
            if old_row == new_row and old_col == new_col:
                return False
            else:
                return True
        else:
            return False

    def rook_moves(self, old,
                   new):  # called from the make_move method if the piece to be moved is a rook. checks that the destination is consistent with the rules of chess for a rook's moves
        """method for testing the validity of a move for a rook"""  # in a straight line in any direction as long as it is not blocked
        old_row = None
        old_col = None
        new_row = None
        new_col = None
        for row in self._board:
            for each in row:
                if old in each:
                    old_col = row.index(each)
                    old_row = self._board.index(row)
        for row in self._board:
            for each in row:
                if new in each:
                    new_col = row.index(each)
                    new_row = self._board.index(row)
        if old_row == new_row or old_col == new_col:
            if old_row == new_row and old_col == new_col:
                return False
            elif old_row == new_row:
                if old_col < new_col:
                    for each in range(old_col + 1, new_col):
                        if len(self._board[old_row][each]) > 1:
                            return False
                    return True
                elif old_col > new_col:
                    for each in range(new_col + 1, old_col):
                        if len(self._board[old_row][each]) > 1:
                            return False
                    return True
            elif old_col == new_col:
                if old_row > new_row:
                    for each in range(new_row + 1, old_row):
                        if len(self._board[each][old_col]) > 1:
                            return False
                    return True
                if old_row < new_row:
                    for each in range(old_row + 1, new_row):
                        if len(self._board[each][old_col]) > 1:
                            return False
                    return True
        else:
            return False

    def bishop_moves(self, old,
                     new):  # called from the make_move method if the piece to be moved is a bishop. checks that the destination is consistent with the rules of chess for a bishop's moves
        """method for testing the validity of a move for a bishop"""  # in any of the diagonals off the current position
        old_row = None
        old_col = None
        new_row = None
        new_col = None
        old_alph = ord(old[
                           0]) - 96  # broke the alphanumeric identifier down and converted the alpha part to another numeric part. helps with math.
        old_num = int(old[1])
        new_alph = ord(new[0]) - 96
        new_num = int(new[1])
        for row in self._board:
            for each in row:
                if old in each:
                    old_col = row.index(each)
                    old_row = self._board.index(row)
        for row in self._board:
            for each in row:
                if new in each:
                    new_col = row.index(each)
                    new_row = self._board.index(row)
        if old_row == new_row or old_col == new_col:  # can't travel in a straight line, those spaces are all false
            return False
        elif old_alph > new_alph and old_num < new_num:  # broke directions down into four quadrants and did the math with the converted algebraic code to check the diagonals
            if abs(old_alph - new_alph) != abs(old_num - new_num):
                return False
            while old_row != new_row + 1 and old_col != new_col + 1:
                if len(self._board[old_row - 1][
                           old_col - 1]) > 1:  # if any of the spaces on its path that aren't the destination contain a piece, returns false
                    return False
                old_row -= 1
                old_col -= 1
            return True
        elif old_alph < new_alph and old_num < new_num:
            if abs(old_alph - new_alph) != abs(old_num - new_num):
                return False
            while old_row != new_row + 1 and old_col != new_col - 1:
                if len(self._board[old_row - 1][old_col + 1]) > 1:
                    return False
                old_row -= 1
                old_col += 1
            return True
        elif old_alph < new_alph and old_num > new_num:
            if abs(old_alph - new_alph) != abs(old_num - new_num):
                return False
            while old_row != new_row - 1 and old_col != new_col - 1:
                if len(self._board[old_row + 1][old_col + 1]) > 1:
                    return False
                old_row += 1
                old_col += 1
            return True
        elif old_alph > new_alph and old_num > new_num:
            if abs(old_alph - new_alph) != abs(old_num - new_num):
                return False
            while old_row != new_row - 1 and old_col != new_col + 1:
                if len(self._board[old_row + 1][old_col - 1]) > 1:
                    return False
                old_row += 1
                old_col -= 1
            return True

    def knight_moves(self, old,
                     new):  # called from the make_move method if the piece to be moved is a knight. checks that the destination is consistent with the rules of chess for a knight's moves
        """method for testing the validity of a move for a knight"""  # 2 spaces in one direction and then 1 space in a direction 90 degrees to the original direction
        old_alph = ord(old[0]) - 96
        old_num = int(old[1])
        new_alph = ord(new[
                           0]) - 96  # similar to the way I checked the bishop's path, just converted the code and did math ("just" as if it didn't take me hours)
        new_num = int(new[1])
        if new_num == old_num + 2:
            if new_alph == old_alph + 1 or new_alph == old_alph - 1:
                return True
            else:
                return False
        elif new_alph == old_alph + 2:
            if new_num == old_num + 1 or new_num == old_num - 1:
                return True
            else:
                return False
        elif new_num == old_num - 2:
            if new_alph == old_alph + 1 or new_alph == old_alph - 1:
                return True
            else:
                return False
        elif new_alph == old_alph - 2:
            if new_num == old_num + 1 or new_num == old_num - 1:
                return True
            else:
                return False
        else:
            return False

    def king_in_check(
            self):  # used after every valid move to see if either king would be left in check, if true the move is reverted.
        """method to determine if a king is in check."""
        for row in self._board:
            for space in row:
                if len(space) > 1:
                    if space[1].get_type() == 'KING':  # first determines where the kings currently are
                        for row2 in self._board:
                            for space2 in row2:
                                if len(space2) > 1:
                                    if space[1].get_color() != space2[
                                        1].get_color():  # then takes the location of every piece that doesn't belong to the king and attempts to move them into the king using the piece_moves methods and using the kings current location as the new and the opponent's location as the old
                                        if space2[
                                            1].get_type() == 'KING':  # if any of them come back true (meaning they could move to the king's location on the next turn) then the king is in check and the move is invalidated
                                            if self.king_moves(space2[0], space[0]):
                                                return True
                                        if space2[1].get_type() == 'ROOK':
                                            if self.rook_moves(space2[0], space[0]):
                                                return True
                                        if space2[1].get_type() == 'BISHOP':
                                            if self.bishop_moves(space2[0], space[0]):
                                                return True
                                        if space2[1].get_type() == 'KNIGHT':
                                            if self.knight_moves(space2[0], space[0]):
                                                return True

    def update_turn(
            self):  # used after every valid move to switch whose turn it is, allowing the next player to control their own pieces
        """method for updating whose turn it is (which pieces can be moved)"""
        if self._turn == 'WHITE':
            self._turn = 'BLACK'
        else:
            self._turn = 'WHITE'

    def update_game_state(
            self):  # used at the end of each BLACK turn to check the current game state before continuing the game.
        """method for updating the game state following BLACK turn"""
        kings_that_made_it = []
        for space in self._board[0]:
            if len(space) > 1:
                if space[1].get_type() == 'KING':
                    kings_that_made_it.append(space[1].get_color())
        if len(kings_that_made_it) == 0:
            return
        elif 'WHITE' in kings_that_made_it and 'BLACK' not in kings_that_made_it:
            self._game_state = 'WHITE_WON'
        elif 'WHITE' not in kings_that_made_it and 'BLACK' in kings_that_made_it:
            self._game_state = 'BLACK_WON'
        elif 'WHITE' in kings_that_made_it and 'BLACK' in kings_that_made_it:
            self._game_state = 'TIE'


class Pieces:  # class for the pieces, allows for four data members, location is only used in setting up the board and is subsequently only tracked within the game the piece is in. the rest are called at various times throughout the game
    """class to store the different pieces and how they move"""

    def __init__(self, name, location, color, type):
        """method for creating new pieces for a chess game"""
        self._name = name
        self._location = location
        self._color = color
        self._type = type

    def get_name(self):
        """method for retrieving the name of a piece"""
        return self._name

    def get_location(self):
        """method for returning the location of a piece"""
        return self._location

    def get_color(self):
        """method for returning color of piece"""
        return self._color

    def get_type(self):
        """method for returning type of piece"""
        return self._type
