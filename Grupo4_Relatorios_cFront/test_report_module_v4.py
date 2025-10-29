import unittest
from datetime import datetime, timedelta
from report_module_v4 import get_most_borrowed_books_report, get_most_active_users_report, to_csv

def dt(days=0):
    return (datetime.utcnow() - timedelta(days=days)).isoformat()

BOOKS = [{'id':1,'title':'Book A'},{'id':2,'title':'Book B'},{'id':3,'title':'Book C'}]
USERS = [{'id':1,'name':'Alice','email':'a@x'},{'id':2,'name':'Bob','email':'b@x'},{'id':3,'name':'Charlie','email':'c@x'}]
LOANS = [{'book_id':1,'user_id':1,'date':dt(1)},{'book_id':2,'user_id':1,'date':dt(2)},{'book_id':1,'user_id':2,'date':dt(3)},{'book_id':1,'user_id':3,'date':dt(29)},{'book_id':3,'user_id':3,'date':dt(40)}]

class T(unittest.TestCase):
    def test_default_last_30_days(self):
        books = get_most_borrowed_books_report(LOANS, BOOKS, top_n=2)
        self.assertEqual(len(books), 2)
        self.assertTrue(all(r['count'] > 0 for r in books))

    def test_explicit_range(self):
        start = (datetime.utcnow() - timedelta(days=5)).isoformat()
        end = datetime.utcnow().isoformat()
        books = get_most_borrowed_books_report(LOANS, BOOKS, start=start, end=end)
        self.assertTrue(any(r['id']==1 for r in books))

    def test_limit_1000(self):
        many = LOANS[:]
        for _ in range(1200):
            many.append({'book_id':2,'user_id':1,'date':dt(0)})
        books = get_most_borrowed_books_report(many, BOOKS)
        self.assertTrue(any(r['id']==2 for r in books))

    def test_privacy_users(self):
        users = get_most_active_users_report(LOANS, USERS, top_n=2)
        for u in users:
            self.assertIn('id', u)
            self.assertIn('name', u)
            self.assertNotIn('email', u)

    def test_csv_export(self):
        rows = get_most_borrowed_books_report(LOANS, BOOKS, top_n=2)
        csv = to_csv(rows)
        self.assertTrue(csv.startswith('id,title,count'))

if __name__ == '__main__':
    unittest.main()
