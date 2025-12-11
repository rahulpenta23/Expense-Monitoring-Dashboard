from fastapi import FastAPI
from company_employees import router as employee_router
from bills import router as bills_router

app = FastAPI()


app.include_router(employee_router)
app.include_router(bills_router)
