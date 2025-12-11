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


# ===========================
# EMPLOYEE CRUD
# ===========================

@router.post("/company_employees")
def new_employee(employee_id: str, employee_name: str, employee_position: str, employee_mail: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO company_employees VALUES (%s,%s,%s,%s)",
        (employee_id, employee_name, employee_position, employee_mail)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"Msg": "new employee created"}


@router.get("/employees/{employee_id}")
def get_one_employee(employee_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM company_employees WHERE employee_id=%s", (employee_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return JSONResponse(content=row)


@router.get("/employees")
def get_all_employees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM company_employees")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return JSONResponse(content=rows)


@router.get("/employeest")
def get_all_employees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(employee_id) FROM company_employees")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return JSONResponse(content=rows)


@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, employee_name: str, employee_position: str, employee_mail: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE company_employees SET employee_name=%s, employee_position=%s, employee_mail=%s WHERE employee_id=%s",
        (employee_name, employee_position, employee_mail, employee_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"Msg": "Employee updated"}


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM company_employees WHERE employee_id=%s", (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "employee deleted successfully"}

@router.get('/category')
def only_id_names():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('select category,amount from bills;')
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows

@router.get('/total')
def only_id_names():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('select category,SUM(amount) AS total from bills GROUP BY category ORDER BY category;')
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows