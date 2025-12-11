from fastapi import APIRouter
import psycopg2
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()
db_url =os.getenv("DB_url")

def get_conn():
    return psycopg2.connect(db_url)


# ======================
# BILLS CRUD + ANALYTICS
# ======================

@router.get("/bills")
def get_bills():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bills")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows



@router.post("/bills")
def create_bill(
    exp_id: str,
    employee_id: str,
    credit_limit: int,
    category: str,
    vendor: str,
    amount: int,
    date: str,
):
    saving = credit_limit - amount
    risk = 0

    if saving <= credit_limit / 15:
        risk += 50
    elif saving <= credit_limit / 10:
        risk += 25
    elif saving <= credit_limit / 5:
        risk += 10

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bills (exp_id, employee_id, category, vendor, amount, date, credit_limit, saving, risk)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (exp_id, employee_id, category, vendor, amount, date, credit_limit, saving, risk))

    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Bill Added"}


@router.delete("/bills/{employee_id}")
def delete_bill(employee_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM bills WHERE employee_id=%s", (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "bill deleted successfully"}


@router.get("/pending_bills")
def get_pending_bills():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.employee_id, c.employee_name, b.category, b.vendor, b.amount, 
               b.date, b.saving, b.risk
        FROM bills b
        INNER JOIN company_employees c ON b.employee_id = c.employee_id
        WHERE b.risk >= 25
        ORDER BY b.risk DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.put("/bills/approve/{employee_id}")
def approve_bills(employee_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE bills SET risk=0 WHERE employee_id=%s", (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Approved"}


@router.put("/bills/reject/{employee_id}")
def reject_bills(employee_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE bills SET risk=75 WHERE employee_id=%s", (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Rejected"}


@router.get("/last")
def last_three():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM bills
        ORDER BY exp_id DESC
        LIMIT 3;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@router.get("/total_exps")
def total_exp_per_employee():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT employee_id, SUM(amount) AS total
        FROM bills
        GROUP BY employee_id
        ORDER BY total DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@router.get('/total_exp')
def only_total_exp():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('select employee_id,SUM(amount) AS total from bills GROUP BY employee_id ORDER BY employee_id;')
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows

@router.get("/billz")
def get_all_employees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(category) FROM bills ;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row