import streamlit as st
import pandas as pd
import datetime
import os
import random
import smtplib
from email.message import EmailMessage
import hashlib
import shutil

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Marathe Group | Secure Portal", page_icon="🏢", layout="wide")

# ---------- EMAIL (OTP) CONFIG ----------
EMAIL_USER = "your_email@gmail.com"      # <-- replace
EMAIL_PASS = "your_app_password"         # <-- replace (App Password recommended)

def send_otp_via_email(receiver_email, purpose="Verification"):
    """Send OTP by email. Returns the OTP string or None on fail."""
    otp = str(random.randint(100000, 999999))
    msg = EmailMessage()
    msg['Subject'] = f"Marathe Group - {purpose} OTP"
    msg['From'] = EMAIL_USER
    msg['To'] = receiver_email
    msg.set_content(f"Your OTP for Marathe Group ({purpose}) is: {otp}\n\nIf you didn't request this, ignore.")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return otp
    except Exception as e:
        st.error("Failed to send OTP email — check EMAIL_USER, EMAIL_PASS and network.")
        st.error(f"SMTP error: {e}")
        return None

# ---------- PASSWORD HASHING ----------
def hash_password(plain):
    return hashlib.sha256(plain.encode('utf-8')).hexdigest()

def verify_password(plain, hashed):
    return hash_password(plain) == hashed

# ---------- FILES / STORAGE ----------
DATA_DIR = "."
ADMIN_FILE = os.path.join(DATA_DIR, "admins.xlsx")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.xlsx")
BOOKING_FILE = os.path.join(DATA_DIR, "bookings.xlsx")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# initialize files if missing
def ensure_xlsx(path, cols):
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_excel(path, index=False)

ensure_xlsx(ADMIN_FILE, ["Name", "Email", "PasswordHash", "Approved"])
ensure_xlsx(CUSTOMER_FILE, ["Name", "Email", "PasswordHash", "Project", "Approved"])
ensure_xlsx(BOOKING_FILE, ["CustomerEmail", "Project", "Date", "Status", "FileName", "FilePath"])

# ---------- SESSION OTP STORE ----------
if "otps" not in st.session_state:
    st.session_state["otps"] = {}  # maps email -> otp

# ---------- PROJECT DATA ----------
projects = {
    "Marathe Sapphire": {"img": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif", "price": "₹38–55 L"},
    "Marathe Tower": {"img": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true", "price": "₹32–45 L"},
    "Marathe Pride": {"img": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif", "price": "₹32–47 L"},
    "Marathe Elenza": {"img": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true", "price": "₹90 L – 1.2 Cr"}
}

# ---------- STYLE & HEADER ----------
st.markdown("""
<style>
body { background-color: #050505; color: #fff; }
h1,h2 { color: #FFD700; }
.card { background: linear-gradient(145deg,#121212,#0f0f0f); padding:15px; border-radius:12px; box-shadow:0 6px 18px rgba(255,215,0,0.08); }
.btn { background: linear-gradient(90deg,#FFD700,#ffb700); color: black; padding:8px 16px; border-radius:10px; font-weight:600; }
.small { color:#ccc; font-size:13px; }
.upload-note { color:#bbb; font-size:13px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;">
  <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true" width="180" style="border-radius:12px; box-shadow:0 6px 30px rgba(255,215,0,0.12);">
  <h1>Marathe Group</h1>
  <div class="small">Luxury Living • Trusted Legacy</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- LAYOUT: Sidebar Navigation ----------
menu = st.sidebar.selectbox("Menu", ["Home", "Customer Portal", "Admin Portal", "Contact"])

# ---------- HOME ----------
if menu == "Home":
    st.header("Our Projects")
    cols = st.columns(2)
    for i, (name, info) in enumerate(projects.items()):
        with cols[i % 2]:
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.image(info["img"], use_column_width=True)
            st.markdown(f"### <span style='color:#FFD700'>{name}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='small'>Price: {info['price']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("To book: go to Customer Portal → Register. Admin will verify your registration and enable your access to documents after booking.")

# ---------- CUSTOMER PORTAL ----------
elif menu == "Customer Portal":
    st.header("Customer Portal")
    df_customers = pd.read_excel(CUSTOMER_FILE)
    df_bookings = pd.read_excel(BOOKING_FILE)

    tab = st.tabs(["Register", "Login", "Forgot Password", "My Documents"])[0]  # We'll use st.tabs flow below

    tabs = st.tabs(["Register", "Login", "Forgot Password", "My Documents"])

    # ---- Register ----
    with tabs[0]:
        st.subheader("Register as Customer")
        name = st.text_input("Full Name", key="cust_reg_name")
        email = st.text_input("Email", key="cust_reg_email")
        password = st.text_input("Set Password", type="password", key="cust_reg_pass")
        project = st.selectbox("Project to Book", list(projects.keys()), key="cust_reg_proj")
        if st.button("Send OTP to verify email", key="cust_send_otp"):
            if not (name and email and password):
                st.error("Please fill name, email and password first.")
            else:
                otp = send_otp_via_email(email, purpose="Registration")
                if otp:
                    st.session_state["otps"][email] = otp
                    st.success("OTP sent. Enter the code below to complete registration.")
        otp_input = st.text_input("Enter OTP", key="cust_reg_otp")
        if st.button("Verify & Register", key="cust_verify"):
            if email in st.session_state["otps"]:
                if st.session_state["otps"][email] == otp_input:
                    # register user hashed password, mark Pending approval
                    hashed = hash_password(password)
                    df_customers.loc[len(df_customers)] = [name, email, hashed, project, "Pending"]
                    df_customers.to_excel(CUSTOMER_FILE, index=False)
                    st.success("Registration submitted. Wait for admin verification.")
                    st.session_state["otps"].pop(email, None)
                else:
                    st.error("OTP incorrect.")
            else:
                st.error("No OTP sent or expired. Click 'Send OTP' first.")

    # ---- Login ----
    with tabs[1]:
        st.subheader("Customer Login")
        email = st.text_input("Email", key="cust_login_email")
        password = st.text_input("Password", type="password", key="cust_login_pass")
        if st.button("Login", key="cust_login_btn"):
            user = df_customers[(df_customers["Email"] == email)]
            if not user.empty and verify_password(password, user.iloc[0]["PasswordHash"]):
                if user.iloc[0]["Approved"] == "Yes":
                    st.success(f"Welcome {user.iloc[0]['Name']}!")
                    # Show booking info & documents
                    my_docs = df_bookings[df_bookings["CustomerEmail"] == email]
                    st.subheader("My Bookings & Documents")
                    if not my_docs.empty:
                        for idx, row in my_docs.iterrows():
                            st.markdown(f"**Project:** {row['Project']}  —  **Status:** {row['Status']}  —  **Date:** {row['Date']}")
                            if pd.notna(row.get("FilePath")) and os.path.exists(str(row["FilePath"])):
                                file_path = str(row["FilePath"])
                                filename = os.path.basename(file_path)
                                with open(file_path, "rb") as f:
                                    st.download_button(f"Download {filename}", f, file_name=filename, key=f"dl_{idx}")
                            else:
                                st.markdown("_No documents uploaded yet._")
                    else:
                        st.info("No bookings or uploaded documents found (you can contact admin).")
                else:
                    st.warning("Your registration is pending approval by the office. Please wait.")
            else:
                st.error("Invalid login credentials.")

    # ---- Forgot Password ----
    with tabs[2]:
        st.subheader("Customer - Forgot Password")
        email_fp = st.text_input("Enter your registered email", key="cust_fp_email")
        if st.button("Send OTP for password reset", key="cust_fp_send"):
            user = df_customers[df_customers["Email"] == email_fp]
            if not user.empty:
                otp = send_otp_via_email(email_fp, purpose="Password Reset")
                if otp:
                    st.session_state["otps"][email_fp] = otp
                    st.success("OTP sent. Enter the OTP and set a new password below.")
            else:
                st.error("Email not registered.")
        otp_fp = st.text_input("Enter OTP", key="cust_fp_otp")
        new_pass = st.text_input("Enter new password", type="password", key="cust_fp_newpass")
        if st.button("Verify OTP & Reset Password", key="cust_fp_reset"):
            if email_fp in st.session_state["otps"] and st.session_state["otps"][email_fp] == otp_fp:
                # update password
                df_customers.loc[df_customers["Email"] == email_fp, "PasswordHash"] = hash_password(new_pass)
                df_customers.to_excel(CUSTOMER_FILE, index=False)
                st.success("Password reset successfully.")
                st.session_state["otps"].pop(email_fp, None)
            else:
                st.error("OTP incorrect or not sent.")

    # ---- My Documents (quick access if they are already logged in) ----
    with tabs[3]:
        st.subheader("My Documents (Quick access)")
        cust_email = st.text_input("Enter your registered email to view documents", key="cust_docs_email")
        if st.button("Show Documents", key="cust_docs_show"):
            user = df_customers[df_customers["Email"] == cust_email]
            if user.empty:
                st.error("Email not registered.")
            elif user.iloc[0]["Approved"] != "Yes":
                st.warning("Your account is not approved yet.")
            else:
                my_docs = pd.read_excel(BOOKING_FILE)
                my_docs = my_docs[my_docs["CustomerEmail"] == cust_email]
                if my_docs.empty:
                    st.info("No documents uploaded yet.")
                else:
                    for idx, row in my_docs.iterrows():
                        st.markdown(f"**Project:** {row['Project']}  •  **Date:** {row['Date']}  •  **Status:** {row['Status']}")
                        if pd.notna(row.get("FilePath")) and os.path.exists(str(row["FilePath"])):
                            fp = str(row["FilePath"])
                            with open(fp, "rb") as f:
                                st.download_button(f"Download {os.path.basename(fp)}", f, file_name=os.path.basename(fp), key=f"cdoc_{idx}")
                        else:
                            st.markdown("_No file uploaded._")

# ---------- ADMIN PORTAL ----------
elif menu == "Admin Portal":
    st.header("Admin Portal")
    df_admins = pd.read_excel(ADMIN_FILE)
    df_customers = pd.read_excel(CUSTOMER_FILE)
    df_bookings = pd.read_excel(BOOKING_FILE)

    tabs = st.tabs(["Register Admin", "Admin Login"])

    # ----- Admin Register -----
    with tabs[0]:
        st.subheader("Register Admin")
        name = st.text_input("Full Name", key="adm_reg_name")
        email = st.text_input("Official Email", key="adm_reg_email")
        password = st.text_input("Set Password", type="password", key="adm_reg_pass")
        if st.button("Send Admin OTP", key="adm_reg_send"):
            if not (name and email and password):
                st.error("Fill all fields first.")
            else:
                otp = send_otp_via_email(email, purpose="Admin Registration")
                if otp:
                    st.session_state["otps"][email] = otp
                    st.success("OTP sent to admin email.")
        otp_admin = st.text_input("Enter OTP", key="adm_reg_otp")
        if st.button("Verify & Register Admin", key="adm_reg_verify"):
            if email in st.session_state["otps"] and st.session_state["otps"][email] == otp_admin:
                df_admins.loc[len(df_admins)] = [name, email, hash_password(password), "Pending"]
                df_admins.to_excel(ADMIN_FILE, index=False)
                st.success("Admin registered. Office will verify.")
                st.session_state["otps"].pop(email, None)
            else:
                st.error("OTP wrong or not sent.")

    # ----- Admin Login -----
    with tabs[1]:
        email = st.text_input("Admin Email", key="adm_login_email")
        password = st.text_input("Password", type="password", key="adm_login_pass")
        if st.button("Admin Login", key="adm_login_btn"):
            admin = df_admins[df_admins["Email"] == email]
            if admin.empty or not verify_password(password, admin.iloc[0]["PasswordHash"]):
                st.error("Invalid admin credentials.")
            else:
                if admin.iloc[0]["Approved"] != "Yes":
                    st.warning("Admin account pending office approval.")
                else:
                    st.success(f"Welcome Admin {admin.iloc[0]['Name']}!")
                    # Admin actions: Approve customers, upload documents, view bookings
                    st.subheader("Pending Customer Approvals")
                    pending = df_customers[df_customers["Approved"] == "Pending"]
                    if not pending.empty:
                        for idx, row in pending.iterrows():
                            st.markdown(f"- {row['Name']}  •  {row['Email']}  •  Project: {row['Project']}")
                            if st.button(f"Approve {row['Email']}", key=f"approve_{idx}"):
                                df_customers.loc[df_customers["Email"] == row["Email"], "Approved"] = "Yes"
                                df_customers.to_excel(CUSTOMER_FILE, index=False)
                                st.success(f"Approved {row['Email']}")
                    else:
                        st.info("No pending customer registrations.")

                    st.markdown("---")
                    st.subheader("Upload Booking Documents for Customer")
                    approved_customers = df_customers[df_customers["Approved"] == "Yes"]
                    if approved_customers.empty:
                        st.info("No approved customers yet.")
                    else:
                        cust_email = st.selectbox("Select customer email", approved_customers["Email"].tolist(), key="adm_sel_cust")
                        project = st.selectbox("Select project", list(projects.keys()), key="adm_sel_proj")
                        uploaded_file = st.file_uploader("Choose file (pdf/jpg/png)", type=["pdf", "jpg", "png"], key="adm_file_up")
                        if uploaded_file and st.button("Upload Document", key="adm_upload_btn"):
                            # save file under uploads/{email}/filename
                            cust_dir = os.path.join(UPLOAD_DIR, cust_email.replace("@", "_at_"))
                            os.makedirs(cust_dir, exist_ok=True)
                            save_path = os.path.join(cust_dir, uploaded_file.name)
                            with open(save_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            # record in bookings
                            df_bookings.loc[len(df_bookings)] = [cust_email, project, datetime.datetime.now().strftime("%Y-%m-%d"), "Document Uploaded", uploaded_file.name, save_path]
                            df_bookings.to_excel(BOOKING_FILE, index=False)
                            st.success("Document uploaded and linked to customer.")

                    st.markdown("---")
                    st.subheader("All Bookings / Documents")
                    df_bookings = pd.read_excel(BOOKING_FILE)
                    if df_bookings.empty:
                        st.info("No bookings/documents uploaded yet.")
                    else:
                        st.dataframe(df_bookings)

# ---------- CONTACT ----------
elif menu == "Contact":
    st.header("Contact")
    st.markdown("""
    **Office Address:** Marathe Group Office, Titwala (E), Maharashtra  
    **Working Hours:** 10:00 AM – 07:00 PM (Mon–Sun)  
    **Phone:** +91 7045871101  
    **Email:** marathegroup1101@gmail.com
    """)

# ---------- END ----------
st.markdown("---")
st.caption("© 2025 Marathe Group — Secure Portal")
