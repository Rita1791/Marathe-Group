import streamlit as st
import pandas as pd
import datetime
import os
import bcrypt
import random
import smtplib
from email.message import EmailMessage

# ---------------- CONFIGURATION ----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

# ---------------- CONSTANTS ----------------
EMAIL_USER = st.secrets.get("EMAIL_USER", "marathegroup1101@gmail.com")
EMAIL_PASS = st.secrets.get("EMAIL_PASS", "")
OFFICE_ADDRESS = "Swami Vivekanand Chowk, Titwala (E), Maharashtra"

# Data files
ADMIN_FILE = "admins.xlsx"
CUSTOMER_FILE = "customers.xlsx"
BOOKING_FILE = "bookings.xlsx"
os.makedirs("uploads", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# Initialize Excel files
for file, cols in [
    (ADMIN_FILE, ["Name", "Email", "PasswordHash", "Approved", "CreatedAt"]),
    (CUSTOMER_FILE, ["Name", "Email", "PasswordHash", "Project", "Approved", "CreatedAt"]),
    (BOOKING_FILE, ["CustomerEmail", "Project", "Date", "Status", "FileName", "FilePath"]),
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_excel(file, index=False)

# ---------------- EMAIL (OTP) ----------------
def send_otp_email(recipient: str, otp: str, purpose: str = "Verification"):
    LOGO_URL = "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true"
    msg = EmailMessage()
    msg["Subject"] = f"Marathe Group — {purpose} OTP"
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    html = f"""
    <html>
      <body style="font-family:Arial,Helvetica,sans-serif;background:#f7f7f7;">
        <table align="center" width="600" style="margin:30px auto;background:#fff;border-radius:10px;">
          <tr style="background:#111;">
            <td style="padding:15px;text-align:center;">
              <img src="{LOGO_URL}" width="160"><br>
              <h2 style="color:#FFD700;margin:10px 0 0 0;">Marathe Group</h2>
            </td>
          </tr>
          <tr>
            <td style="padding:25px;">
              <h3>Your {purpose} OTP</h3>
              <p>Use the code below to continue. It expires in <b>5 minutes</b>.</p>
              <div style="font-size:30px;letter-spacing:5px;font-weight:bold;background:#fafafa;padding:15px;text-align:center;border-radius:8px;">
                {otp}
              </div>
              <p style="color:#777;margin-top:20px;">If you did not request this, ignore this email.</p>
              <hr>
              <small>Marathe Group • {OFFICE_ADDRESS}</small>
            </td>
          </tr>
        </table>
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
        st.error(f"Error sending OTP: {e}")
        return False

# ---------------- PASSWORD SECURITY ----------------
def hash_pw(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_pw(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------- PROJECT DATA ----------------
projects = {
    "Marathe Sapphire": {
        "location": "Titwala (E)",
        "address": "Swami Vivekanand Chowk Road, Titwala East",
        "price": "1 BHK ₹38L (Incl. Taxes) | 2 BHK ₹55L (Incl. Taxes)",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif",
    },
    "Marathe Tower": {
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East",
        "price": "1 BHK ₹32L + Taxes | 2 BHK ₹45L + Taxes",
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true",
    },
    "Marathe Pride": {
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East",
        "price": "1 BHK ₹32L + Taxes | 2 BHK ₹47L + Taxes",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif",
    },
    "Marathe Elenza": {
        "location": "Shahad (W)",
        "address": "Sales Office, Shahad West",
        "price": "2 BHK ₹90L | 3 BHK ₹1.2Cr",
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true",
    }
}

# ---------------- STYLING ----------------
st.markdown("""
<style>
:root { --gold: #FFD700; }
body { background-color: #0e0e0e; color: white; }
.card { background: linear-gradient(145deg,#111,#0a0a0a); border-radius:15px; padding:18px; margin:12px 0; box-shadow:0 0 20px rgba(255,215,0,0.1);}
h1,h2,h3 { color: var(--gold); }
button, .stDownloadButton>button { background: linear-gradient(90deg,#FFD700,#ffb700); color:#111; font-weight:600; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="text-align:center;">
    <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true" width="180">
    <h1>Marathe Group</h1>
    <h4 style="color:gray;">Luxury Living • Trusted Legacy</h4>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ---------------- MENU ----------------
menu = st.sidebar.selectbox("Navigation", ["Home", "Projects", "Customer Portal", "Admin Portal", "Contact"])

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("Welcome to Marathe Group")
    st.image(projects["Marathe Elenza"]["image"], caption="Marathe Elenza — Elegance Redefined", use_column_width=True)
    for name, data in projects.items():
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <h3>{name}</h3>
                <p><b>📍 Location:</b> {data['location']}</p>
                <p><b>🏠 Address:</b> {data['address']}</p>
                <p><b>💰 Price:</b> {data['price']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------- PROJECTS ----------------
elif menu == "Projects":
    st.header("Our Projects")
    for name, data in projects.items():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.image(data["image"], caption=name, use_column_width=True)
        st.markdown(f"""
        **Location:** {data['location']}  
        **Address:** {data['address']}  
        **Price:** {data['price']}  
        """)
        st.markdown(f"[View on Google Maps](https://www.google.com/maps/search/{data['address'].replace(' ','+')})")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CUSTOMER PORTAL ----------------
elif menu == "Customer Portal":
    tab1, tab2 = st.tabs(["Register", "Login"])

    # Register
    with tab1:
        name = st.text_input("Full Name", key="r_name")
        email = st.text_input("Email", key="r_email")
        password = st.text_input("Set Password", type="password", key="r_pass")
        project = st.selectbox("Select Project", list(projects.keys()), key="r_proj")
        if st.button("Send OTP"):
            otp = str(random.randint(100000, 999999))
            send_otp_email(email, otp, "Registration")
            st.session_state.otp = otp
            st.session_state.email = email
        otp_in = st.text_input("Enter OTP", key="r_otp")
        if st.button("Register"):
            if otp_in == st.session_state.get("otp") and email == st.session_state.get("email"):
                df = pd.read_excel(CUSTOMER_FILE)
                hashed = hash_pw(password)
                df.loc[len(df)] = [name, email, hashed, project, "Pending", datetime.datetime.now()]
                df.to_excel(CUSTOMER_FILE, index=False)
                st.success("Registered successfully! Await admin approval.")
            else:
                st.error("Invalid OTP.")

    # Login
    with tab2:
        email = st.text_input("Email", key="l_email")
        password = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            df = pd.read_excel(CUSTOMER_FILE)
            user = df[df["Email"] == email]
            if user.empty:
                st.error("No user found.")
            elif not check_pw(password, user.iloc[0]["PasswordHash"]):
                st.error("Incorrect password.")
            elif user.iloc[0]["Approved"] != "Yes":
                st.warning("Approval pending.")
            else:
                st.success(f"Welcome {user.iloc[0]['Name']}!")
                dfb = pd.read_excel(BOOKING_FILE)
                mydocs = dfb[dfb["CustomerEmail"] == email]
                for _, r in mydocs.iterrows():
                    if os.path.exists(r["FilePath"]):
                        with open(r["FilePath"], "rb") as f:
                            st.download_button(r["FileName"], f, file_name=r["FileName"])

# ---------------- ADMIN PORTAL ----------------
elif menu == "Admin Portal":
    tab1, tab2 = st.tabs(["Register Admin", "Login"])

    # Register admin
    with tab1:
        name = st.text_input("Full Name", key="a_name")
        email = st.text_input("Email", key="a_email")
        password = st.text_input("Set Password", type="password", key="a_pass")
        if st.button("Register Admin"):
            df = pd.read_excel(ADMIN_FILE)
            hashed = hash_pw(password)
            df.loc[len(df)] = [name, email, hashed, "Pending", datetime.datetime.now()]
            df.to_excel(ADMIN_FILE, index=False)
            st.success("Admin registration sent for approval.")

    # Admin login
    with tab2:
        email = st.text_input("Admin Email", key="al_email")
        password = st.text_input("Password", type="password", key="al_pass")
        if st.button("Login"):
            df = pd.read_excel(ADMIN_FILE)
            admin = df[df["Email"] == email]
            if admin.empty:
                st.error("No admin found.")
            elif not check_pw(password, admin.iloc[0]["PasswordHash"]):
                st.error("Incorrect password.")
            elif admin.iloc[0]["Approved"] != "Yes":
                st.warning("Approval pending.")
            else:
                st.success(f"Welcome Admin {admin.iloc[0]['Name']}")
                st.subheader("Pending Customer Approvals")
                dfc = pd.read_excel(CUSTOMER_FILE)
                pending = dfc[dfc["Approved"] == "Pending"]
                for _, r in pending.iterrows():
                    st.write(f"{r['Name']} — {r['Email']} ({r['Project']})")
                    if st.button(f"Approve {r['Email']}", key=r['Email']):
                        dfc.loc[dfc["Email"] == r["Email"], "Approved"] = "Yes"
                        dfc.to_excel(CUSTOMER_FILE, index=False)
                        st.success(f"{r['Email']} approved.")

                st.subheader("Upload Customer Documents")
                cust_email = st.selectbox("Select Customer", dfc["Email"].tolist(), key="u_email")
                proj = st.selectbox("Project", list(projects.keys()), key="u_proj")
                file = st.file_uploader("Upload File", type=["pdf", "jpg", "png"], key="u_file")
                if file and st.button("Upload Document"):
                    save_path = os.path.join("uploads", file.name)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                    dfb = pd.read_excel(BOOKING_FILE)
                    dfb.loc[len(dfb)] = [cust_email, proj, datetime.datetime.now(), "Uploaded", file.name, save_path]
                    dfb.to_excel(BOOKING_FILE, index=False)
                    st.success("Uploaded successfully.")

# ---------------- CONTACT ----------------
else:
    st.header("Contact Us")
    st.markdown(f"""
    📍 **Address:** {OFFICE_ADDRESS}  
    ⏰ **Working Hours:** 10:00 AM – 07:00 PM  
    📞 **Phone:** +91 7045871101  
    ✉️ **Email:** marathegroup1101@gmail.com  
    💬 [WhatsApp](https://wa.me/917045871101)
    """)
    st.caption("© 2025 Marathe Group | Designed by Ritika Rawat 💻")
