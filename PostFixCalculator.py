class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "Node({})".format(self.value)

    __repr__ = __str__


class Stack:

    def __init__(self):
        self.top = None
        self.count = 0

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return 'Top:{}\nStack:\n{}'.format(self.top, out)

    __repr__ = __str__

    def is_empty(self):
        return self.count == 0

    def __len__(self):
        return self.count

    def peek(self):
        try:
            return self.top.value
        except AttributeError:
            return None

    def push(self, value):
        self.count += 1
        new = Node(value)
        new.next = self.top
        self.top = new

    def pop(self):
        if self.is_empty():
            return 'Stack is empty'
        else:
            self.count -= 1
            remove = self.top.value
            self.top = self.top.next
            return remove


def find_next_opr(txt):
    if not isinstance(txt, str) or len(txt) <= 0:
        return "error: findNextOpr"

    # --- YOU CODE STARTS HERE
    operators = {'+', '-', '/', '*', '^'}
    for char in txt:
        if char in operators:
            return txt.index(char)
    return -1


def is_number(txt):
    if not isinstance(txt, str) or len(txt) == 0:
        return "error: is_number"
    # --- YOU CODE STARTS HERE
    try:
        return type(float(txt.strip())) is float
    except ValueError:
        return False


def get_next_number(expr, pos):
    if not isinstance(expr, str) or not isinstance(pos, int) or len(expr) == 0 or pos < 0 or pos >= len(expr):
        return None, None, "error: getNextNumber"
    # --- YOU CODE STARTS HERE
    next_number = None
    next_opr_pos = None
    next_opr = None

    sub = expr[pos:].replace('(', ' ').replace(')', ' ').strip()

    if sub[0] == '-':
        negative_pos = find_next_opr(expr[pos:]) + pos
        next_pos = find_next_opr(expr[negative_pos+1:])
        if next_pos != -1:
            next_opr_pos = negative_pos + next_pos + 1
    else:
        next_pos = find_next_opr(expr[pos:])
        if next_pos != -1:
            next_opr_pos = next_pos + pos

    if next_opr_pos:
        next_opr = expr[next_opr_pos]
        next_number = expr[pos:next_opr_pos].strip()
    else:
        next_number = expr[pos:]

    next_number = next_number.replace('(', ' ').replace(')', ' ')
    if is_number(next_number):
        return float(next_number), next_opr, next_opr_pos
    else:
        next_number = None
    return next_number, next_opr, next_opr_pos


def postfix(expr):
    if not isinstance(expr, str) or len(expr) == 0:
        return "error: postfix"
    if expr.count('(') != expr.count(')'):
        return 'error, invalid expression'

    precedence = {'+': 1, '-': 1, '/': 2, '*': 2, '^': 3, '(': 0}
    operators = Stack()
    expression = []
    pos = 0
    while True:
        number, operator, operator_pos = get_next_number(expr, pos)
        if (not number and pos < len(expr.strip())) or operator_pos == "error: getNextNumber":
            return 'error, invalid expression'
        if number:
            expression.append(str(number))
        if operator_pos is not None:
            for c in expr[pos:operator_pos]:
                if c == '(':
                    operators.push('(')
                elif c == ')':
                    while operators.peek() and operators.peek() != '(':
                        expression.append(operators.pop())
                    operators.pop()
        if operator:
            while operators.peek() and precedence[operator] <= precedence[operators.peek()]:
                expression.append(operators.pop())
            operators.push(operator)
        if operator_pos:
            pos = operator_pos + 1
        else:
            for i in range(len(operators)):
                if operators.peek() == '(':
                    operators.pop()
                else:
                    expression.append(operators.pop())
            break
    return ' '.join(expression)


def calculator(expr):
    expression = postfix(expr)
    if expression == 'error, invalid expression':
        return expression
    stack = Stack()
    operators = {'+', '-', '/', '*', '^'}
    for item in expression.split(' '):
        if item in operators:
            num2 = stack.pop()
            num1 = stack.pop()
            stack.push(evaluate(num1, item, num2))
        else:
            stack.push(float(item))
    return stack.pop()


def evaluate(num1, opr, num2):
    evaluation = {
        '+': num1 + num2,
        '-': num1 - num2,
        '/': num1 / num2,
        '*': num1 * num2,
    }

    # Only perform if needed to avoid overflows
    if opr == '^':
        return num1 ** num2
    return evaluation[opr]


def main():
    expression = "5 * 12 ^ (4 - 2)"
    evaluated = calculator(expression)
    print(evaluated)


if __name__ == "__main__":
    main()
