"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    ###return float(own_moves - opp_moves) #70.00% #61.43%
    ###return float(1/(opp_moves+1)+own_moves) #64.29%
    ###return float(own_moves^2 - opp_moves^2)
    return (own_moves-(0.1+game.height*game.height-len(game.get_blank_spaces()))*opp_moves) / (len(game.get_blank_spaces())+own_moves-opp_moves)


class CustomPlayer:

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=60.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left): 
        self.time_left = time_left

        if len(legal_moves) == 0:
            return (-1, -1)

        best_move = (-1, -1)
        depth = 1

        try:
            if self.iterative is False:
                d = self.search_depth #
                strategy = self.minimax if self.method == "minimax" else self.alphabeta
                _, best_mov = strategy(game.copy(), d)
                return best_mov      #
            else: 
                while True:
                    strategy = self.minimax if self.method == "minimax" else self.alphabeta
                    _, best_move = strategy(game.copy(), depth)
                    depth = depth + 1

        except Timeout:
            return best_move


    def minimax(self, game, depth, maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        scorez = float("-inf") if maximizing_player else float("inf")
        best_mov = (-1, -1)

        if depth == 1:
            for m in game.get_legal_moves():
                score = self.score(game.forecast_move(m), game.inactive_player if not maximizing_player else game.active_player)
                if (maximizing_player and score > scorez) or ((not maximizing_player) and score < scorez):
                    scorez, best_mov = score, m

        if depth > 1:
            for m in game.get_legal_moves():
                new = game.forecast_move(m)
                s, _ = self.minimax(new, depth - 1, not maximizing_player)
                if (maximizing_player and s > scorez) or ((not maximizing_player) and s < scorez):
                    scorez, best_mov = s, m
        elif depth == 0:
            scorez = self.score(game, game.inactive_player if not maximizing_player else game.active_player)
        return scorez, best_mov


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        Returns
        ----------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        bestest = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)

        if depth > 0:
            for move in game.get_legal_moves():
                new_state = game.forecast_move(move)
                s = self.alphabeta(new_state, depth - 1, alpha, beta, not maximizing_player)[0]

                if maximizing_player:

                    if s > bestest:
                        bestest = s
                        best_move = move

                    if bestest > alpha:
                        alpha = bestest

                    if bestest >= beta:
                        return bestest, best_move

                elif not maximizing_player:

                    if s < bestest:

                        bestest = s
                        best_move = move

                    if bestest <= alpha:
                        return bestest, best_move

                    if bestest < beta:
                        beta = bestest

        elif depth == 0:
            bestest = self.score(game, game.inactive_player if not maximizing_player else game.active_player)
        return bestest, best_move

