class Player:

    def __init__(self, type: str, mark: str, color: tuple):
        self.type = type
        self.mark = mark
        self.color = color
        self.score = 0

    def __str__(self):
        return self.mark
