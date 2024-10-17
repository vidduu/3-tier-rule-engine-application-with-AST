from flask import Flask, jsonify, request
from models import db, Rule
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
db.init_app(app)

with app.app_context():
    db.create_all()

# Create your existing functions here (create_rule, combine_rules, evaluate_rule)

@app.route('/api/rules', methods=['POST'])
def create_rule():
    data = request.json
    rule_string = data.get('rule_string')
    new_rule = Rule(rule_string=rule_string)
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({"message": "Rule created", "id": new_rule.id}), 201

@app.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    rule = Rule.query.get(rule_id)
    if not rule:
        return jsonify({"message": "Rule not found"}), 404
    db.session.delete(rule)
    db.session.commit()
    return jsonify({"message": "Rule deleted"}), 204

@app.route('/api/rules/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    user_data = data.get('user_data')
    rule_strings = [rule.rule_string for rule in Rule.query.all()]
    combined_ast = combine_rules(rule_strings)
    is_eligible = evaluate_rule(combined_ast, user_data)
    return jsonify({"eligible": is_eligible}), 200

if __name__ == '__main__':
    app.run(debug=True)
