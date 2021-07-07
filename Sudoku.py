'''
How to play:
------------

Fill a 9x9 grid with numbers according to 3 strict rules:
    1. There is a 9x9 grid, each must be filled with a number ranging from 1–9
    2. You cannot have the same number in a single row or column
    3. You cannot have the same number in a 3x3 section

name                          = 'py-console-sudoku',
version                       = '1.0.0',
author                        = 'Erel Adoni',
author_email                  = 'ereladoni@gmail.com',
description                   = 'A Python Sudoku generator and solver',
url                           = 'https://github.com/jeffsieu/py-sudoku',
keywords                      = ['SUDOKU'], 
packages                      = ['sudoku'],
python_requires               = '>=2.7',
classifiers = [
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

'''

import time

def print_board(board): # prints a Sudoku board
    '''
    Parameters:
        board (2D list of integers): a Sudoku board
    '''
    for r in range(9):
        if r % 3 == 0 and r != 0: # every 3 rows
            print("------|-------|------") # divider
        for c in range(9):
            if c % 3 == 0 and c != 0: # every 3 columns
                print("| ", end="") # divider

            if c == 8:
                print(board[r][c], end="\n") # end of line
            else:
                print(str(board[r][c]) + " ", end="")

class SudokuBoardSolver:
    def __init__(self, board):
        self.board = board

    def locate_empty_cell(self): # finds the first empty cell on the board (represented by a 0)
        '''
        Parameters:
            self.board (2D list of integers): a Sudoku board
        
        Returns:
            if found - a tuple of 'row' and 'col',
            else False
        '''
        
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return False

    def is_option_valid(self, num, cell): # checks whether a number can be fit into a specific cell (row, col)
        '''
        Parameters:
            num (int):                        the number that is trying to be entered in a cell
            cell (tuple):                     a row and column index

        Returns:
            False for an invalid option,
            True for a valid option
        '''

        for col in self.board[cell[0]]: # checks whether the number is already in current row
            if col == num:
                return False

        for row in range(9): # checks whether the number is already in current column
            if self.board[row][cell[1]] == num:
                return False

        _3x3_section_row = cell[0] // 3
        _3x3_section_col = cell[1] // 3

        for i in range(3): # checks whether the number is already in current 3x3 section
            for k in range(3):
                if self.board[i + (_3x3_section_row * 3)][k + (_3x3_section_col * 3)] == num:
                    return False
        
        return True

    def solve_board(self): # solves a Sudoku board using recursion
        '''
        Parameters:
            None.

        Returns:
            A solved Sudoku board
        '''
        start = time.time() # start a timer
        
        self.__solver()
        
        print( "solved in {} seconds".format( time.time() - start ) + "\n")

    def __solver(self):

        next_cell_to_solve = self.locate_empty_cell()

        if not next_cell_to_solve:
            return True
        else:
            row, col = next_cell_to_solve

        for num in range(1, 10):
            if self.is_option_valid(num, (row, col)):
                self.board[row][col] = num
                
                # recursion
                if self.__solver():
                    return self.board
                
                self.board[row][col] = 0 # backtracking

        return False





from random import shuffle, randint

class SudokuBoardGenerator:

    def __init__(self):
        self.board = self.reset_board()

    def reset_board(self):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        return self.board

    def is_board_full(self): # checks whether the sudoku board is full
        '''
        Parameters:
            None.
        
        Returns:
            False if at least one cell has a value of 0, else True
        '''
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False

        return True

    def copy_board(self): # creates a copy of a Sudoku board
        '''
        Parameters:
            None.
        
        Returns:
            An exact copy of the original Sudoku board
        '''
        board_copy = []

        for row in range(9):
            board_copy.append([])

            for col in range(9):
                board_copy[row].append(self.board[row][col])
        
        return board_copy

    def generate_solved_board(self): # generates a solved (full) Sudoku board
        '''
        Parameters:
            None.

        Returns:
            A full solved Sudoku board
        '''

        numberList = list(range(1, 10))
    
        for cell_number in range(81): # loops through the entire board
            cell_row = cell_number // 9
            cell_col = cell_number % 9
            
            if self.board[cell_row][cell_col] == 0:
                shuffle(numberList) # makes it random

                for num in numberList:
                    if (not(num in self.board[cell_row]) and # checks whether the number is already in current row
                        not num in [r[cell_col] for r in self.board]): # checks whether the number is already in current column

                        _3x3_section_row = cell_row // 3
                        _3x3_section_col = cell_col // 3
                        can_use = True

                        for i in range(3): # checks whether the number is already in current 3x3 section
                            for k in range(3):
                                if self.board[i + (_3x3_section_row * 3)][k + (_3x3_section_col * 3)] == num:
                                    can_use = False
                                    break
                            else:
                                continue
                            break
                                                                
                        if can_use:
                            self.board[cell_row][cell_col] = num
                            
                            # recursion
                            if self.is_board_full():
                                return True
                            else:
                                if self.generate_solved_board():
                                    return True
                break
        
        self.board[cell_row][cell_col] = 0
    
    def count_solutions(self, board): # calculates all possible combinations of numbers until a solution is found
        '''
        Parameters:
            board (2D list of integers): a Sudoku board

        Returns:
            None
        '''
        global solutions

        numberList = list(range(1, 10))
    
        # finds the next empty cell
        for cell_number in range(81):
            cell_row = cell_number // 9
            cell_col = cell_number % 9
            
            if board[cell_row][cell_col] == 0:
                
                for num in numberList:
                    if (not(num in self.board[cell_row]) and # checks whether the number is already in current row
                        not num in [r[cell_col] for r in self.board]): # checks whether the number is already in current column

                        _3x3_section_row = cell_row // 3
                        _3x3_section_col = cell_col // 3
                        can_use = True # if the number does not already appear in the row/column/3x3 section

                        for i in range(3): # checks whether the number is already in current 3x3 section
                            for k in range(3):
                                if self.board[i + (_3x3_section_row * 3)][k + (_3x3_section_col * 3)] == num:
                                    can_use = False
                                    break
                            else:
                                continue
                            break

                        if can_use:
                            board[cell_row][cell_col] = num
                            
                            # recursion
                            if self.is_board_full():
                                solutions += 1
                                break
                            else:
                                if self.count_solutions(self.board):
                                    return True
                break
        self.board[cell_row][cell_col] = 0 # backtracking

    def generate_unsolved_board(self, difficulty): # removes numbers from the Sudoku board which has only one solution, one by one
        '''
        Parameters:
            difficulty (int): amount of attempts to remove more numbers from the board

        Returns:
            None
        '''
        print("Generating a new Sudoku board to solve...")
        
        start = time.time() # start a timer
        
        self.generate_solved_board()

        global solutions
        attempts = difficulty * 3 # a higher number of attempts will result in more numbers being removed from the board
        
        while attempts > 0:
            # selects a random cell that is not already empty
            row = randint(0,8)
            col = randint(0,8)
            while self.board[row][col] == 0:
                row = randint(0,8)
                col = randint(0,8)
            
            cell_backup = self.board[row][col] # backup its cell value in case the number of solution(s) is different from 1
            self.board[row][col] = 0
            
            board_copy = self.copy_board() # take a full copy of the board after the removal

            solutions = 0 # resets the number of solutions that this board has (using backtracking, implemented in 'count_solutions')
            self.count_solutions(board_copy) 

            if solutions != 1: # removes the change if the number of solution(s) is not 1.
                self.board[row][col] = cell_backup
                attempts -= 1 # not a must: checks if it is possible to remove more numbers using another cell
        
        print( "generated a new board in {} seconds".format( time.time() - start ) + "\n")