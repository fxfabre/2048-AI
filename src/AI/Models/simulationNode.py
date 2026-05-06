class SimulationNode:
    def __init__(self):
        # TODO : ajouter gestion des game over, pénalisation scores ? ou critère pour apprentissage après.

        # score cumulatif sur tous les états fils obtenu si on move left ici.
        self.scoreLeft = [0]  # avoid empty list
        self.scoreRight = [0]  # avoid empty list
        self.scoreUp = [0]  # avoid empty list
        self.scoreDown = [0]  # avoid empty list

        # Sous arbres. Not used now
        self.nodeLeft = None
        self.nodeRight = None
        self.nodeUp = None
        self.nodeDown = None

        self.nbSimulations = 0

    def addScore(self, direction, score):
        # move : left, right, up or down
        # score : somme des scores obtenus dans tous les noeuds fils
        direction = direction.lower()

        if direction == "left":
            self.scoreLeft.append(score)
        elif direction == "right":
            self.scoreRight.append(score)
        elif direction == "up":
            self.scoreUp.append(score)
        elif direction == "down":
            self.scoreDown.append(score)
        else:
            raise Exception("Unknown direction : " + str(direction))

        self.nbSimulations += 1
        return self

    def initNode(self, move):
        if move == "left":
            if self.left is None:
                self.nodeLeft = SimulationNode()
        elif move == "down":
            if self.down is None:
                self.nodeDown = SimulationNode()
        elif move == "right":
            if self.right is None:
                self.nodeRight = SimulationNode()
        elif move == "up":
            if self.up is None:
                self.nodeUp = SimulationNode()
        else:
            raise Exception("Unknown direction")

    def display(self):
        print(f"#### Node : score = {sum(self.scores)}")
        print(f"{self.finished} / {self.finished + self.nbGameOver} succeeded")

        leftScore = (self.left and sum(self.left.scores)) or 0
        print(f"  Left  : {leftScore}")

        rightScore = (self.right and sum(self.right.scores)) or 0
        print(f"  Right : {rightScore}")

        upScore = (self.up and sum(self.up.scores)) or 0
        print(f"  Up    : {upScore}")

        downScore = (self.down and sum(self.down.scores)) or 0
        print(f"  Down  : {leftScore}")

    def getBestMove(self):
        return self.getMaxMove()

    def getMaxMove(self):
        """
        :return: move with the highest score
        """
        best_score = max(self.scoreLeft)
        best_move = "left"

        score = max(self.scoreRight)
        if score > best_score:
            best_score = score
            best_move = "right"

        score = max(self.scoreUp)
        if score > best_score:
            best_score = score
            best_move = "up"

        score = max(self.scoreDown)
        if score > best_score:
            # best_score = score
            best_move = "down"

        return best_move
