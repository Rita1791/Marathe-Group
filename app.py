# app.py - Marathe Group (Professional)
import streamlit as st
import pandas as pd
import datetime
import os
import random
import smtplib
from email.message import EmailMessage
import bcrypt
import time
import hashlib

# ---------------- Page config ----------------
st.set_page_config(page_title="Marathe Group — Luxury Living", page_icon="🏢", layout="wide")

# ----------------- Constants & Paths -----------------
DATA_DIR = "."
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_FILE = os.path.join(DATA_DIR, "admins.xlsx")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.xlsx")
BOOKING_FILE = os.path.join(DATA_DIR, "bookings.xlsx")

# OTP / security settings
OTP_EXPIRY_SECONDS = 300   # 5 minutes
OTP_MAX_PER_WINDOW = 5
OTP_WINDOW_SECONDS = 300

# defaults used (you can change)
OFFICE_ADDRESS = "Swami Vivekanand Chowk, Titwala (E), Maharashtra"
SENDER_EMAIL = st.secrets.get("EMAIL_USER", "")
SENDER_PASS = st.secrets.get("EMAIL_PASS", "")

# ----------------- Helpers: storage init -----------------
def ensure(path, cols):
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_excel(path, index=False)

ensure(ADMIN_FILE, ["Name","Email","PasswordHash","Approved","CreatedAt"])
ensure(CUSTOMER_FILE, ["Name","Email","PasswordHash","Project","Approved","CreatedAt"])
ensure(BOOKING_FILE, ["CustomerEmail","Project","Date","Status","FileName","FilePath"])

# ----------------- Session stores -----------------
if "otp_store" not in st.session_state:
    # { email: {"otp": "...", "ts": epoch } }
    st.session_state.otp_store = {}
if "otp_rate" not in st.session_state:
    st.session_state.otp_rate = {}  # { email: [timestamps] }

# ----------------- Utility: bcrypt password helpers -----------------
def hash_password_bcrypt(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password_bcrypt(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False

# ----------------- Utility: send OTP via SMTP (HTML) -----------------
def send_otp_email(recipient: str, otp: str, purpose: str = "Verification") -> bool:
    if not SENDER_EMAIL or not SENDER_PASS:
        st.error("Email sender not configured. Add EMAIL_USER and EMAIL_PASS to Streamlit secrets.")
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Marathe Group — {purpose} OTP"
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        html = f"""
        <html>
          <body style="font-family:Arial,Helvetica,sans-serif;color:#111;">
            <div style="padding:20px;border-radius:10px;background:#fff;">
              <h2 style="color:#b8860b;margin:0">Marathe Group — {purpose} OTP</h2>
              <p>Hello,</p>
              <p>Your OTP is:</p>
              <div style="font-size:28px;font-weight:700;color:#000">{otp}</div>
              <p style="color:#555">This OTP expires in {OTP_EXPIRY_SECONDS//60} minutes. If you did not request this, ignore.</p>
              <hr/>
              <small style="color:#777">Marathe Group • {OFFICE_ADDRESS}</small>
            </div>
          </body>
        </html>
        """
        msg.add_alternative(html, subtype="html")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send OTP email: {e}")
        return False

# ----------------- OTP helpers -----------------
def can_send_otp(email: str) -> bool:
    now = time.time()
    events = st.session_state.otp_rate.get(email, [])
    # prune
    events = [t for t in events if now - t <= OTP_WINDOW_SECONDS]
    st.session_state.otp_rate[email] = events
    return len(events) < OTP_MAX_PER_WINDOW

def store_otp(email: str, otp: str):
    st.session_state.otp_store[email] = {"otp": otp, "ts": time.time()}
    st.session_state.otp_rate.setdefault(email, []).append(time.time())

def verify_otp(email: str, otp: str):
    rec = st.session_state.otp_store.get(email)
    if not rec:
        return False, "No OTP requested."
    if time.time() - rec["ts"] > OTP_EXPIRY_SECONDS:
        st.session_state.otp_store.pop(email, None)
        return False, "OTP expired."
    if rec["otp"] != otp:
        return False, "Incorrect OTP."
    st.session_state.otp_store.pop(email, None)
    return True, "OK"

# ----------------- Projects data -----------------
projects = {
    "Marathe Sapphire": {
        "location": "Titwala (E)",
        "address": "Swami Vivekanand Chowk Road, Titwala East",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif",
        "price": "1 BHK ₹38L | 2 BHK ₹55L",
        "brochure": "docs/Marathe_Sapphire_brochure.pdf"
    },
    "Marathe Tower": {
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East",
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true",
        "price": "1 BHK ₹32L | 2 BHK ₹45L",
        "brochure": "docs/Marathe_Tower_brochure.pdf"
    },
    "Marathe Pride": {
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif",
        "price": "1 BHK ₹32L | 2 BHK ₹47L",
        "brochure": "docs/Marathe_Pride_brochure.pdf"
    },
    "Marathe Elenza": {
        "location": "Shahad (W)",
        "address": "Sales Office, Shahad West, Maharashtra",
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true",
        "price": "2 BHK ₹90L | 3 BHK ₹1.2Cr",
        "brochure": "docs/Marathe_Elenza_brochure.pdf"
    }
}

# ----------------- CSS Styling (premium) -----------------
st.markdown(
    """
    <style>
    :root { --gold: #FFD700; --muted: #bfbfbf; }
    body { background: #050505; color: #fff; }
    .hero { text-align:center; padding:24px; }
    .card { background: linear-gradient(145deg,#111,#0e0e0e); padding:18px; border-radius:14px; box-shadow:0 8px 30px rgba(255,215,0,0.06); margin-bottom:18px; }
    .project-img { border-radius:10px; box-shadow: 0 6px 25px rgba(0,0,0,0.6); width:100%; height:220px; object-fit:cover; }
    .cta { background: linear-gradient(90deg,var(--gold), #ffb700); color: #000; padding:10px 18px; border-radius:10px; font-weight:700; text-decoration:none;}
    .muted { color: #bfbfbf; font-size:13px; }
    .nav { display:flex; gap:18px; justify-content:center; align-items:center; margin-bottom:8px; }
    .footer { text-align:center; color:#9b9b9b; font-size:13px; padding:20px 0; }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Header / Navbar -----------------
logo_url = "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true"
st.markdown(f"""
<div class="hero">
  <img src="{logo_url}" width="160" style="border-radius:14px; box-shadow:0 10px 30px rgba(255,215,0,0.08);" />
  <h1 style="margin:6px 0; color:var(--gold)">Marathe Group</h1>
  <div class="muted">Luxury Living • Trusted Legacy</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='nav'><a href='#home' class='muted'>Home</a> | <a href='#projects' class='muted'>Projects</a> | <a href='#about' class='muted'>About</a> | <a href='#contact' class='muted'>Contact</a></div>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- Layout: main content + sidebar -----------------
sidebar_choice = st.sidebar.selectbox("Menu", ["Home", "Projects", "Customer Portal", "Admin Portal", "Contact"])

# ----------------- Home Page -----------------
if sidebar_choice == "Home":
    st.header("Welcome to Marathe Group")
    st.markdown("<p class='muted'>Premium residential & commercial developments across Mumbai's growing suburbs.</p>", unsafe_allow_html=True)
    # Show hero image (use Elenza image as hero)
    st.image(projects["Marathe Elenza"]["image"], use_column_width=True, caption="Marathe Elenza — Elegance redefined")
    st.markdown("---")
    st.subheader("Featured Projects")
    cols = st.columns(2)
    for i, (name, data) in enumerate(projects.items()):
        with cols[i % 2]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(data["image"], use_column_width=True, caption=name, output_format="auto")
            st.markdown(f"**{name}**  \n\n{data['location']}  \n\n**Price:** {data['price']}")
            # Brochure download (if exists in repo docs/)
            if os.path.exists(data["brochure"]):
                with open(data["brochure"], "rb") as f:
                    st.download_button(f"📄 Download Brochure — {name}", f, file_name=os.path.basename(data["brochure"]), key=f"bro_{name}")
            else:
                # placeholder link to repo path — users can add PDF later
                st.markdown(f"<a class='cta' href='{data['brochure']}' target='_blank'>📄 Download Brochure</a>", unsafe_allow_html=True)
            if st.button(f"💛 Book Site Visit — {name}", key=f"book_{name}"):
                st.session_state["preselect_project"] = name
                st.success(f"Go to Customer Portal → Register to book {name}")
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------- Projects page -----------------
elif sidebar_choice == "Projects":
    st.header("All Projects")
    for name, info in projects.items():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        cols = st.columns([1,2])
        with cols[0]:
            st.image(info["image"], use_column_width=True)
        with cols[1]:
            st.markdown(f"### <span style='color:var(--gold)'>{name}</span>", unsafe_allow_html=True)
            st.markdown(f"**Location:** {info['location']}")
            st.markdown(f"**Address:** {info['address']}")
            st.markdown(f"**Price:** {info['price']}")
            # Google maps link
            q = "+".join(info['address'].split())
            maps = f"https://www.google.com/maps/search/?api=1&query={q}"
            st.markdown(f"[🧭 View on Google Maps]({maps})")
            # Brochure
            if os.path.exists(info["brochure"]):
                with open(info["brochure"], "rb") as f:
                    st.download_button(f"📄 Download Brochure — {name}", f, file_name=os.path.basename(info["brochure"]), key=f"pb_{name}")
            else:
                st.markdown(f"<a class='cta' href='{info['brochure']}' target='_blank'>📄 Download Brochure</a>", unsafe_allow_html=True)
            if st.button(f"💛 Book Site Visit — {name}", key=f"pbk_{name}"):
                st.session_state["preselect_project"] = name
                st.success(f"Go to Customer Portal → Register to book {name}")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- Customer Portal -----------------
elif sidebar_choice == "Customer Portal":
    st.header("Customer Portal")
    df_customers = pd.read_excel(CUSTOMER_FILE)
    df_bookings = pd.read_excel(BOOKING_FILE)

    tabs = st.tabs(["Register", "Login", "Forgot Password", "My Documents"])

    # ----- Register -----
    with tabs[0]:
        st.subheader("Register (Customer)")
        r_name = st.text_input("Full Name", key="cust_reg_name")
        r_email = st.text_input("Email", key="cust_reg_email")
        r_pass = st.text_input("Set Password", type="password", key="cust_reg_pass")
        pre_proj = st.session_state.get("preselect_project", None)
        r_project = st.selectbox("Project to Book", list(projects.keys()), index=list(projects.keys()).index(pre_proj) if pre_proj in projects else 0, key="cust_reg_proj")
        if st.button("Send OTP", key="cust_send_otp"):
            if not (r_name and r_email and r_pass):
                st.error("Please fill Name, Email, Password.")
            else:
                if not can_send_otp(r_email):
                    st.error("OTP rate limit reached. Try after some time.")
                else:
                    otp = f"{random.randint(100000,999999)}"
                    ok = send_otp_email(r_email, otp, purpose="Customer Registration")
                    if ok:
                        store_otp(r_email, otp)
                        st.success("OTP sent to your email. Enter it below to verify.")
        r_otp = st.text_input("Enter OTP", key="cust_reg_otp")
        if st.button("Verify & Register", key="cust_verify"):
            ok, msg = verify_otp(r_email, r_otp)
            if ok:
                hashed = hash_password_bcrypt(r_pass)
                df_customers.loc[len(df_customers)] = [r_name, r_email, hashed, r_project, "Pending", datetime.datetime.now().isoformat()]
                df_customers.to_excel(CUSTOMER_FILE, index=False)
                st.success("Registration submitted. Admin will verify and approve your account.")
            else:
                st.error(msg)

    # ----- Login -----
    with tabs[1]:
        st.subheader("Customer Login")
        l_email = st.text_input("Email", key="cust_login_email")
        l_pass = st.text_input("Password", type="password", key="cust_login_pass")
        if st.button("Login", key="cust_login_btn"):
            df_customers = pd.read_excel(CUSTOMER_FILE)  # refresh
            row = df_customers[df_customers["Email"] == l_email]
            if row.empty:
                st.error("Email not registered.")
            else:
                if verify_password_bcrypt(l_pass, row.iloc[0]["PasswordHash"]):
                    if row.iloc[0]["Approved"] == "Yes":
                        st.success(f"Welcome {row.iloc[0]['Name']}!")
                        # show bookings & documents
                        my_docs = df_bookings[df_bookings["CustomerEmail"] == l_email]
                        st.subheader("My Bookings & Documents")
                        if my_docs.empty:
                            st.info("No documents uploaded yet by admin.")
                        else:
                            for idx, r in my_docs.iterrows():
                                st.markdown(f"**{r['Project']}** — {r['Status']} ({r['Date']})")
                                fp = r.get("FilePath")
                                if pd.notna(fp) and os.path.exists(str(fp)):
                                    with open(fp, "rb") as fh:
                                        st.download_button(f"Download {r['FileName']}", fh, file_name=r['FileName'], key=f"dl_{idx}")
                                else:
                                    st.markdown("_Document not available._")
                    else:
                        st.warning("Your registration is pending approval by the office.")
                else:
                    st.error("Incorrect password.")

    # ----- Forgot password -----
    with tabs[2]:
        st.subheader("Forgot Password")
        fp_email = st.text_input("Enter registered email", key="fp_email")
        if st.button("Send Reset OTP", key="fp_send"):
            df_customers = pd.read_excel(CUSTOMER_FILE)
            if df_customers[df_customers["Email"] == fp_email].empty:
                st.error("Email not registered.")
            else:
                if not can_send_otp(fp_email):
                    st.error("OTP rate limit reached.")
                else:
                    otp = f"{random.randint(100000,999999)}"
                    if send_otp_email(fp_email, otp, purpose="Password Reset"):
                        store_otp(fp_email, otp)
                        st.success("OTP sent. Enter OTP and new password below.")
        fp_otp = st.text_input("Enter OTP", key="fp_otp")
        fp_new = st.text_input("New Password", type="password", key="fp_new")
        if st.button("Verify & Reset", key="fp_reset"):
            ok, msg = verify_otp(fp_email, fp_otp)
            if ok:
                df_customers = pd.read_excel(CUSTOMER_FILE)
                df_customers.loc[df_customers["Email"] == fp_email, "PasswordHash"] = hash_password_bcrypt(fp_new)
                df_customers.to_excel(CUSTOMER_FILE, index=False)
                st.success("Password reset successful.")
            else:
                st.error(msg)

    # ----- My Documents quick access -----
    with tabs[3]:
        st.subheader("My Documents")
        m_email = st.text_input("Enter your approved email", key="md_email")
        if st.button("Show Documents", key="md_show"):
            df_customers = pd.read_excel(CUSTOMER_FILE)
            if df_customers[df_customers["Email"] == m_email].empty:
                st.error("Email not registered.")
            elif df_customers[df_customers["Email"] == m_email].iloc[0]["Approved"] != "Yes":
                st.warning("Your account is not approved yet.")
            else:
                df_bookings = pd.read_excel(BOOKING_FILE)
                docs = df_bookings[df_bookings["CustomerEmail"] == m_email]
                if docs.empty:
                    st.info("No documents uploaded yet.")
                else:
                    for idx, r in docs.iterrows():
                        st.markdown(f"**{r['Project']}** — {r['Status']} ({r['Date']})")
                        fp = r.get("FilePath")
                        if pd.notna(fp) and os.path.exists(str(fp)):
                            with open(str(fp), "rb") as fh:
                                st.download_button(f"Download {r['FileName']}", fh, file_name=r['FileName'], key=f"md_dl_{idx}")

# ----------------- Admin Portal -----------------
elif sidebar_choice == "Admin Portal":
    st.header("Admin Portal")
    df_admins = pd.read_excel(ADMIN_FILE)
    df_customers = pd.read_excel(CUSTOMER_FILE)
    df_bookings = pd.read_excel(BOOKING_FILE)

    tabs = st.tabs(["Register Admin", "Admin Login"])

    # Register admin
    with tabs[0]:
        st.subheader("Register Admin")
        a_name = st.text_input("Full Name", key="adm_reg_name")
        a_email = st.text_input("Official Email", key="adm_reg_email")
        a_pass = st.text_input("Set Password", type="password", key="adm_reg_pass")
        if st.button("Send OTP", key="adm_send"):
            if not (a_name and a_email and a_pass):
                st.error("Fill all fields.")
            else:
                if not can_send_otp(a_email):
                    st.error("OTP rate limit reached.")
                else:
                    otp = f"{random.randint(100000,999999)}"
                    if send_otp_email(a_email, otp, purpose="Admin Registration"):
                        store_otp(a_email, otp)
                        st.success("OTP sent.")
        adm_otp = st.text_input("Enter OTP", key="adm_otp")
        if st.button("Verify & Register Admin", key="adm_verify"):
            ok, msg = verify_otp(a_email, adm_otp)
            if ok:
                hashed = hash_password_bcrypt(a_pass)
                df_admins.loc[len(df_admins)] = [a_name, a_email, hashed, "Pending", datetime.datetime.now().isoformat()]
                df_admins.to_excel(ADMIN_FILE, index=False)
                st.success("Admin registration submitted — office will verify.")
            else:
                st.error(msg)

    # Admin login + dashboard
    with tabs[1]:
        st.subheader("Admin Login")
        login_email = st.text_input("Email", key="adm_login_email")
        login_pass = st.text_input("Password", type="password", key="adm_login_pass")
        if st.button("Login", key="adm_login_btn"):
            df_admins = pd.read_excel(ADMIN_FILE)
            row = df_admins[df_admins["Email"] == login_email]
            if row.empty:
                st.error("Admin not registered.")
            else:
                if verify_password_bcrypt(login_pass, row.iloc[0]["PasswordHash"]):
                    if row.iloc[0]["Approved"] != "Yes":
                        st.warning("Admin account pending approval by main office.")
                    else:
                        st.success(f"Welcome Admin {row.iloc[0]['Name']}")
                        # Admin controls
                        st.subheader("Pending Customer Approvals")
                        df_customers = pd.read_excel(CUSTOMER_FILE)
                        pending = df_customers[df_customers["Approved"] == "Pending"]
                        if pending.empty:
                            st.info("No pending customer registrations.")
                        else:
                            for idx, r in pending.iterrows():
                                st.markdown(f"- {r['Name']} • {r['Email']} • {r['Project']}")
                                if st.button(f"Approve {r['Email']}", key=f"approve_{idx}"):
                                    df_customers.loc[df_customers["Email"] == r['Email'], "Approved"] = "Yes"
                                    df_customers.to_excel(CUSTOMER_FILE, index=False)
                                    st.success(f"Approved {r['Email']}")

                        st.markdown("---")
                        st.subheader("Upload Documents for Customer")
                        approved = df_customers[df_customers["Approved"] == "Yes"]
                        if not approved.empty:
                            sel_email = st.selectbox("Select Customer Email", approved["Email"].tolist(), key="adm_sel_cust")
                            sel_proj = st.selectbox("Select Project", list(projects.keys()), key="adm_sel_proj")
                            upfile = st.file_uploader("Choose file (pdf/jpg/png)", type=["pdf","jpg","png"], key="adm_upload")
                            if upfile and st.button("Upload Document", key="adm_upload_btn"):
                                cust_dir = os.path.join(UPLOAD_DIR, sel_email.replace("@","_at_"))
                                os.makedirs(cust_dir, exist_ok=True)
                                save_path = os.path.join(cust_dir, upfile.name)
                                with open(save_path, "wb") as fh:
                                    fh.write(upfile.getbuffer())
                                # record
                                df_bookings.loc[len(df_bookings)] = [sel_email, sel_proj, datetime.datetime.now().strftime("%Y-%m-%d"), "Document Uploaded", upfile.name, save_path]
                                df_bookings.to_excel(BOOKING_FILE, index=False)
                                st.success("Document uploaded & linked to customer.")
                        else:
                            st.info("No approved customers yet.")

                        st.markdown("---")
                        st.subheader("All Bookings / Documents")
                        st.dataframe(pd.read_excel(BOOKING_FILE))
                else:
                    st.error("Incorrect password.")

# ----------------- Contact -----------------
elif sidebar_choice == "Contact":
    st.header("Contact Us")
    st.markdown(f"""
    📍 **Address:** {OFFICE_ADDRESS}  
    ⏰ **Working Hours:** 10:00 AM – 07:00 PM (Mon–Sun)  
    📞 **Phone:** +91 7045871101  
    💬 [WhatsApp Chat](https://wa.me/917045871101)  
    ✉️ **Email:** marathegroup1101@gmail.com
    """)
    st.markdown("<div class='footer'>© 2025 Marathe Group — Designed by Ritika Rawat</div>", unsafe_allow_html=True)
