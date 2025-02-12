class Node:
    def __init__(self, state=None, parent=None, action=None):
        self.state = state
        self.action = action
        self.parent = parent


class Frontier:
    def __init__(self):
        self.frontier = []

    def addState(self, node):
        self.frontier.append(node)


    def isEmpty(self):
        return len(self.frontier) == 0


    def containsState(self, state):
        return any(i.state == state for i in self.frontier)


class StackFrontier(Frontier):
    def remove(self):
        if self.isEmpty():
            raise Exception("Frontier is emmpty")

        state = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return state


class QueueFrontier(Frontier):
    def remove(self):
        if self.isEmpty():
            raise Exception("Frontier is emmpty")

        state = self.frontier[0]
        self.frontier = self.frontier[1:]
        return state