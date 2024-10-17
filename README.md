# 3-tier-rule-engine-application-with-AST

Overview

A straightforward 3-tier rule engine application was built to assess user eligibility by evaluating attributes such as age, department, income, and expenditure.

1. User Interface (UI)
Objective: To create a user-friendly interface for individuals to input their attributes and view eligibility results. Additionally, admins can manage and update rules.
* Technology: Basic HTML/CSS.
* Features:
    * A form for users to input their attributes (age, department, income).
    * Display eligibility results based on user input.
    * An admin interface to create, update, or manage eligibility rules dynamically.
2. API Layer (Middle Tier)
Objective: Acts as the bridge between the UI and the backend, processing requests and communicating with the backend. It also evaluates the eligibility criteria using the AST-based rule engine.

* Framework: Flask/FastAPI.
* Features:
    * Handles user submissions via POST requests.
    * Admins can add or modify rules dynamically.
    * Rule engine using Abstract Syntax Tree (AST) to interpret and evaluate complex eligibility conditions.
* Endpoints:
    * POST /evaluate: Accepts user attributes and returns eligibility results based on predefined rules.
    * POST /rules: Allows the admin to create, modify, or delete rules using AST-based dynamic handling.
3. Backend (Data Tier)
Objective: Manages data storage, including user submissions, eligibility rules, and the results of evaluations.
* Database: SQLite.
* Features:
    * Stores user attributes and their evaluation history.
    * Saves eligibility rules in a structured, retrievable, and editable format.
4. AST for Rule Representation
Objective: Utilizes the Abstract Syntax Tree to represent and evaluate the rule conditions. AST is used to structure logical operations in a tree form, making it easy to parse, modify, and execute complex rules.
* Implementation: Built-in Python ast library is used to create and dynamically modify rules.
* Flow:
    * User Submission: Attributes are submitted through the UI.
    * API Processing: The API processes the request and uses the AST-based engine to evaluate the current rules.
    * AST-Based Rule Engine: Parses the rules into an AST and evaluates the conditions (e.g., age > 18, income > 50000).
    * Storage: Evaluation results and rules are saved in the backend for future use.
    * Admin Management: Administrators can add or update rules, and these changes immediately reflect in the rule evaluation process.

      
Summary

This 3-tier architecture combines a simple UI, an API that uses AST-based evaluation, and a data tier to store the rules and results. Users can input their data and see results, while admins have the flexibility to manage rules dynamically.

