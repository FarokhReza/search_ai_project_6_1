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
            for current_state in prb.successor(state):
                if current_state.__hash__() in save_state:
                    continue
                current_state.g_n = state.g_n + prb.get_cost_from_change(
                    state, current_state.prev_action[0])
                my_list.append(current_state)

        return None                        

    def get_heuristic_cost(state: State) -> int:
        h_cost = 0

        for pipe in state.pipes:
            if pipe.is_one_color():
                h_cost += 20

        for pipe in state.pipes:
            if pipe.is_empty():
                h_cost += 8

        
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
        state.h_n = Search.get_heuristic_cost(state)
        state.f_n = state.h_n + state.g_n
        my_list.append(state)

        while len(my_list):
            state = max(my_list, key=lambda x:x.f_n)
            my_list.remove(state)
            if prb.is_goal(state):
                return Solution(state, prb, start_time)
            save_state.append(state.__hash__())
            for current_state in prb.successor(state):
                if current_state.__hash__() in save_state:
                    continue
                current_state.g_n = state.g_n + prb.get_cost_from_change(
                    state, current_state.prev_action[0])
                current_state.h_n = Search.get_heuristic_cost(current_state)
                current_state.f_n = current_state.g_n + current_state.h_n
                my_list.append(current_state)

        return None
    
    @staticmethod
    def ida_star(prb: Problem) -> Solution:
        start_time = datetime.now()
        my_list = []
        save_state = []
        state = prb.initState
        state.g_n = 0
        depth = state.h_n = Search.get_heuristic_cost(state)
        state.f_n = state.h_n + state.g_n
        my_list.append(state)
        min_f = float('inf')
        while True:
            result, new_depth = Search.search(prb, my_list, save_state, depth, start_time, min_f)
            if result is not None:
                return result
            # if new_depth == float('inf'):
            #     return None
            depth = new_depth

    @staticmethod
    def search(prb: Problem, my_list, save_state, depth, start_time, min_f):
        f_limit = depth
        state = max(my_list, key=lambda x:x.f_n)
        my_list.remove(state)
        if state in save_state:
            return None, f_limit
        if prb.is_goal(state):
            return Solution(state, prb, start_time), f_limit
        for current_state in prb.successor(state):
            if current_state.__hash__() in save_state:
                continue

            current_state.g_n = state.g_n + prb.get_cost_from_change(
                state, current_state.prev_action[0])
            current_state.h_n = Search.get_heuristic_cost(current_state)
            current_state.f_n = current_state.g_n + current_state.h_n
            my_list.append(current_state)
           
            if current_state.f_n > f_limit:
                min_f = min(min_f, current_state.f_n)
                continue
            
            if prb.is_goal(current_state):
                return Solution(current_state, prb, start_time), f_limit
            
            save_state.append(current_state.__hash__())
            result, new_f_limit = Search.search(prb, my_list, save_state, depth, start_time, min_f)
            if result is not None:
                return result, f_limit
            if new_f_limit < min_f:
                min_f = new_f_limit
            my_list.pop()
            save_state.pop()
        return None, min_f

    @staticmethod
    def rbfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        save_state = []
        state = prb.initState
        state.g_n = 0   
        state.h_n = Search.get_heuristic_cost(state)
        state.f_n = state.h_n + state.g_n
        return Search.rbf_search(prb, state, float('inf'), start_time, save_state)


    @staticmethod
    def rbf_search(prb: Problem, state: State, f_limit: int, start_time: datetime, save_state):
        if prb.is_goal(state):
            return Solution(state, prb, start_time)

        states = prb.successor(state)
        if not states:
            return None

        for next_state in states:
            next_state.g_n = state.g_n + prb.get_cost_from_change(state, next_state.prev_action[0])
            next_state.h_n = Search.get_heuristic_cost(next_state)
            next_state.f_n = next_state.g_n + next_state.h_n

        while True:
            best_state = max(states, key=lambda x: x.f_n)
            if best_state.__hash__() in save_state:
                continue
            save_state.append(best_state.__hash__())
            # f = min(f_limit, best_successor.f_n)
            f = min(f_limit, max(states, key=lambda x: x.f_n if x != best_state else -float('inf')).f_n)
            result = Search.rbf_search(prb, best_state, f_limit, start_time, save_state)
            if result:
                return result
            best_state.f_n = float('inf')
    # @staticmethod
    # def rbf_search(prb: Problem, state: State, f_limit: int, start_time: datetime):
    #     if prb.is_goal(state):
    #         return Solution(state, prb, start_time)

    #     states = prb.successor(state)
    #     if not states:
    #         return None

    #     for next_state in states:
    #         next_state.g_n = state.g_n + prb.get_cost_from_change(state, next_state.prev_action[0])
    #         next_state.h_n = Search.get_heuristic_cost(next_state)
    #         next_state.f_n = next_state.g_n + next_state.h_n

    #     while True:
    #         best_state = max(states, key=lambda x: x.f_n)
            
    #         # f = min(f_limit, best_successor.f_n)
    #         f = min(f_limit, max(states, key=lambda x: x.f_n if x != best_state else -float('inf')).f_n)
    #         result = Search.rbf_search(prb, best_state, f_limit, start_time)
    #         if result:
    #             return result
    #         best_state.f_n = float('inf')
            