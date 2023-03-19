class Pipe:
    def __init__(self, stack: list, limit: int):
        self.stack = stack
        self.limit = limit

    def is_one_color(self) -> bool:  # this function checks that all balls are the same color
        for i in range(1, len(self.stack)):
            if self.stack[i] != self.stack[i - 1]:
                return False
        return True

    def add_ball(self, color):
        self.stack.append(color)

    def remove_ball(self):
        return self.stack.pop()

    def is_full(self):
        if len(self.stack) == self.limit:
            return True
        return False

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        return False

    # def __str__(self):
    #     return '{' + ' '.join(self.stack) + '}'      


    def print_pipe(self):
        print('{', end=' ')
        for i in self.stack:
            print(i, end=' ')
        print('}')

    def get_pipe_for_gui(self):
        # p1=RGB,p2=RBR,p3=GBR,p4=GGG,p5=E,p6=E,p7=E,p8=E
        out = ""
        if len(self.stack) == 0:
            out += 'E'
            return out
        for i in self.stack:
            out += (str(i[0]).upper())
        return out

    def __hash__(self):
        hash_string = ''
        for i in self.stack:
            hash_string += str(i) + " "
        return hash_string
    
    