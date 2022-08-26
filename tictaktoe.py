#!/usr/bin/env python3

import copy
import sys
import pygame
import numpy as np
import random

from constants import *

# GAME
pygame.init()

# SO THIS ONE IS OUR SCREEN OR THE PLAYING AREA
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
pygame.display.set_caption('Tic Tac toe')
screen.fill(BG_COLOR)

class Board():
	def __init__(self):
		# this represents a 3x3 board of empty boxes
		self.squares = np.zeros((ROWS,COLS))
		self.empty_sqrs = self.squares
		self.marked_sqrs = 0
		
	def final_state(self,show = False):
		
		# vertical wins
		for col in range(COLS):
			if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
				if show:
					color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
					iPos = (col * SQ_SIZE + SQ_SIZE // 2, 20)
					fPos = (col * SQ_SIZE + SQ_SIZE // 2, HEIGHT - 20)
					pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
				return self.squares[0][col] # this will provide player numbers
		
		# horizontal wins
		for row in range(ROWS):
			if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
				if show:
					color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
					iPos = (20, row * SQ_SIZE + SQ_SIZE // 2)
					fPos = (WIDTH - 20, row * SQ_SIZE + SQ_SIZE // 2)
					pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
				return self.squares[row][0] # this will provide player numbers
			
			
		# diangonal left - right win
		if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
			if show:
				color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
				iPos = (20, 20)
				fPos = (WIDTH - 20, HEIGHT - 20)
				pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
			return self.squares[1][1]
		
		
		# diagonal right - left win
		if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
			if show:
				color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
				iPos = (20, HEIGHT - 20)
				fPos = (WIDTH - 20, 20)
				pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
			return self.squares[1][1]
		
		# no win yet
		return 0
		
	def mark_sqr(self,row,col,player):
		self.squares[row][col] = player
		self.marked_sqrs += 1
		
	def empty_sqr(self,row,col):
		return self.squares[row][col] ==0
	
	def get_empty_sqrs(self):
		empty_sqrs = []
		for row in range(ROWS):
			for col in range(COLS):
				if self.empty_sqr(row, col):
					empty_sqrs.append((row,col))
					
		return empty_sqrs
	
	def isFull(self):
		return self.marked_sqrs ==9
	
	def isempty(self):
		return self.marked_sqrs ==0


class AI():
	def __init__(self,level=1, player=2):
		self.level = level
		self.player = player
	
	def rnd(self,board):
		empty_sqrs = board.get_empty_sqrs()
		idx = random.randrange(0 ,len(empty_sqrs) )
		
		return empty_sqrs[idx]
	
	def minimax(self,board,maximizing):
		
		# terminal cases
		case = board.final_state()
		
		# p1 wins
		if case == 1:
			return 1, None
		
		# p2 wins
		if case ==2:
			return -1, None 
		
		# draw
		elif board.isFull():
			return 0, None
		
		if maximizing:
			max_eval = -100
			
			best_move = None 
			empty_sqrs = board.get_empty_sqrs()
			
			for (row,col) in empty_sqrs:
				temp_board = copy.deepcopy(board)
				temp_board.mark_sqr(row,col,1)
				eval = self.minimax(temp_board, False)[0]
				
				if eval > max_eval:
					max_eval = eval
					best_move = (row,col)
					
			return max_eval , best_move
			
			
		elif not maximizing:
			max_eval = 100
			
			best_move = None 
			empty_sqrs = board.get_empty_sqrs()
			
			for (row,col) in empty_sqrs:
				temp_board = copy.deepcopy(board)
				temp_board.mark_sqr(row,col,self.player)
				eval = self.minimax(temp_board, True)[0]
				
				if eval < max_eval:
					max_eval = eval
					best_move = (row,col)
			
			return max_eval , best_move
				
		
		
	def eval(self,main_board):
		if self.level == 0:
			# random choices
			eval = 'random'
			move = self.rnd(main_board)
			
			
		else:
			# minmax algo choice
			eval,move = self.minimax(main_board,False)
		
		print(f'AI has chose to mark the sqr in pos {move} with an eval of {eval}')
		
		return move # (row,col)
		
class Game:
	def __init__(self):
		self.board = Board()
		self.ai = AI()
		self.player = 1
		self.gamemode = 'ai'
		self.running = True
		self.show_lines()
		
	
		
	def show_lines(self):
		
		screen.fill(BG_COLOR)
		
		#VERTICAL
		pygame.draw.line(screen,LINE_COLOR, (SQ_SIZE ,0) ,(SQ_SIZE,HEIGHT) , LINE_WIDTH)
		pygame.draw.line(screen,LINE_COLOR, (WIDTH-SQ_SIZE ,0) ,(WIDTH-SQ_SIZE,HEIGHT) , LINE_WIDTH)
		
		# HORIZNOTAL
		pygame.draw.line(screen,LINE_COLOR, (0,SQ_SIZE) ,(WIDTH,SQ_SIZE) , LINE_WIDTH)
		pygame.draw.line(screen,LINE_COLOR, (0,HEIGHT-SQ_SIZE) ,(WIDTH,HEIGHT-SQ_SIZE) , LINE_WIDTH)


	def draw_fig(self,row,col):
		if self.player ==1:
			# DESC LINE
			start_desc = (col * SQ_SIZE + OFFSET , row*SQ_SIZE + OFFSET)
			end_desc = (col * SQ_SIZE + SQ_SIZE-OFFSET , row*SQ_SIZE + SQ_SIZE-OFFSET)
			pygame.draw.line(screen,CROSS_COLOR, start_desc , end_desc , CROSS_WIDTH)
			
			# ASC LINE
			start_asc = (col * SQ_SIZE + OFFSET , row*SQ_SIZE + SQ_SIZE-OFFSET)
			end_asc = (col * SQ_SIZE + SQ_SIZE-OFFSET , row*SQ_SIZE + OFFSET)
			pygame.draw.line(screen,CROSS_COLOR, start_asc , end_asc , CROSS_WIDTH)
			
		elif self.player ==2:
			center = (col*SQ_SIZE + SQ_SIZE//2 , row*SQ_SIZE + SQ_SIZE//2 )
			pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)
			
			
	def make_move(self,row,col):
		self.board.mark_sqr(row, col, self.player)
		self.draw_fig(row,col)
		self.next_turn()

	def next_turn(self):
		self.player = self.player % 2 + 1
		
		
	def change_gamemode(self):
		
		self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
		
	def isover(self):
		return self.board.final_state(show=True) != 0 or self.board.isFull()
		
	def reset(self):
		self.__init__()
		
# entry point where file gonna execute
def main():
	
	#object
	game = Game()
	board = game.board
	ai = game.ai
	
	
	# main loop
	while True:
		
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.MOUSEBUTTONDOWN:
#				print(event.pos) # it will provide the coordinates where we are clicking the board
				pos = event.pos
				row = pos[1] // SQ_SIZE
				col = pos[0] // SQ_SIZE
				
				if board.empty_sqr(row, col) and game.running:
					game.make_move(row, col)
					
					if game.isover():
						game.running = False
					
					
			if event.type == pygame.KEYDOWN:
				# G - CCHANGE GAME MODE
				if event.key == pygame.K_g:
					game.change_gamemode()
					
				# reset game
				
				if event.key == pygame.K_r:
					game.reset()
					board = game.board
					ai = game.ai
					
				# 0 -random ai
				if event.key == pygame.K_0:
					ai.level = 0
					
				# 1 -impossible ai
				if event.key == pygame.K_1:
					ai.level = 1
				
		if game.gamemode == 'ai' and game.player == ai.player and game.running:
			# update screen
			pygame.display.update()
			
			# ai methods
			row,col = ai.eval(board)
			
			game.make_move(row, col)
			
			if game.isover():
				game.running = False
			
		
		pygame.display.update()
	
main()
	
	