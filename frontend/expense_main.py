import streamlit as st
from datetime import date
import requests

st.set_page_config(layout="wide")
st.sidebar.markdown("## 🧾 Expense Monitor")
page = st.sidebar.radio("Navigation", ["Home", "Employee View", "Category View", "Approvals", "Create Expense"])


if page == 'Home':
        # st.container(border=True)
        st.header("Expense Monitoring Dashboard")
        st.write('🟢 Real-time tracking of employee expenses')
        with st.container(border=True):
         cols = st.columns([1,1,1])
         with cols[0]:
            st.write('Total Expenses')
            ress = requests.get('http://localhost:8000/total_exp')
            ress = ress.json()
            sum=0
            for i in range(0,len(ress)):
              sum+=ress[i][1]
            st.subheader(f"Rs.{sum}")
         with cols[1]:
            st.write('Total Claims')
            ress = requests.get('http://localhost:8000/billz')
            ress = ress.json()
            ress = ress[0]
            st.subheader(ress)
            
         with cols[2]:
            st.write('Active Employees')
            ress = requests.get('http://localhost:8000/employeest')
            ress = ress.json()
            ress = ress[0][0]
            st.subheader(f'{ress}')
        st.markdown('---')
        colss = st.columns([1,1])
        with colss[0]:
            st.subheader("Recent Expenses")
            ress = requests.get('http://localhost:8000/last')
            ress = ress.json()
            for i in ress:
                with st.container(border=True):
                    st.write(f"**Expense ID:** {i[0]}")
                    st.write(f"**Employee ID:** {i[4]}")
                    st.write(f"**Credit Limit** {i[9]}")
                    st.write(f"**Category:** {i[1]}")
                    st.write(f"**Vendor:** {i[7]}")
                    st.write(f"**Amount:** {i[2]}")
                    st.write(f"**Date:** {i[3]}")
                    # st.write(f"**Saving:** {i[5]}")
                    # st.write(f"**Risk:** {i[6]}")
                    # st.write(f"**Extra 1:** {i[8]}")
        with colss[1]:
            st.subheader("Top 5 Spenders")
            res= requests.get("http://localhost:8000/total_exps")
            res = res.json()
            # st.write(res) 
            for i in res:
                with st.container(border=True):
                    st.write(f'**Employee_id:** {i[0]}')
                    st.write(f'**Total Expenses:** {i[1]}')

#Employee View
if page == "Employee View":
   st.title("Employee Details & Expenses")
   employee_id = st.number_input("Enter Employee ID (e.g. 1):", min_value=1)
   col=st.columns([1,1])
   with col[1]:
    btn1 = st.button("Total Expense",type='primary')
   with col[0]:      
    btn = st.button("Fetch Employee",type='primary')
   if btn:
    url = f"http://localhost:8000/employees/{employee_id}"
    # URL = f"http://localhost:8000/total_exp/{employee_id}"
    
    res = requests.get(url)
    if res.status_code == 200:
     res = res.json()
     if res is None:
         st.error("Enter correct Employee Id")
         st.stop()
     else:
        st.success("Employee Found")
        with st.container(border=True):
        #  for i in res:
         st.write("**Id** : ",res[0])
         st.write("**Name** : ",res[1])
         st.write("**Position** : ",res[2])
         st.write("**Email** : ",res[3])
   if btn1:
    URL = f"http://localhost:8000/total_exp"
    OKAY = requests.get(URL)    
    if OKAY.status_code == 200:
                st.success("Employee S")
                OKAY = OKAY.json()
                for i,j in enumerate(OKAY):
                 with st.container(border=True):
                  st.write("Employee ",OKAY[i][0])
                  st.write("       Total - ",OKAY[i][1])
            
    else:
            st.error("Employee not found")


# -------------------------
# Page: Category View
# -------------------------
elif page == "Category View":
    st.title("Category Analytics")

    reqq = requests.get("http://localhost:8000/category")
    if reqq.status_code==200:
        reqq = reqq.json()
    
        reqq = [{"category": item[0], "amount": item[1]} for item in reqq]

        st.vega_lite_chart(
        {
            "data": {"values": reqq},
            "mark": "bar",
            "encoding": {
                "x": {"field": "category", "type": "nominal"},
                "y": {"field": "amount", "type": "quantitative"},
                "color": {"field": "category", "type": "nominal"}
            }
        },
        use_container_width=True
    )
    st.markdown("---")
    st.subheader("Category Totals")
    
    reqqs = requests.get("http://localhost:8000/total")
    if reqqs.status_code==200:
        reqqs = reqqs.json()
        data= [{"Employee": item[0], "Total Amount": item[1]} for item in reqqs]
    #       st.error("Failed to fetch category data")
    if data:
        st.table(data)
    else:
        st.warning("No total data available")
#||||||||||||||||||||||||||||
# Page: Approvals
# ||||||||||||||||||||||||||||
elif page == "Approvals":
    st.title("Pending Approvals")
    employee_id=st.text_input("Employee Id: ")
    btn=st.button("Delete Bills",type='primary')
    if btn:
        del1 = requests.delete(f"http://localhost:8000/bills/{employee_id}")
    req = requests.get("http://localhost:8000/pending_bills")
    if req.status_code == 200:
        bills = req.json()
        for i,j in enumerate(bills):
          with st.container(border=True):
            # for s in j:
             st.write("Id : ",j[0])
             st.write("Name : ",j[1])
             st.write("Category : ",j[2])
             st.write("Vendor : ",j[3])
             st.write("Credit Limit : ",j[4])
             st.write("Date : ",j[5])
             st.write("Saving",j[6])
             st.write("Risk Rate",j[7])

        # if not bills:
        #     st.info("No pending approvals.")
        # else:


# Page: Create Expense

elif page == "Create Expense":
    st.title("Create Expense (Manual)")

    with st.form('Create_expense_form'):
        
    
        # def update_expense():
        exp_id = st.number_input('Expense_id',min_value=1)
        employee_id = st.number_input('Employee_id',min_value=1 )
        credit_limit = st.number_input('Credit Limit',min_value=10000,step=10000)
        category = st.selectbox('Category',['Hotel','Hospital','Food','Travel','Other'])
        vendor = st.text_input('Vendor')
        amount = st.number_input('Amount Rs.',min_value=1000 ,step=1000)
        dates = st.date_input('Select Date')
        # saving = st.number_input('Enter Attendance',min_value=1)
        # performance = st.number_input('Enter Performance',min_value=1)
        inst_dtl = st.form_submit_button("Create Expense",type='primary')
        if inst_dtl:
                # dates= str(dates)
                url = f"http://localhost:8000/bills?exp_id={exp_id}&employee_id={employee_id}&credit_limit={credit_limit}&category={category}&vendor={vendor}&amount={amount}&date={dates}"
                res = requests.post(url)
                if res.status_code == 200:
                    st.toast('Added')
                else:
                    st.error('not found')
# data = res['employee_id']
st.sidebar.divider()
st.sidebar.markdown("### Admin")
with st.sidebar.expander("Create Employee", expanded=False):
    emp_id = st.number_input('Enter Employee_id',min_value=1 )
    emp_name = st.text_input('Enter Name')
    emp_position = st.selectbox('Select',['Manager','Cashier','Waiter'])
    emp_mail = st.text_input('Email')
    # credit_limit = st.number_input('Credit Limit',min_value=10000, step =100)
    btnadd = st.button('Create Employee',type='primary')
    if btnadd:
        url = f"http://localhost:8000/company_employees?employee_id={emp_id}&employee_name={emp_name}&employee_position={emp_position}&employee_mail={emp_mail}"
        req = requests.post(url)
        if req.status_code==200:
            st.sidebar.success('Created Employee')
        else:
            st.error('Error') 

