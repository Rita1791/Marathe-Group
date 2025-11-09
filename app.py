import streamlit as st
import pandas as pd
import datetime
import os

# --------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Marathe Group | Luxury Living", page_icon="🏢", layout="wide")

# --------------- HEADER ----------------
st.markdown("""
    <div style="text-align:center;">
        <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true"
             width="200" style="border-radius:20px; margin-bottom:15px;">
        <h1 style="color:#FFD700;">🏢 Marathe Group</h1>
        <h4 style="color:#ccc;">Luxury Living • Trusted Legacy</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --------------- MISSION ----------------
st.markdown("""
<div style='background: linear-gradient(135deg, #1c1c1c, #111); padding: 40px; border-radius: 15px;'>
<h2 style='text-align:center; color:#FFD700;'>🌟 Our Mission & Vision</h2>
<p style='font-size:18px; text-align:center; color:#f0f0f0;'>
To build homes that redefine comfort, design excellence, and trust.
Marathe Group is committed to crafting modern living experiences rooted in quality and transparency.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------- PROJECT DATA -----------------
projects = {
    "Marathe Sapphire": {"price": "₹38–55 Lakh", "location": "Titwala (E)", "status": "Ongoing"},
    "Marathe Tower": {"price": "₹32–45 Lakh", "location": "Titwala (E)", "status": "Ongoing"},
    "Marathe Pride": {"price": "₹32–47 Lakh", "location": "Ambernath (E)", "status": "Ongoing"},
    "Marathe Elenza": {"price": "₹90 Lakh – 1.2 Cr", "location": "Shahad (W)", "status": "Completed"},
}

# ----------------- DATABASE INITIALIZATION -----------------
admin_file = "admins.xlsx"
customer_file = "customers.xlsx"
booking_file = "bookings.xlsx"

for file, columns in [
    (admin_file, ["Name", "Email", "Password", "Approved"]),
    (customer_file, ["Name", "Email", "Password", "Project", "Approved"]),
    (booking_file, ["CustomerEmail", "Project", "Date", "Status", "Documents"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=columns).to_excel(file, index=False)

# ----------------- MAIN NAVIGATION -----------------
menu = st.sidebar.radio("Navigate", ["🏠 Home", "🧑‍💼 Admin Portal", "👤 Customer Portal", "📞 Contact"])

# ----------------- HOME -----------------
if menu == "🏠 Home":
    st.header("🏗️ Ongoing Projects")
    for name, data in projects.items():
        st.markdown(f"""
        ### {name}
        📍 Location: {data['location']}  
        💰 Price Range: {data['price']}  
        📊 Status: **{data['status']}**
        """)
        if st.button(f"Book {name}", key=f"book_{name}"):
            st.session_state["selected_project"] = name
            st.success(f"Please proceed to 'Customer Portal → Register' to book {name}")

# ----------------- ADMIN PORTAL -----------------
elif menu == "🧑‍💼 Admin Portal":
    st.header("🧑‍💼 Admin Dashboard")

    df_admins = pd.read_excel(admin_file)
    df_customers = pd.read_excel(customer_file)
    df_bookings = pd.read_excel(booking_file)

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # ADMIN LOGIN
    with tab1:
        email = st.text_input("Admin Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = df_admins[(df_admins["Email"] == email) & (df_admins["Password"] == password)]
            if not user.empty and user.iloc[0]["Approved"] == "Yes":
                st.success(f"Welcome Admin {user.iloc[0]['Name']} 👋")
                st.subheader("📋 Customer Registrations Pending Approval")
                pending = df_customers[df_customers["Approved"] == "Pending"]
                if not pending.empty:
                    for idx, row in pending.iterrows():
                        st.markdown(f"🧍 {row['Name']} | {row['Email']} | Project: {row['Project']}")
                        if st.button(f"Approve {row['Email']}"):
                            df_customers.loc[df_customers["Email"] == row["Email"], "Approved"] = "Yes"
                            df_customers.to_excel(customer_file, index=False)
                            st.success(f"✅ Approved {row['Email']}")
                else:
                    st.info("No pending customers.")
                
                st.subheader("📄 Upload Customer Documents")
                cust_email = st.selectbox("Select Customer", df_customers[df_customers["Approved"] == "Yes"]["Email"].tolist())
                project = st.selectbox("Select Project", list(projects.keys()))
                file = st.file_uploader("Upload Document (PDF/Receipt/Agreement)", type=["pdf", "jpg", "png"])
                if file and st.button("Upload Document"):
                    df_bookings.loc[len(df_bookings)] = [cust_email, project, datetime.datetime.now().strftime("%Y-%m-%d"), "Document Uploaded", file.name]
                    df_bookings.to_excel(booking_file, index=False)
                    st.success(f"📁 Uploaded {file.name} for {cust_email}")

            elif not user.empty:
                st.warning("⏳ Account pending office approval.")
            else:
                st.error("❌ Invalid credentials or access denied.")

    # ADMIN REGISTER
    with tab2:
        name = st.text_input("Full Name", key="admin_name")
        email = st.text_input("Official Email", key="admin_email")
        password = st.text_input("Set Password", type="password", key="admin_pass")
        if st.button("Register Admin"):
            if name and email and password:
                df_admins.loc[len(df_admins)] = [name, email, password, "Pending"]
                df_admins.to_excel(admin_file, index=False)
                st.success("✅ Registration submitted. Wait for office verification.")
            else:
                st.error("All fields are required.")

# ----------------- CUSTOMER PORTAL -----------------
elif menu == "👤 Customer Portal":
    st.header("👤 Customer Dashboard")

    df_customers = pd.read_excel(customer_file)
    df_bookings = pd.read_excel(booking_file)

    tab1, tab2 = st.tabs(["📝 Register", "🔑 Login"])

    # CUSTOMER REGISTER
    with tab1:
        name = st.text_input("Full Name", key="cust_name")
        email = st.text_input("Email", key="cust_email")
        password = st.text_input("Password", type="password", key="cust_pass")
        project = st.selectbox("Select Project", list(projects.keys()))
        if st.button("Register"):
            df_customers.loc[len(df_customers)] = [name, email, password, project, "Pending"]
            df_customers.to_excel(customer_file, index=False)
            st.success("✅ Registration submitted. You will be verified soon.")

    # CUSTOMER LOGIN
    with tab2:
        email = st.text_input("Email", key="cust_login_email")
        password = st.text_input("Password", type="password", key="cust_login_pass")
        if st.button("Login"):
            user = df_customers[(df_customers["Email"] == email) & (df_customers["Password"] == password)]
            if not user.empty and user.iloc[0]["Approved"] == "Yes":
                st.success(f"Welcome {user.iloc[0]['Name']} 👋")
                cust_docs = df_bookings[df_bookings["CustomerEmail"] == email]
                if not cust_docs.empty:
                    for idx, row in cust_docs.iterrows():
                        st.markdown(f"""
                        📁 **Project:** {row['Project']}  
                        📅 **Date:** {row['Date']}  
                        🧾 **Document:** {row['Documents']}
                        """)
                else:
                    st.info("No documents uploaded yet.")
            elif not user.empty:
                st.warning("⏳ Awaiting verification from office.")
            else:
                st.error("❌ Invalid credentials.")

# ----------------- CONTACT -----------------
elif menu == "📞 Contact":
    st.header("📞 Contact Us")
    st.markdown("""
    📍 **Address:** Marathe Group Office, Titwala (E), Maharashtra  
    📞 **Phone:** +91 7045871101  
    💬 [Chat on WhatsApp](https://wa.me/917045871101)  
    ✉️ **Email:** marathegroup1101@gmail.com  
    👤 **Owner:** Parasana Ramesh Marathe  
    """)
    st.caption("© 2025 Marathe Group | Designed & Developed by Ritika Rawat 💻")
