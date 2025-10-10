from ._flyer import Flyer


class Bird(Flyer):

    def move_flyer(self) -> None: ...

    def __init__(self) -> None:
        super().__init__()
        print("In Bird")
