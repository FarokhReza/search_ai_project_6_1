from Solution import Solution
from Problem import Problem
from datetime import datetime


class Search:
    @staticmethod

    def bfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if prb.is_goal(c):
                    return Solution(c, prb, start_time)
                queue.append(c)
        return None

    @staticmethod

    def dfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        stack = []
        state = prb.initState
        stack.append(state)
        while len(stack) > 0:
            state = stack.pop()
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            neighbors = prb.successor(state)
            stack.extend(neighbors)
        return None
    
    
    @staticmethod
    
    def dfs_2(prb: Problem) -> Solution:
        start_time = datetime.now()
        stack = []
        save_state = []
        state = prb.initState
        stack.append(state)
        # save_state.append(state)
        while len(stack) > 0:
            state = stack.pop()
            if state.__hash__() not in save_state:
                save_state.append(state.__hash__())
                if prb.is_goal(state):
                    return Solution(state, prb, start_time)
                neighbors = prb.successor(state)
                stack.extend(neighbors)
        return None