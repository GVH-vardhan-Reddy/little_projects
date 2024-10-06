from flask import Flask, request, render_template
app = Flask(__name__)
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    left_associative = {'+': True, '-': True, '*': True, '/': True, '^': False}

    def is_operator(c):
        return c in precedence

    def greater_precedence(op1, op2):
        return precedence[op1] > precedence[op2]

    def equal_precedence(op1, op2):
        return precedence[op1] == precedence[op2]

    output = []
    operators = []
    number = []

    for char in expression:
        if char.isdigit():  # If the character is a digit
            number.append(char)
        else:
            if number:
                output.append(''.join(number))
                number = []
            if char == '(':
                operators.append(char)
            elif char == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Pop the '('
            elif is_operator(char):
                while (operators and operators[-1] != '(' and
                       (greater_precedence(operators[-1], char) or
                        (equal_precedence(operators[-1], char) and left_associative[char]))):
                    output.append(operators.pop())
                operators.append(char)

    if number:
        output.append(''.join(number))

    while operators:
        output.append(operators.pop())

    return ' '.join(output)

def evaluate_postfix(expression):
    stack = []
    tokens = expression.split()

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            # Ensure to handle operators and operands correctly
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)

    return stack[0]

def evaluate_infix(expression):
    postfix_expression = infix_to_postfix(expression)
    return evaluate_postfix(postfix_expression)
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression=None
    if request.method == 'POST':
        expression = request.form.get('textarea')
        result = evaluate_infix(expression)
    return render_template('index.html', fix=result,expression=expression)

if __name__ == '__main__':
    app.run(debug=True)
