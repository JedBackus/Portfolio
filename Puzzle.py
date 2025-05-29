import copy


def solve_puzzle(Board, Source, Destination):
    """
    A function for finding the shortest path in a puzzle, from a random starting position to a random destination. The
    puzzle is passed to the function in the form of a list of lists, with each position in the puzzle being represented
    by either a '_' showing that it is an available space, or a '#' showing that the space is blocked. The function uses
    backtracking to find all paths (if there are any) to the destination, and then returns a list of spaces used to
    follow the shortest path along with the directions moved.

        Input: board, source, destination.
        board = [
                ['-', '-', '-', '-', '-'],
                ['-', '-', '#', '-', '-'],
                ['-', '-', '-', '-', '-'],
                ['#', '-', '#', '#', '-'],
                ['-', '#', '-', '-', '-']
                ]
        source: A tuple representing the indices of the starting position, e.g. for the upper right corner,
                    source=(0, 4).
        destination: A tuple representing the indices of the goal position, e.g. for the lower right corner,
                    goal=(4, 4).

        Output: A list of tuples representing the indices of each position in the path. The first tuple should be the
        starting position, or source, and the last tuple should be the destination. If there is no valid path, None
        should be returned. Not an empty list, but the None object. If source and destination are same return the same
        cell.


    :param Board:           The puzzle passed as a list of lists
    :param Source:          The starting position in the form of an (x, y) coordinate
    :param Destination:     The destination in the form of an (x, y) coordinate
    :return:                A list containing the (x, y) coordinates of spaces in the path used and a string of
                            directions moved

    """
    # final variable is initialized to None, if no path is found the None object is returned
    final = None
    # the visited list is used to ensure that the path does not loop into itself
    visited = []
    # the path variable is used as a stack. The source position is initialized to it as a starting point, the number
    # following the source coordinate indicates the direction for the algorythm to attempt (0 = Up, 1 = Right,
    # 2 = Down, 3 = Left, 4 = all paths have been tried)
    path = [(Source, 0)]
    # the guide variable will hold the string containing the moves used, the fin_guide variable will be the shortest
    # path used
    guide = ''
    fin_guide = ''
    # the while loop is based on the stack, ensuring that all possible paths are explored
    while len(path) > 0:
        # the top of the stack is popped, and the coordinate saved as the loc with the number saved as the direction
        loc, dir = path.pop()
        # immediately the same space is placed back on the stack, but the direction indicator is incremented
        path.append((loc, dir + 1))
        # if the space has not been visited on the current path it is added to the visited list
        if loc not in visited:
            visited.append(loc)
        # if the space is the destination, the path to the destination is saved. if it's not the first path,
        # the shortest is saved
        if loc == Destination:
            if not final or len(path) < len(final):
                final = []
                for i in path:
                    final.append(i[0])
                fin_guide = copy.deepcopy(guide)
        # for each space, each direction of travel is attempted, if it is an open space the path continues along it
        if dir == 0:
            if is_valid(move_up(loc), Board) and move_up(loc) not in visited:
                path.append((move_up(loc), 0))
                guide = guide + 'U'
        elif dir == 1:
            if is_valid(move_right(loc), Board) and move_right(loc) not in visited:
                path.append((move_right(loc), 0))
                guide = guide + 'R'
        elif dir == 2:
            if is_valid(move_down(loc), Board) and move_down(loc) not in visited:
                path.append((move_down(loc), 0))
                guide = guide + 'D'
        elif dir == 3:
            if is_valid(move_left(loc), Board) and move_left(loc) not in visited:
                path.append((move_left(loc), 0))
                guide = guide + 'L'
        # once all directions have been attempted, the space is taken off the stack and the visited list,
        # creating the backtracking
        else:
            visited.pop()
            path.pop()
            guide = guide[:-1]
    # once all paths have been attempted, the final path is returned along with the string containing the moves
    return final, fin_guide


def is_valid(pos, board):
    """
    A function to help the Puzzle function determine if an attempted move will be valid. A valid move is one that is
    within the bounds of the puzzle, and the space does not contain a '#' indicating a wall.

    :param pos:         The (x, y) coordinate of the space the Puzzle function is attempting to move
    :param board:       The puzzle from the Puzzle function, used to determine if the space is open or has a wall
    :return:            Returns True if the space is valid or False if it is not
    """
    if 0 <= pos[0] < len(board) and 0 <= pos[1] < len(board[0]) and board[pos[0]][pos[1]] != '#':
        return True
    else:
        return False


def move_down(source):
    """
    A function to help the Puzzle function move along a path. Moves the passed position down one space.

    :param source:      The (x, y) coordinate of the position the Puzzle function is moving from
    :return:            The (x, y) coordinate of the position the Puzzle function is moving to
    """
    source = (source[0] + 1, source[1])
    return source


def move_up(source):
    """
    A function to help the Puzzle function move along a path. Moves the passed position up one space.

    :param source:      The (x, y) coordinate of the position the Puzzle function is moving from
    :return:            The (x, y) coordinate of the position the Puzzle function is moving to
    """
    source = (source[0] - 1, source[1])
    return source


def move_right(source):
    """
    A function to help the Puzzle function move along a path. Moves the passed position right one space.

    :param source:      The (x, y) coordinate of the position the Puzzle function is moving from
    :return:            The (x, y) coordinate of the position the Puzzle function is moving to
    """
    source = (source[0], source[1] + 1)
    return source


def move_left(source):
    """
    A function to help the Puzzle function move along a path. Moves the passed position left one space.

    :param source:      The (x, y) coordinate of the position the Puzzle function is moving from
    :return:            The (x, y) coordinate of the position the Puzzle function is moving to
    """
    source = (source[0], source[1] - 1)
    return source


# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    Puzzle =    [
                ['-', '-', '-', '-', '-'],
                ['-', '-', '#', '-', '-'],
                ['-', '-', '-', '-', '-'],
                ['#', '-', '#', '#', '-'],
                ['-', '#', '-', '-', '-']
                ]

    test1 = solve_puzzle(Puzzle, (0, 2), (2, 2))
    test2 = solve_puzzle(Puzzle, (0, 0), (4, 4))
    test3 = solve_puzzle(Puzzle, (0, 0), (4, 0))
    test4 = solve_puzzle(Puzzle, (0, 0), (0, 0))

    print(test1)
    print(test2)
    print(test3)
    print(test4)
