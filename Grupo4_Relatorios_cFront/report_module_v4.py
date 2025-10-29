from collections import Counter
from datetime import datetime, timedelta
from typing import List, Dict, Optional

ISO_FMT = "%Y-%m-%dT%H:%M:%S"

def _parse_iso(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        try:
            return datetime.fromisoformat(s.replace('Z','+00:00')).replace(tzinfo=None)
        except ValueError:
            return datetime.strptime(s[:19], ISO_FMT)
    except Exception:
        raise ValueError("Data invalida")

def _window(start: Optional[str], end: Optional[str]):
    end_dt = _parse_iso(end) or datetime.utcnow()
    start_dt = _parse_iso(start) or (end_dt - timedelta(days=30))
    if start_dt > end_dt:
        raise ValueError("start > end")
    return start_dt, end_dt

def _filter_loans_by_date(loans: List[Dict], start: Optional[str], end: Optional[str]):
    s, e = _window(start, end)
    out = []
    for l in loans:
        d = _parse_iso(l['date']) if isinstance(l.get('date'), str) else l.get('date')
        if d is None:
            continue
        if isinstance(d, datetime):
            d_naive = d.replace(tzinfo=None)
        else:
            raise ValueError("date invalida")
        if s <= d_naive <= e:
            out.append(l)
        if len(out) >= 1000:
            break
    return out

def _top_sorted(items, top_n):
    items.sort(key=lambda x: x['count'], reverse=True)
    return items[:top_n] if top_n else items

def get_most_borrowed_books_report(loans: List[Dict], books: List[Dict], start: Optional[str]=None, end: Optional[str]=None, top_n: Optional[int]=None):
    fl = _filter_loans_by_date(loans, start, end)
    c = Counter([l['book_id'] for l in fl])
    rows = [{'id': b['id'], 'title': b.get('title',''), 'count': c.get(b['id'], 0)} for b in books if c.get(b['id'], 0) > 0]
    return _top_sorted(rows, top_n)

def get_most_active_users_report(loans: List[Dict], users: List[Dict], start: Optional[str]=None, end: Optional[str]=None, top_n: Optional[int]=None):
    fl = _filter_loans_by_date(loans, start, end)
    c = Counter([l['user_id'] for l in fl])
    rows = [{'id': u['id'], 'name': u.get('name',''), 'count': c.get(u['id'], 0)} for u in users if c.get(u['id'], 0) > 0]
    return _top_sorted(rows, top_n)

def to_csv(rows):
    if not rows:
        return ''
    cols = list(rows[0].keys())
    out = [','.join(cols)]
    for r in rows:
        out.append(','.join(str(r.get(k,'')) for k in cols))
    return '\n'.join(out)
