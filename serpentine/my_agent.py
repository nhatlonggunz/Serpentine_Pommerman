import random
import numpy as np

from serpentine.directions import Directions, Direction

from pommerman import characters
from pommerman.constants import Action, Item
from pommerman.agents import BaseAgent


class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)
        self.queue = []

    @staticmethod
    def is_passage_cell(board: np.array, position: tuple) -> bool:
        row, col = position

        if row < 0 or row > board.shape[0] or col < 0 or col > board.shape[0]:
            return False
        if board[position] != Item.Passage.value:
            return False
        return True

    def create_path(self, board: np.array, my_location: tuple, goal_location: tuple) -> list:
        """ BFS to a goal location.  Returns True if it can be reached."""
        to_visit = [my_location]
        visited = []

        came_from = dict()
        came_from[my_location] = None

        came_from_direction = dict()
        came_from_direction[my_location] = Directions.ZERO

        while to_visit:
            point = to_visit.pop(0)
            visited.append(point)

            # Check if we have found the location
            if point == goal_location:
                break

            for direction in Directions.NEIGHBOURS:
                # By making it a numpy array we can add the values
                new_point = tuple(np.array(point) + direction.array)

                if self.is_passage_cell(board, new_point) and new_point not in visited:
                    to_visit.append(new_point)
                    came_from[new_point] = point
                    came_from_direction[new_point] = direction

        return self.trace_path(came_from, came_from_direction, goal_location)

    def trace_path(self, came_from: dict, came_from_direction: dict, goal_location: tuple) -> list:
        """ Returns a list of directions from a start node with the parent None, leading to the goal node.  """
        current = goal_location
        parent = came_from.get(goal_location, None)
        path = []

        while parent is not None:
            path.append(came_from_direction[current])
            current, parent = parent, came_from.get(parent, None)
        return list(reversed(path))

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        if not self.queue:
            my_location = obs['position']
            board = obs['board']

            print(board)
            print(self.create_path(board, my_location, (3, 1)))

            if self.create_path(board, my_location, (2, 2)):
                print("sure")

            for i in range(100):
                self.queue.append(random.choice(list(Action)))

        return self.queue.pop()
