from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)  # Initialize the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'  # Database configuration
db = SQLAlchemy(app)  # Initialize the database

# Database model for rules
class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Rule {self.rule_string}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Step 1: Define the AST Node class
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # left child (Node)
        self.right = right     # right child (Node)
        self.value = value     # optional value (int/str)

# Step 2: Create the `create_rule` function
def create_rule(rule_string):
    if not isinstance(rule_string, str) or not rule_string:
        raise ValueError("Invalid rule string")

    tokens = re.split(r'(\s+|[()])', rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]

    def build_ast(tokens):
        stack = []
        current = None

        for token in tokens:
            if token == '(':
                stack.append(current)
                current = None
            elif token == ')':
                if stack:
                    current = stack.pop()
            elif token in ('AND', 'OR'):
                node = Node("operator", left=current, value=token)
                current = node
            else:
                node = Node("operand", value=token)
                if current and current.type == "operator":
                    current.right = node
                current = node
        return current

    return build_ast(tokens)

# Step 3: Implement `combine_rules` function
def combine_rules(rules):
    root = None
    for rule in rules:
        if root is None:
            root = create_rule(rule)
        else:
            new_rule = create_rule(rule)
            root = Node("operator", left=root, right=new_rule, value="OR")
    return root

# Step 4: Implement the `evaluate_rule` function
def evaluate_rule(node, data):
    if node.type == "operand":
        left_operand, operator, right_operand = node.value.split(' ')
        right_operand = right_operand.strip("'") if "'" in right_operand else int(right_operand)

        # Evaluate based on the operator
        if operator == '>':
            return data[left_operand] > right_operand
        elif operator == '<':
            return data[left_operand] < right_operand
        elif operator == '=':
            return data[left_operand] == right_operand
    elif node.type == "operator":
        left_eval = evaluate_rule(node.left, data)
        right_eval = evaluate_rule(node.right, data)
        if node.value == "AND":
            return left_eval and right_eval
        elif node.value == "OR":
            return left_eval or right_eval

# API to create a new rule
@app.route('/api/rules', methods=['POST'])
def create_rule_api():
    data = request.json
    rule_string = data.get('rule_string')
    new_rule = Rule(rule_string=rule_string)
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({"message": "Rule created", "id": new_rule.id}), 201

# API to evaluate rules
@app.route('/api/rules/evaluate', methods=['POST'])
def evaluate_api():
    data = request.json
    user_data = data.get('user_data')
    rule_strings = [rule.rule_string for rule in Rule.query.all()]
    combined_ast = combine_rules(rule_strings)
    is_eligible = evaluate_rule(combined_ast, user_data)
    return jsonify({"eligible": is_eligible}), 200

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Main entry point to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
