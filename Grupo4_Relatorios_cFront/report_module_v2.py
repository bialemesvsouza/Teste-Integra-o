from collections import Counter

def get_most_borrowed_books(books, loans, top_n=5):
    c = Counter([l['book_id'] for l in loans])
    out = []
    for b in books:
        out.append({'id': b['id'], 'title': b.get('title',''), 'count': c.get(b['id'], 0)})
    return out

def get_most_active_users(users, loans, top_n=5):
    c = Counter([l['user_id'] for l in loans])
    out = []
    for u in users:
        out.append({'id': u['id'], 'name': u.get('name',''), 'count': c.get(u['id'], 0)})
    return out
