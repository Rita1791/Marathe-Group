# app.py
import streamlit as st
import pandas as pd
import datetime
import os
import random
import smtplib
from email.message import EmailMessage
import hashlib
import time
import json

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Marathe Group | Secure Portal", page_icon="🏢", layout="wide")

# ---------- USER CONFIG ----------
# Replace with your SMTP sender email and app password (Gmail app password recommended)
EMAIL_USER = st.secrets.get("EMAIL_USER", "")   # put in Streamlit Cloud secrets (recommended)
EMAIL_PASS = st.secrets.get("EMAIL_PASS", "")   # put in Streamlit Cloud secrets

# Optional Google Sheets sync (set SERVICE_ACCOUNT_JSON in secrets or provide file path)
GOOGLE_SHEETS_ENABLED = False  # set to True to enable

# OTP settings
OTP_EXPIRY_SECONDS = 300      # 5 minutes
OTP_RATE_LIMIT_WINDOW = 300   # seconds window to limit sends
OTP_RATE_LIMIT_MAX = 5        # max OTP sends per email per window

# Storage paths
DATA_DIR = "."
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_FILE = os.path.join(DATA_DIR, "admins.xlsx")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.xlsx")
BOOKING_FILE = os.path.join(DATA_DIR, "bookings.xlsx")

# initialize files if missing
def ensure_xlsx(path, cols):
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_excel(path, index=False)

ensure_xlsx(ADMIN_FILE, ["Name", "Email", "PasswordHash", "Approved", "CreatedAt"])
ensure_xlsx(CUSTOMER_FILE, ["Name", "Email", "PasswordHash", "Project", "Approved", "CreatedAt"])
ensure_xlsx(BOOKING_FILE, ["CustomerEmail", "Project", "Date", "Status", "FileName", "FilePath"])

# ---------- OTP store & rate limit in session ----------
if "otp_store" not in st.session_state:
    # otp_store: { email: {"otp": "...", "ts": 1234567890 } }
    st.session_state["otp_store"] = {}

if "otp_rate" not in st.session_state:
    # otp_rate: { email: [timestamp1, timestamp2, ...] }
    st.session_state["otp_rate"] = {}

# ---------- Password helpers ----------
def hash_password(plain):
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()

def verify_password(plain, hashed):
    return hash_password(plain) == hashed

# ---------- Email (HTML OTP) ----------
def send_otp_email(receiver_email, otp, purpose="Verification"):
    """
    Sends a nice HTML OTP email. Uses EMAIL_USER and EMAIL_PASS.
    Returns True on success.
    """
    if not EMAIL_USER or not EMAIL_PASS:
        st.error("EMAIL_USER / EMAIL_PASS not configured. Put them in Streamlit secrets.")
        return False
    msg = EmailMessage()
    msg["Subject"] = f"Marathe Group — {purpose} OTP"
    msg["From"] = EMAIL_USER
    msg["To"] = receiver_email

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color:#111;">
        <div style="max-width:600px; margin:auto; padding:20px; border-radius:10px; background:linear-gradient(180deg,#fff,#f7f7f7);">
          <h2 style="color:#b8860b; margin:0 0 10px 0;">Marathe Group — OTP</h2>
          <p style="margin:8px 0;">Hello,</p>
          <p style="margin:8px 0;">Your <strong>{purpose}</strong> OTP is:</p>
          <div style="font-size:28px; font-weight:700; color:#000; letter-spacing:4px; margin:12px 0;">{otp}</div>
          <p style="font-size:13px; color:#444; margin:8px 0;">This code will expire in {OTP_EXPIRY_SECONDS//60} minutes. If you didn't request this, ignore this email.</p>
          <hr>
          <p style="font-size:12px; color:#666; margin:6px 0;">Marathe Group • Trusted Legacy</p>
        </div>
      </body>
    </html>
    """
    msg.add_alternative(html, subtype="html")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"SMTP send failed: {e}")
        return False

# ---------- OTP helpers ----------
def can_send_otp(email):
    """Simple rate-limit check"""
    now = time.time()
    events = st.session_state["otp_rate"].get(email, [])
    # drop older than window
    events = [t for t in events if now - t <= OTP_RATE_LIMIT_WINDOW]
    st.session_state["otp_rate"][email] = events
    return len(events) < OTP_RATE_LIMIT_MAX

def store_otp(email, otp):
    st.session_state["otp_store"][email] = {"otp": otp, "ts": time.time()}
    st.session_state["otp_rate"].setdefault(email, []).append(time.time())

def verify_and_consume_otp(email, otp):
    rec = st.session_state["otp_store"].get(email)
    if not rec:
        return False, "No OTP sent"
    if time.time() - rec["ts"] > OTP_EXPIRY_SECONDS:
        st.session_state["otp_store"].pop(email, None)
        return False, "OTP expired"
    if rec["otp"] != otp:
        return False, "Incorrect OTP"
    # valid:
    st.session_state["otp_store"].pop(email, None)
    return True, "OK"

# ---------- Optional: Google Sheets sync (outline) ----------
def sync_row_to_google_sheets(sheet_name, row_values):
    """
    Optional: sync a row to Google Sheets.
    To enable:
      - set GOOGLE_SHEETS_ENABLED = True
      - add service account JSON contents into st.secrets["GSPREAD_SERVICE_ACCOUNT"] as a JSON string
    """
    if not GOOGLE_SHEETS_ENABLED:
        return False
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        creds_json = st.secrets.get("GSPREAD_SERVICE_ACCOUNT")
        if not creds_json:
            st.error("Google Sheets service account not found in secrets.")
            return False
        creds_dict = json.loads(creds_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        sheet.append_row(row_values)
        return True
    except Exception as e:
        st.error(f"Google Sheets sync failed: {e}")
        return False

# ---------- PROJECT DATA ----------
projects = {
    "Marathe Sapphire": {"img": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif", "price": "₹38–55 Lakh"},
    "Marathe Tower": {"img": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true", "price": "₹32–45 Lakh"},
    "Marathe Pride": {"img": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif", "price": "₹32–47 Lakh"},
    "Marathe Elenza": {"img": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true", "price": "₹90 L – 1.2 Cr"},
}

# ---------- STYLE & HEADER ----------
st.markdown("""
<style>
body { background-color: #050505; color: #fff; }
h1,h2 { color: #FFD700; }
.card { background: linear-gradient(145deg,#121212,#0f0f0f); padding:15px; border-radius:12px; box-shadow:0 6px 18px rgba(255,215,0,0.08); }
.carousel { width:100%; max-width:1100px; margin:auto; }
.carousel img { width:100%; height:320px; object-fit:cover; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.6); }
.btn { background: linear-gradient(90deg,#FFD700,#ffb700); color: black; padding:8px 16px; border-radius:10px; font-weight:600; }
.small { color:#ccc; font-size:13px; }
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

# ---------- Image carousel (simple) ----------
carousel_images = [projects[k]["img"] for k in projects]
carousel_html = "<div class='carousel'>"
for src in carousel_images:
    carousel_html += f"<img src='{src}'/>"
carousel_html += "</div>"
# Show carousel images stacked (browser will show all; simple effect). For advanced carousel, JS would be needed.
st.markdown(carousel_html, unsafe_allow_html=True)
st.markdown("---")

# ---------- Sidebar navigation ----------
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
    st.info("To book: go to Customer Portal → Register. Admin will verify your registration and enable document access after booking.")

# ---------- CUSTOMER PORTAL ----------
elif menu == "Customer Portal":
    st.header("Customer Portal")
    df_customers = pd.read_excel(CUSTOMER_FILE)
    df_bookings = pd.read_excel(BOOKING_FILE)

    tabs = st.tabs(["Register", "Login", "Forgot Password", "My Documents"])

    # ---- Register ----
    with tabs[0]:
        st.subheader("Register")
        name = st.text_input("Full Name", key="cust_reg_name")
        email = st.text_input("Email", key="cust_reg_email")
        password = st.text_input("Set Password", type="password", key="cust_reg_pass")
        project = st.selectbox("Project to Book", list(projects.keys()), key="cust_reg_proj")
        if st.button("Send OTP", key="cust_send_otp"):
            if not (name and email and password):
                st.error("Fill Name, Email and Password first")
            else:
                if not can_send_otp(email):
                    st.error("Too many OTP requests. Try again later.")
                else:
                    otp = str(random.randint(100000, 999999))
                    ok = send_otp_email(email, otp, purpose="Customer Registration")
                    if ok:
                        store_otp(email, otp)
                        st.success("OTP sent to your email. Enter it below.")
        otp_input = st.text_input("Enter OTP", key="cust_reg_otp")
        if st.button("Verify & Register", key="cust_verify"):
            ok, msg = verify_and_consume_otp(email, otp_input)
            if ok:
                hashed = hash_password(password)
                df_customers.loc[len(df_customers)] = [name, email, hashed, project, "Pending", datetime.datetime.now().isoformat()]
                df_customers.to_excel(CUSTOMER_FILE, index=False)
                # optional sheets
                if GOOGLE_SHEETS_ENABLED:
                    sync_row_to_google_sheets("MaratheRegistry", [name, email, project, "Pending", datetime.datetime.now().isoformat()])
                st.success("Registered. Await admin approval.")
            else:
                st.error(msg)

    # ---- Login ----
    with tabs[1]:
        st.subheader("Login")
        email = st.text_input("Email", key="cust_login_email")
        password = st.text_input("Password", type="password", key="cust_login_pass")
        if st.button("Login", key="cust_login_btn"):
            user = df_customers[df_customers["Email"] == email]
            if user.empty:
                st.error("Email not registered.")
            else:
                if verify_password(password, user.iloc[0]["PasswordHash"]):
                    if user.iloc[0]["Approved"] == "Yes":
                        st.success(f"Welcome {user.iloc[0]['Name']}")
                        # show bookings/documents
                        my_docs = df_bookings[df_bookings["CustomerEmail"] == email]
                        st.subheader("My Bookings & Documents")
                        if my_docs.empty:
                            st.info("No documents yet; contact office.")
                        else:
                            for idx, row in my_docs.iterrows():
                                st.markdown(f"**{row['Project']}** — {row['Status']} ({row['Date']})")
                                fp = row.get("FilePath")
                                if pd.notna(fp) and os.path.exists(str(fp)):
                                    with open(fp, "rb") as f:
                                        st.download_button(f"Download {row['FileName']}", f, file_name=row['FileName'], key=f"dl_{idx}")
                                else:
                                    st.markdown("_No file available._")
                    else:
                        st.warning("Registration pending admin approval.")
                else:
                    st.error("Incorrect password.")

    # ---- Forgot Password ----
    with tabs[2]:
        st.subheader("Forgot Password")
        fp_email = st.text_input("Enter your registered email", key="fp_email")
        if st.button("Send OTP for Reset", key="fp_send"):
            user = df_customers[df_customers["Email"] == fp_email]
            if user.empty:
                st.error("Email not registered.")
            else:
                if not can_send_otp(fp_email):
                    st.error("Too many OTP requests. Try later.")
                else:
                    otp = str(random.randint(100000, 999999))
                    if send_otp_email(fp_email, otp, purpose="Password Reset"):
                        store_otp(fp_email, otp)
                        st.success("OTP sent. Enter below.")
        fp_otp = st.text_input("Enter OTP", key="fp_otp")
        new_pass = st.text_input("New Password", type="password", key="fp_newpass")
        if st.button("Verify & Reset", key="fp_reset"):
            ok, msg = verify_and_consume_otp(fp_email, fp_otp)
            if ok:
                df_customers.loc[df_customers["Email"] == fp_email, "PasswordHash"] = hash_password(new_pass)
                df_customers.to_excel(CUSTOMER_FILE, index=False)
                st.success("Password reset successful.")
            else:
                st.error(msg)

    # ---- My Documents ----
    with tabs[3]:
        st.subheader("My Documents")
        doc_email = st.text_input("Enter your approved email", key="md_email")
        if st.button("Show Documents", key="md_show"):
            user = df_customers[df_customers["Email"] == doc_email]
            if user.empty:
                st.error("Email not registered.")
            elif user.iloc[0]["Approved"] != "Yes":
                st.warning("Not approved yet.")
            else:
                my_docs = pd.read_excel(BOOKING_FILE)
                my_docs = my_docs[my_docs["CustomerEmail"] == doc_email]
                if my_docs.empty:
                    st.info("No documents.")
                else:
                    for idx, row in my_docs.iterrows():
                        st.markdown(f"**{row['Project']}** — {row['Status']} ({row['Date']})")
                        fp = row.get("FilePath")
                        if pd.notna(fp) and os.path.exists(str(fp)):
                            with open(str(fp), "rb") as f:
                                st.download_button(f"Download {row['FileName']}", f, file_name=row['FileName'], key=f"md_dl_{idx}")
                        else:
                            st.markdown("_No file uploaded._")

# ---------- ADMIN PORTAL ----------
elif menu == "Admin Portal":
    st.header("Admin Portal")
    df_admins = pd.read_excel(ADMIN_FILE)
    df_customers = pd.read_excel(CUSTOMER_FILE)
    df_bookings = pd.read_excel(BOOKING_FILE)

    tabs = st.tabs(["Register Admin", "Admin Login"])

    # Register admin (with OTP)
    with tabs[0]:
        st.subheader("Register Admin")
        aname = st.text_input("Full Name", key="adm_reg_name")
        aemail = st.text_input("Official Email", key="adm_reg_email")
        apass = st.text_input("Set Password", type="password", key="adm_reg_pass")
        if st.button("Send OTP to Admin Email", key="adm_send"):
            if not (aname and aemail and apass):
                st.error("Fill all fields.")
            else:
                if not can_send_otp(aemail):
                    st.error("Too many OTP requests.")
                else:
                    otp = str(random.randint(100000, 999999))
                    if send_otp_email(aemail, otp, purpose="Admin Registration"):
                        store_otp(aemail, otp)
                        st.success("OTP sent.")
        adm_otp = st.text_input("Enter OTP", key="adm_otp")
        if st.button("Verify & Register Admin", key="adm_verify"):
            ok, msg = verify_and_consume_otp(aemail, adm_otp)
            if ok:
                df_admins.loc[len(df_admins)] = [aname, aemail, hash_password(apass), "Pending", datetime.datetime.now().isoformat()]
                df_admins.to_excel(ADMIN_FILE, index=False)
                st.success("Admin registered. Office must approve.")
            else:
                st.error(msg)

    # Admin Login and dashboard
    with tabs[1]:
        aemail_login = st.text_input("Admin Email", key="adm_login_email")
        apass_login = st.text_input("Password", type="password", key="adm_login_pass")
        if st.button("Admin Login", key="adm_login_btn"):
            adm = df_admins[df_admins["Email"] == aemail_login]
            if adm.empty:
                st.error("Admin not registered.")
            elif not verify_password(apass_login, adm.iloc[0]["PasswordHash"]):
                st.error("Incorrect password.")
            elif adm.iloc[0]["Approved"] != "Yes":
                st.warning("Admin account pending verification.")
            else:
                st.success(f"Welcome Admin {adm.iloc[0]['Name']}")
                st.subheader("Pending Customer Approvals")
                pending = df_customers[df_customers["Approved"] == "Pending"]
                if not pending.empty:
                    for idx, row in pending.iterrows():
                        st.markdown(f"- {row['Name']} • {row['Email']} • {row['Project']}")
                        if st.button(f"Approve {row['Email']}", key=f"approve_{idx}"):
                            df_customers.loc[df_customers["Email"] == row["Email"], "Approved"] = "Yes"
                            df_customers.to_excel(CUSTOMER_FILE, index=False)
                            st.success(f"Approved {row['Email']}")
                else:
                    st.info("No pending customers.")

                st.markdown("---")
                st.subheader("Upload Document for Customer")
                approved = df_customers[df_customers["Approved"] == "Yes"]
                if not approved.empty:
                    cust_email = st.selectbox("Select Customer", approved["Email"].tolist(), key="adm_cust_sel")
                    proj = st.selectbox("Project", list(projects.keys()), key="adm_proj_sel")
                    uploaded = st.file_uploader("Upload file (pdf/jpg/png)", type=["pdf", "jpg", "png"], key="adm_file")
                    if uploaded and st.button("Upload Document", key="adm_upload_btn"):
                        cust_dir = os.path.join(UPLOAD_DIR, cust_email.replace("@", "_at_"))
                        os.makedirs(cust_dir, exist_ok=True)
                        save_path = os.path.join(cust_dir, uploaded.name)
                        with open(save_path, "wb") as f:
                            f.write(uploaded.getbuffer())
                        df_bookings.loc[len(df_bookings)] = [cust_email, proj, datetime.datetime.now().strftime("%Y-%m-%d"), "Document Uploaded", uploaded.name, save_path]
                        df_bookings.to_excel(BOOKING_FILE, index=False)
                        st.success("Uploaded and linked to customer.")
                        # optional sheets sync
                        if GOOGLE_SHEETS_ENABLED:
                            sync_row_to_google_sheets("MaratheBookings", [cust_email, proj, datetime.datetime.now().strftime("%Y-%m-%d"), "Uploaded", uploaded.name])
                else:
                    st.info("No approved customers.")

                st.markdown("---")
                st.subheader("All Bookings")
                st.dataframe(pd.read_excel(BOOKING_FILE))

# ---------- CONTACT ----------
elif menu == "Contact":
    st.header("Contact Us")
    st.markdown("""
    **Office Address:** Marathe Group Office, Titwala (E), Maharashtra  
    **Working Hours:** 10:00 AM – 07:00 PM (Mon–Sun)  
    **Phone:** +91 7045871101  
    **Email:** marathegroup1101@gmail.com
    """)

st.markdown("---")
st.caption("© 2025 Marathe Group — Secure Portal")
