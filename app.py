import streamlit as st
import pandas as pd
import datetime
import os
import random
import smtplib
from email.message import EmailMessage

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Marathe Group | Luxury Living", page_icon="🏢", layout="wide")

# ----------------- EMAIL CONFIG (OTP) -----------------
EMAIL_USER = "your_email@gmail.com"  # Replace with your sender email
EMAIL_PASS = "your_app_password"     # Replace with your App Password (from Google)

def send_otp(receiver_email):
    otp = str(random.randint(100000, 999999))
    msg = EmailMessage()
    msg['Subject'] = "Marathe Group OTP Verification"
    msg['From'] = EMAIL_USER
    msg['To'] = receiver_email
    msg.set_content(f"Dear User,\n\nYour OTP for Marathe Group verification is: {otp}\n\nPlease do not share this code.\n\nBest,\nMarathe Group Team")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return otp
    except:
        st.error("❌ Failed to send OTP. Check your email credentials or network.")
        return None

# ----------------- HEADER -----------------
st.markdown("""
    <div style="text-align:center;">
        <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true"
             width="200" style="border-radius:20px; margin-bottom:15px;">
        <h1 style="color:#FFD700;">🏢 Marathe Group</h1>
        <h4 style="color:#ccc;">Luxury Living • Trusted Legacy</h4>
    </div>
""", unsafe_allow_html=True)

# ----------------- STYLE -----------------
st.markdown("""
<style>
body {background-color: #0d0d0d; color: white;}
h1, h2, h3 {color: #FFD700;}
.card {
    background: linear-gradient(145deg, #1a1a1a, #111);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 0px 20px rgba(255,215,0,0.2);
    margin-bottom: 30px;
}
.card:hover {transform: scale(1.02);}
.btn {
    background: linear-gradient(90deg, #FFD700, #ffb700);
    color: black;
    padding: 10px 20px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------- FILE SETUP -----------------
admin_file = "admins.xlsx"
customer_file = "customers.xlsx"
booking_file = "bookings.xlsx"
for f, cols in [(admin_file, ["Name", "Email", "Password", "Approved"]),
                (customer_file, ["Name", "Email", "Password", "Project", "Approved"]),
                (booking_file, ["CustomerEmail", "Project", "Date", "Status", "Documents"])]:
    if not os.path.exists(f):
        pd.DataFrame(columns=cols).to_excel(f, index=False)

# ----------------- PROJECTS -----------------
projects = {
    "Marathe Sapphire": {
        "img": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif",
        "price": "₹38–55 Lakh", "loc": "Titwala (E)"
    },
    "Marathe Tower": {
        "img": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true",
        "price": "₹32–45 Lakh", "loc": "Titwala (E)"
    },
    "Marathe Pride": {
        "img": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif",
        "price": "₹32–47 Lakh", "loc": "Ambernath (E)"
    },
    "Marathe Elenza": {
        "img": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true",
        "price": "₹90 Lakh – 1.2 Cr", "loc": "Shahad (W)"
    }
}

# ----------------- NAVIGATION -----------------
menu = st.sidebar.radio("Navigate", ["🏠 Home", "👤 Customer Portal", "🧑‍💼 Admin Portal", "📞 Contact"])

# ----------------- HOME -----------------
if menu == "🏠 Home":
    st.markdown("<h2 style='text-align:center;'>🏗️ Our Projects</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (name, p) in enumerate(projects.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='card'>
                <img src='{p["img"]}' width='100%' style='border-radius:10px;'>
                <h3 style='text-align:center;'>{name}</h3>
                <p style='text-align:center;'>📍 {p["loc"]}<br>💰 {p["price"]}</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- CUSTOMER PORTAL -----------------
elif menu == "👤 Customer Portal":
    st.header("👤 Customer Portal")
    df_customers = pd.read_excel(customer_file)
    df_bookings = pd.read_excel(booking_file)

    tabs = st.tabs(["📝 Register", "🔑 Login"])

    with tabs[0]:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Set Password", type="password")
        project = st.selectbox("Select Project", list(projects.keys()))
        if st.button("Send OTP"):
            otp = send_otp(email)
            if otp:
                user_otp = st.text_input("Enter OTP")
                if st.button("Verify OTP"):
                    if user_otp == otp:
                        df_customers.loc[len(df_customers)] = [name, email, password, project, "Pending"]
                        df_customers.to_excel(customer_file, index=False)
                        st.success("✅ Registration complete! Await admin verification.")
                    else:
                        st.error("❌ Incorrect OTP.")

    with tabs[1]:
        email = st.text_input("Email", key="cust_login_email")
        password = st.text_input("Password", type="password", key="cust_login_pass")
        if st.button("Login"):
            user = df_customers[(df_customers["Email"] == email) & (df_customers["Password"] == password)]
            if not user.empty and user.iloc[0]["Approved"] == "Yes":
                st.success(f"Welcome {user.iloc[0]['Name']} 👋")
                docs = df_bookings[df_bookings["CustomerEmail"] == email]
                if not docs.empty:
                    st.subheader("📄 Your Documents")
                    for _, d in docs.iterrows():
                        st.write(f"🏢 {d['Project']} | 📅 {d['Date']} | 📁 {d['Documents']}")
                else:
                    st.info("No documents yet uploaded.")
            elif not user.empty:
                st.warning("⏳ Awaiting office verification.")
            else:
                st.error("❌ Invalid credentials.")

# ----------------- ADMIN PORTAL -----------------
elif menu == "🧑‍💼 Admin Portal":
    st.header("🧑‍💼 Admin Portal")
    df_admins = pd.read_excel(admin_file)
    df_customers = pd.read_excel(customer_file)
    df_bookings = pd.read_excel(booking_file)

    tabs = st.tabs(["📝 Register", "🔑 Login"])

    with tabs[0]:
        name = st.text_input("Full Name", key="admin_name")
        email = st.text_input("Email", key="admin_email")
        password = st.text_input("Password", type="password", key="admin_pass")
        if st.button("Send Admin OTP"):
            otp = send_otp(email)
            if otp:
                user_otp = st.text_input("Enter OTP to Verify")
                if st.button("Verify Admin OTP"):
                    if user_otp == otp:
                        df_admins.loc[len(df_admins)] = [name, email, password, "Pending"]
                        df_admins.to_excel(admin_file, index=False)
                        st.success("✅ Admin registration pending verification.")
                    else:
                        st.error("❌ Incorrect OTP.")

    with tabs[1]:
        email = st.text_input("Admin Email", key="admin_login_email")
        password = st.text_input("Password", type="password", key="admin_login_pass")
        if st.button("Login Admin"):
            admin = df_admins[(df_admins["Email"] == email) & (df_admins["Password"] == password)]
            if not admin.empty and admin.iloc[0]["Approved"] == "Yes":
                st.success(f"Welcome Admin {admin.iloc[0]['Name']}")
                st.subheader("📋 Pending Customer Approvals")
                pending = df_customers[df_customers["Approved"] == "Pending"]
                for _, c in pending.iterrows():
                    st.markdown(f"🧍 {c['Name']} ({c['Email']}) — {c['Project']}")
                    if st.button(f"Approve {c['Email']}"):
                        df_customers.loc[df_customers["Email"] == c["Email"], "Approved"] = "Yes"
                        df_customers.to_excel(customer_file, index=False)
                        st.success(f"✅ Approved {c['Email']}")
                st.subheader("📄 Upload Booking Documents")
                cust_email = st.selectbox("Select Customer", df_customers[df_customers["Approved"] == "Yes"]["Email"].tolist())
                project = st.selectbox("Project", list(projects.keys()))
                file = st.file_uploader("Upload Document (PDF/Image)", type=["pdf", "jpg", "png"])
                if file and st.button("Upload"):
                    df_bookings.loc[len(df_bookings)] = [cust_email, project, datetime.datetime.now().strftime("%Y-%m-%d"), "Uploaded", file.name]
                    df_bookings.to_excel(booking_file, index=False)
                    st.success("📁 Document uploaded successfully.")
            elif not admin.empty:
                st.warning("⏳ Pending office verification.")
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
