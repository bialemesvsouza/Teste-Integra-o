from flask import Flask, request, jsonify, render_template
from report_module_v4 import (
    get_most_borrowed_books_report,
    get_most_active_users_report,
    to_csv
)

app = Flask(__name__)

# Mock de dados (pode vir de um banco no futuro)
BOOKS = [{'id':1,'title':'Book A'},{'id':2,'title':'Book B'},{'id':3,'title':'Book C'}]
USERS = [{'id':1,'name':'Alice'},{'id':2,'name':'Bob'},{'id':3,'name':'Charlie'}]
LOANS = [
    {'book_id':1,'user_id':1,'date':'2025-10-01T10:00:00'},
    {'book_id':2,'user_id':2,'date':'2025-10-15T12:30:00'},
    {'book_id':1,'user_id':3,'date':'2025-10-25T14:00:00'},
    {'book_id':3,'user_id':1,'date':'2025-09-20T10:00:00'},
    {'book_id':2,'user_id':1,'date':'2025-10-29T19:59:00'}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report/books')
def report_books():
    start = request.args.get('start')
    end = request.args.get('end')
    top_n = request.args.get('top_n', type=int)
    rows = get_most_borrowed_books_report(LOANS, BOOKS, start, end, top_n)
    return jsonify(rows)

@app.route('/report/users')
def report_users():
    start = request.args.get('start')
    end = request.args.get('end')
    top_n = request.args.get('top_n', type=int)
    rows = get_most_active_users_report(LOANS, USERS, start, end, top_n)
    return jsonify(rows)

@app.route('/report/books/csv')
def report_books_csv():
    rows = get_most_borrowed_books_report(LOANS, BOOKS)
    return to_csv(rows), 200, {'Content-Type': 'text/csv'}

if __name__ == '__main__':
    app.run(debug=True)
