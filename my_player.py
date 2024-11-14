# 2230323 Garnier Guilhem
# 2312403 Marc Zhang
from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError


class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float = 60*15, *args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name, time_limit, *args)

    def eval_state(self, state):
        return 0

    def manhattanDist(self, A, B):
        mask1 = [(0, 2), (1, 3), (2, 4)]
        mask2 = [(0, 4)]
        diff = (abs(B[0] - A[0]), abs(B[1] - A[1]))
        dist = (abs(B[0] - A[0]) + abs(B[1] - A[1]))/2
        if diff in mask1:
            dist += 1
        if diff in mask2:
            dist += 2
        return dist

    def compute_score(self, state, player_id, enemy_id):
        # Returns a player score where the higher score is the winning player
        rep = state.get_rep()
        env = rep.get_env()
        dim = rep.get_dimensions()
        center = (dim[0]//2, dim[1]//2)
        dist = 0
        for i, j in list(env.keys()):
            p = env.get((i, j), None)
            if p.get_owner_id() == player_id:
                dist += self.manhattanDist(center, (i, j))
            elif p.get_owner_id() == enemy_id:
                dist - + self.manhattanDist(center, (i, j))
        return state.get_scores()[player_id]-state.get_scores()[enemy_id] - dist/1000

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        player_id = current_state.get_next_player().get_id()
        for p in current_state.get_players():
            if p.get_id() != player_id:
                enemy_id = p.get_id()
        # Allow more computing for last steps
        if current_state.get_step() < 10:
            max_depth = 1
        elif current_state.get_step() < 42:
            max_depth = 2
        else:
            max_depth = 4

        def max_value(state, alpha, beta, depth):
            if state.is_done() or depth > max_depth:
                return self.compute_score(state, player_id, enemy_id), None

            v, move = -float('inf'), None
            filtered_actions = [self.compute_score(a.get_next_game_state(
            ), player_id, enemy_id) for a in state.get_possible_actions()]
            max_score = max(filtered_actions)
            filtered_actions = [a for a in state.get_possible_actions()
                                if self.compute_score(a.get_next_game_state(), player_id, enemy_id) >= max_score-0.8]
            for a in filtered_actions:
                v2, _ = min_value(a.get_next_game_state(),
                                  alpha, beta, depth+1)
                if v2 > v:
                    v, move = v2, a
                    alpha = max(alpha, v)
                if v >= beta:
                    return v, move
            return v, move

        def min_value(state, alpha, beta, depth):
            if state.is_done() or depth > max_depth:
                return self.compute_score(state, player_id, enemy_id), None
            v, move = float('inf'), None
            for a in state.get_possible_actions():
                v2, _ = max_value(a.get_next_game_state(),
                                  alpha, beta, depth+1)
                if v2 < v:
                    v, move = v2, a
                    beta = min(beta, v)
                if v <= alpha:
                    return v, move
            return v, move

        move = max_value(current_state, -float('inf'), +float('inf'), 0)[1]
        return move
