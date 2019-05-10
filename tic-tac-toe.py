EMPTY_MARK = '_'
O_MARK = 'o'
X_MARK = 'x'
CENTER = (1,1)
CORNERS = ((0,0),(0,2),(2,2),(2,0))

def best_play(board_state, mark_in_play):
	return max(possible_plays(board_state, mark_in_play), key=lambda play: play[1])

def possible_plays(board_state, mark_in_play):
	return [(possible_next_board_state,
             play_score(possible_next_board_state,
                        played_position))
            for possible_next_board_state, played_position
            in possible_following_board_states(board_state,
                                               mark_in_play)]

def possible_following_board_states(board_state, mark_in_play):
    return [(board_state_after_marking(board_state,
                                       empty_position,
                                       mark_in_play),
             empty_position)
            for empty_position in empty_positions(board_state)]

def board_state_after_marking(board_state, position_to_mark, mark):
	return [[board_state[row][col] if (row, col) != position_to_mark else mark
             for col in range(len(board_state[row]))]
            for row in range(len(board_state))]

def play_score(board_state, played_position):
    line_patterns = adjacent_marks(board_state, played_position)
    mark_to_check = position_mark(board_state, played_position)
    two_in_line = amount_of_two_in_line(line_patterns, mark_to_check)
    two_in_line_blocked = amount_of_two_in_line_blocked(line_patterns, mark_to_check)
    return 1000*winning_play(line_patterns, mark_to_check) \
    + 600*blocking_play(line_patterns, mark_to_check) \
    + 90*(two_in_line if two_in_line >= 2 else 0) \
    + 80*(two_in_line_blocked if two_in_line_blocked >=2 else 0)\
    + 110*(played_position==CENTER) \
    + (played_position in CORNERS)

def adjacent_marks(board_state, interceptor_position):
    return [[mark for position, mark in line
             if not position == interceptor_position]
            for line in board_lines(board_state)
            if interceptor_position
            in [position for position, __ in line]]

def board_lines(board_state):
    return [*board_rows(board_state),
    *board_columns(board_state),
    *board_diagonals(board_state)]

def board_rows(board_state):
    return [[((col, row), board_state[col][row])
          for row in range(len(board_state))]
         for col in range(len(board_state))]

def board_columns(board_state):
	return [[((row, col), board_state[row][col])
          for row in range(len(board_state))]
         for col in range(len(board_state))]

def board_diagonals(board_state):
	return [first_diagonal(board_state), second_diagonal(board_state)]

def first_diagonal(board_state):
	return [((i, i), board_state[i][i]) for i in range(len(board_state))]

def second_diagonal(board_state):
	return [((i, j), board_state[i][j]) for i, j
            in zip(range(len(board_state)), reversed(range(len(board_state))))]

def position_mark(board_state, position):
    return board_state[position[0]][position[1]]

def winning_play(line_patterns, mark_to_check):
    return any([all([mark_to_check == mark for mark in line_pattern])
                for line_pattern in line_patterns])

def blocking_play(line_patterns, mark_to_check):
    return winning_play(line_patterns, opposite_mark(mark_to_check))

def opposite_mark(mark):
    return O_MARK if mark == X_MARK else X_MARK

def amount_of_two_in_line(line_patterns, mark_to_check):
    return sum([two_in_line(line_pattern, mark_to_check)
                for line_pattern in line_patterns])

def two_in_line(line_pattern, mark_to_check):
    return mark_to_check in line_pattern and None in line_pattern

def amount_of_two_in_line_blocked(line_patterns, mark_to_check):
    return amount_of_two_in_line(line_patterns, opposite_mark(mark_to_check))

def opposite_corner(corner):
    row, col = corner
    return (2 if row == 0 else 0, 2 if col == 0 else 0)

def empty_positions(board_state):
	return [(row, col) for row in range(len(board_state))
         for col in range(len(board_state[row]))
                          if not board_state[row][col]]

def play_to_string(play):
    board_state, score = play
    aux = board_state_to_string(board_state)
    aux += '=======\nscore: '+str(score)
    return aux

def board_state_to_string(board_state):
    aux = ""
    for row in range(len(board_state)):
        aux += "|"
        for col in range(len(board_state[row])):
            aux += (board_state[row][col] or EMPTY_MARK) + "|"
        aux += '\n'
    return aux;

def initial_board_state():
    return [[input((row, col)) for col in range(3)] for row in range(3)]

board_state = initial_board_state()
print(board_state_to_string(board_state))
print(play_to_string(best_play(board_state, input('Mark: '))))
