from Solution import Solution
from Problem import Problem
from datetime import datetime
from State import State


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


    @staticmethod

    def dfs_limited_depth(prb: Problem, depth: int, start_time: datetime) -> Solution:
        stack = []
        state = prb.initState
        stack.append((state, 0))
        current_depth = 0
        while len(stack):
            state, current_depth = stack.pop()
            if current_depth <= depth:
                if prb.is_goal(state):
                    return Solution(state, prb, start_time)
                neighbors = prb.successor(state)
                for neighbor in neighbors:
                    stack.append((neighbor, current_depth+1))

        return None


     # test2 -> 40s

    def dfs_limited_depth_2(prb: Problem, depth: int, start_time: datetime) -> Solution:
        stack = []
        save_state = []

        state = prb.initState
        stack.append((state, 0))

        while len(stack):
            state, current_depth = stack.pop()
            if current_depth <= depth:
                if state.__hash__() not in save_state:
                    save_state.append(state.__hash__())
                    if prb.is_goal(state):
                        return Solution(state, prb, start_time)
                    neighbors = prb.successor(state)
                    for neighbor in neighbors:
                        stack.append((neighbor, current_depth+1))

        return None

    @staticmethod

    def ids(prb: Problem) -> Solution:
        start_time = datetime.now()
        depth = 0
        while True:
            result = Search.dfs_limited_depth_2(prb, depth, start_time)
            if result is not None:
                return result
            depth += 1

    
    # def get_heuristic_cost(state: State) -> int:
    #     # calculate heuristic cost using number of pipes that are not one color
    #     cost = 0
    #     for pipe in state.pipes:
    #         if not pipe.is_one_color():
    #             cost += 1
    #     return cost


    # def get_heuristic_cost(state: State) -> int:
    #     h_cost = 0
    #     for pipe in state.pipes:
    #         if not pipe.is_one_color():
    #             h_cost += 1
    #         if not (pipe.is_full() or pipe.is_empty()):
    #             h_cost += 1
    #     for pipe in state.pipes:
    #         for ball in pipe.stack:
    #             if ball != pipe.stack[-1]:
    #                 h_cost += 1
    #     return h_cost
    

    def get_heuristic_cost(state: State) -> int:
        h_cost = 0
        
        for pipe in state.pipes:
            for ball in pipe.stack:
                if ball != pipe.stack[-1]:
                    h_cost += 1
        return h_cost
    @staticmethod
    def a_star(prb: Problem) -> Solution:
        start_time = datetime.now()
        open_set = []
        closed_set = set()
        start_state = prb.initState
        # initialize start state
        start_state.g_n = 0
        start_state_h_n = Search.get_heuristic_cost(start_state)
        start_state.priority = start_state.g_n + start_state_h_n
        open_set.append(start_state)

        while open_set:
            current_state = min(open_set, key=lambda x:x.priority)
            open_set.remove(current_state)
            if prb.is_goal(current_state):
                return Solution(current_state, prb, start_time)
            closed_set.add(current_state.__hash__())
            for successor in prb.successor(current_state):
                if successor.__hash__() in closed_set:
                    continue
                successor_g_n = current_state.g_n + prb.get_cost_from_change(current_state, successor.prev_action[0])
                if successor not in open_set:
                    successor.h_n = Search.get_heuristic_cost(successor)
                    successor_g_n_h_n = successor_g_n + successor.h_n
                    successor.g_n = successor_g_n
                    successor.priority = successor_g_n_h_n
                    open_set.append(successor)
                else:
                    if successor_g_n < successor.g_n:
                        successor.g_n = successor_g_n
                        successor_h_n = Search.get_heuristic_cost(successor)
                        successor_f_n = successor_h_n + successor_g_n
                        successor.priority = successor_f_n

        return None

    
