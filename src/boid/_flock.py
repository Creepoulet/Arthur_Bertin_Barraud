from ._predator import Predator
from ._bird import Bird


class Flock:

    def show_flock(self): ...

    def move_flock(self): ...

    def __init__(self) -> None:
        print("In Flock")
