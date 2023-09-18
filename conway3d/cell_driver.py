# from abc import ABC, abstractmethod
# from enum import Enum
# from typing import Generic, TypeVar
#
# T_CELL_STATE = TypeVar('T_CELL_STATE', bound=Enum)
#
#
# class CellDriver(ABC, Generic[T_CELL_STATE]):
#     @abstractmethod
#     def default_state(self) -> T_CELL_STATE:
#         """The default state value to initialize cell populations with.
#         """
#
#     @abstractmethod
#     def next_state(self, state: T_CELL_STATE, **kwargs) -> T_CELL_STATE:
#         """Determines the next state for a cell.
#
#         Args:
#             state: the current state of the cell
#             **kwargs: any other arguments the implementation needs to
#                 determine the next state.
#
#         Returns:
#             The next state for the cell.
#         """
