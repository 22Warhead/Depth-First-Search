from fileinput import filename
from PIL import Image, ImageDraw
from usage import StackFrontier, Node
import sys

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            data = f.read()

        if data.count("A") != 1:
            raise Exception("Only one instance of A needs to be present")
        if data.count("B") != 1:
            raise Exception("Only one instance of B needs to be present")

        maze = data.splitlines()

        self.walls = []

        self.height, self.width = len(maze), max(len(i) for i in maze)

        for i in range(self.height):
            row = []
            try:
                for j in range(self.width):
                    if maze[i][j] == " ":
                        row.append(False)
                    elif maze[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif maze[i][j] == "B":
                        self.goal=(i, j)
                        row.append(False)
                    else:
                        row.append(True)
            except IndexError:
                row.append(False)

            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbours(self, state):
        r, c = state
        actions = (
            ("up", (r-1, c)),
            ("down", (r+1, c)),
            ("left", (r, c-1)),
            ("right", (r, c+1)),
        )

        result = []

        for action, (i, j) in actions:
            if 0 <= i < self.height and 0 <= j < self.width and not self.walls[i][j]:
                result.append((action, (i, j)))

        return result

    def solve(self):
        self.numExplored = 0
        self.explored = set()

        start = Node(state=self.start, action=None, parent=None)
        frontier = StackFrontier()
        frontier.addState(start)

        while True:
            if frontier.isEmpty():
                raise Exception("No, Solution")

            node = frontier.remove()
            self.numExplored += 1
            if node.state == self.goal:
                action = []
                cells = []
                while node.parent is not None:
                    action.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                action.reverse()
                cells.reverse()
                self.solution = (action, cells)

                return

            self.explored.add(node.state)
            for action, state in self.neighbours(node.state):
                if not frontier.containsState(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.addState(child)

    def outputImage(self, filename, showSolution=True, show_explored=False):
        size=50
        border=2

        img = Image.new("RGBA", (size*self.width, self.height*size), "black")

        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)

                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 255, 0)
                elif solution is not None and (i, j) in solution:
                    fill = (0, 255, 0)

                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (255, 0, 255)
                else:
                    fill = (230, 230, 230)

                draw.rectangle(
                    ([(j*size + border, i*size+border),
                      ((j+1)*size - border, (i+1)*size - border )]), fill =fill
                )
        img.save("dfs"+filename+".png")


name = "maze3"
m = Maze(name+".txt")
m.print()

m.solve()
print(m.numExplored)
m.print()
m.outputImage(name, show_explored=True)