from Solution import Solution
from Problem import Problem
from datetime import datetime
from State import State


class Search:

    @staticmethod
    def bfs(prb: Problem) -> Solution:  # this method get a first
        # state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        state = prb.initState
        queue.append(state)
        while len(queue):
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
        while len(stack):
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
        while len(stack):
            state = stack.pop()
            if state.__hash__() not in save_state:
                save_state.append(state.__hash__())
                if prb.is_goal(state):
                    return Solution(state, prb, start_time)
                neighbors = prb.successor(state)
                stack.extend(neighbors)
        return None

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

    @staticmethod
    def ucs(prb: Problem):
        start_time = datetime.now()
        my_list = []
        save_state = []
        state = prb.initState
        state.g_n = 0
        my_list.append(state)

        while len(my_list):
            state = min(my_list, key=lambda x:x.g_n)
            my_list.remove(state)
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            
            if state.__hash__() in save_state:
                continue
            save_state.append(state.__hash__())
            for successor in prb.successor(state):
                if successor.__hash__() in save_state:
                    continue
                g_n = state.g_n + prb.get_cost_from_change(
                    state, successor.prev_action[0])
                if successor not in my_list:
                    successor.g_n = g_n
                    my_list.append(successor)
                else:
                    if g_n < successor.g_n:
                        successor.g_n = g_n

        return None                        

    def get_heuristic_cost(state: State) -> int:
        h_cost = 0

        for pipe in state.pipes:
            if pipe.is_one_color():
                h_cost += 20

        for pipe in state.pipes:
            if pipe.is_empty():
                h_cost += 10
        
        for pipe in state.pipes:
            for ball in pipe.stack:
                if ball != pipe.stack[-1]:
                    h_cost -= 1

        return h_cost

    @staticmethod
    def a_star(prb: Problem) -> Solution:
        start_time = datetime.now()
        my_list = []
        save_state = []
        state = prb.initState
        state.g_n = 0
        
        h_n = Search.get_heuristic_cost(state)
        state.f_n = h_n
        my_list.append(state)

        while len(my_list):
            state = max(my_list, key=lambda x:x.f_n)
            my_list.remove(state)
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            save_state.append(state.__hash__())
            for successor in prb.successor(state):
                if successor.__hash__() in save_state:
                    continue
                g_n = state.g_n + prb.get_cost_from_change(
                    state, successor.prev_action[0])
                if successor not in my_list:
                    successor.h_n = Search.get_heuristic_cost(successor)
                    f_n = g_n + successor.h_n
                    successor.g_n = g_n
                    successor.f_n = f_n
                    my_list.append(successor)
                else:
                    if g_n < successor.g_n:
                        successor.g_n = g_n
                        h_n = Search.get_heuristic_cost(successor)
                        f_n = h_n + g_n
                        successor.f_n = f_n

        return None
    
    @staticmethod
    def ida_star(prb: Problem) -> Solution:
        start_time = datetime.now()
        my_list = []
        save_state = []
        state = prb.initState
        state.g_n = 0
        h_n = Search.get_heuristic_cost(state)
        state.f_n = h_n
        my_list.append(state)
        depth = h_n

        while True:
            result, new_depth = Search.search(prb, my_list, save_state, depth, start_time)
            if result is not None:
                return result
            if new_depth == float('inf'):
                return None
            depth = new_depth

    @staticmethod
    def search(prb: Problem, my_list, save_state, depth, start_time):
        f_limit = depth
        min_f = float('inf')
        state = max(my_list, key=lambda x:x.f_n)
        if state in save_state:
            return None, f_limit
        if prb.is_goal(state):
            return Solution(state, prb, start_time), f_limit
        for successor in prb.successor(state):
            if successor.__hash__() in save_state:
                continue

            g_n = state.g_n + prb.get_cost_from_change(
                state, successor.prev_action[0])
            successor.h_n = Search.get_heuristic_cost(successor)
            f_n = g_n + successor.h_n
            successor.g_n = g_n
            successor.f_n = f_n
            my_list.append(successor)

            if f_n > f_limit:
                min_f = min(min_f, f_n)
                continue
            
            if prb.is_goal(successor):
                return Solution(successor, prb, start_time), f_limit
            
            save_state.append(successor.__hash__())
            result, new_f_limit = Search.search(prb, my_list, save_state, depth, start_time)
            if result is not None:
                return result, f_limit
            if new_f_limit < min_f:
                min_f = new_f_limit
            my_list.pop()
            save_state.pop()
        return None, min_f

    