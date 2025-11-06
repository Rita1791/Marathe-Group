import streamlit as st
import pandas as pd
import datetime
import os

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

# ----------------- HEADER -----------------
st.markdown("""
    <div style="text-align:center;">
        <h1>🏢 Marathe Group</h1>
        <h4 style="color:gray;">Luxury Living • Trusted Legacy</h4>
    </div>
""", unsafe_allow_html=True)
st.image(
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80",
    use_column_width=True,
    caption="Building Dreams Since 1995"
)
st.markdown("---")

# ----------------- MISSION & VISION -----------------
st.markdown("""
<style>
.mission-vision-box {
    background: linear-gradient(135deg, #1f1f1f, #2a2a2a);
    padding: 40px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.3);
    border: 1px solid rgba(255, 215, 0, 0.4);
    transition: all 0.3s ease-in-out;
}
.mission-vision-box:hover {
    transform: scale(1.01);
    box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.5);
}
.mission-title {
    color: #FFD700;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}
.mission-text {
    font-size: 18px;
    color: #f0f0f0;
    text-align: justify;
    line-height: 1.6;
}
.icon {
    font-size: 35px;
    text-align: center;
    display: block;
    margin-bottom: 10px;
}
</style>

<h2 style="text-align:center; color:#FFD700;">🌟 Our Mission & Vision</h2>

<div class="mission-vision-box">
    <div class="icon">🏗️</div>
    <div class="mission-title">Our Mission</div>
    <div class="mission-text">
        To build homes that redefine comfort, quality, and elegance — delivering unmatched value through trust, innovation, and transparency. 
        Every project we create blends design excellence with long-lasting craftsmanship for families to cherish for generations.
    </div>
    <br>
    <div class="icon">🌍</div>
    <div class="mission-title">Our Vision</div>
    <div class="mission-text">
        To become a name synonymous with trust and excellence in India’s real estate sector by crafting landmark spaces that enrich lives, 
        inspire communities, and reflect modern living with a timeless essence.
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ----------------- PROJECT DATA -----------------
projects = {
    "Marathe Sapphire": {
        "location": "Titwala (E)",
        "address": "Swami Vivekanand Chowk Road, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif",
        "flats": [
            {"type": "1 BHK", "area": "650 sq.ft", "price": "₹35 Lakh", "status": "Available",
             "image": "https://images.unsplash.com/photo-1600566753190-17f2ba1b3b69?auto=format&fit=crop&w=1000&q=80"},
            {"type": "2 BHK", "area": "950 sq.ft", "price": "₹52 Lakh", "status": "Available",
             "image": "https://images.unsplash.com/photo-1598300056391-8eb1d63d5d92?auto=format&fit=crop&w=1000&q=80"},
        ]
    },
    "Marathe Tower": {
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East, Maharashtra",
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true",
        "flats": [
            {"type": "1 BHK", "area": "620 sq.ft", "price": "₹33 Lakh", "status": "Sold",
             "image": "https://images.unsplash.com/photo-1598300042247-c95c6d3e0f9d?auto=format&fit=crop&w=1000&q=80"},
            {"type": "2 BHK", "area": "910 sq.ft", "price": "₹50 Lakh", "status": "Available",
             "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80"},
        ]
    },
    "Marathe Pride": {
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif",
        "flats": [
            {"type": "1 BHK", "area": "640 sq.ft", "price": "₹34 Lakh", "status": "Available",
             "image": "https://images.unsplash.com/photo-1600607687920-4e24d07d1c07?auto=format&fit=crop&w=1000&q=80"},
        ]
    }
}

completed_projects = [
    {"name": "Marathe Empress", "location": "Titwala (E)", "address": "Jagat Naka, Titwala East, Maharashtra",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Empress.webp?raw=true"},
    {"name": "Marathe Height", "location": "Titwala (E)", "address": "Near Ghar Aangan, Titwala East, Maharashtra",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/marathe%20Height.png?raw=true"},
    {"name": "Marathe Fortune", "location": "Titwala (E)", "address": "Ganesh Mandir Road, Titwala East, Maharashtra",
     "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Fortune.avif"},
    {"name": "Marathe Empire", "location": "Titwala (E)", "address": "Near Mahaganpati Hospital, Titwala East, Maharashtra",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Empire.jpg?raw=true"},
    {"name": "Marathe Elenza", "location": "Shahad (W)", "address": "Sales Office, Shahad West, Maharashtra",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true"},
]

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏗️ Ongoing Projects", 
    "🏠 Completed Projects", 
    "📝 Enquiry Form", 
    "📞 Contact Info", 
    "🧑‍💼 Admin Portal", 
    "👤 Customer Portal"
])

# ----------------- ONGOING PROJECTS -----------------
with tab1:
    st.subheader("🏗️ Ongoing Projects")
    for name, data in projects.items():
        st.image(data["image"], caption=name, use_column_width=True)
        st.markdown(f"🏢 **Project:** {name}  \n📍 **Location:** {data['location']}  \n🏠 **Address:** {data['address']}")
        st.markdown("### 🏡 Available Flats:")
        for flat in data["flats"]:
            st.image(flat["image"], caption=f"{flat['type']} - {flat['area']} - {flat['price']} ({flat['status']})",
                     use_column_width=True)
        st.markdown("---")

# ----------------- COMPLETED PROJECTS -----------------
with tab2:
    st.subheader("🏠 Completed Projects")
    for p in completed_projects:
        st.image(p["image"], caption=p["name"], use_column_width=True)
        st.markdown(f"🏢 **Project:** {p['name']}  \n📍 **Location:** {p['location']}  \n🏠 **Address:** {p['address']}")
        st.markdown("---")

# ----------------- ENQUIRY FORM -----------------
with tab3:
    st.subheader("📝 Flat Enquiry Form")
    st.write("Please fill the form below and our team will contact you soon:")

    excel_path = "enquiries.xlsx"
    if not os.path.exists(excel_path):
        pd.DataFrame(columns=["Name", "Phone", "Project", "Message", "Timestamp"]).to_excel(excel_path, index=False)

    with st.form("enquiry_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        project = st.selectbox("Select Project", list(projects.keys()) + [p["name"] for p in completed_projects])
        message = st.text_area("Additional Message (optional)")
        submit = st.form_submit_button("Submit Enquiry")

        if submit:
            if name and phone:
                df = pd.read_excel(excel_path)
                new_entry = pd.DataFrame([[name, phone, project, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                                         columns=df.columns)
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_excel(excel_path, index=False)
                st.success(f"✅ Thank you {name}! Your enquiry for **{project}** has been recorded.")
            else:
                st.error("⚠️ Please enter both Name and Phone Number.")

    # Secure download section for admin
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>🔐 Admin Access - Enquiry Records</h3>", unsafe_allow_html=True)
    admin_pass = st.text_input("Enter Admin Password:", type="password")
    if admin_pass == "Marathe@Admin2025":
        with open(excel_path, "rb") as f:
            st.download_button("📥 Download Enquiries Excel File", f, file_name="enquiries.xlsx")
    elif admin_pass != "":
        st.error("❌ Incorrect password.")

# ----------------- CONTACT INFO -----------------
with tab4:
    st.subheader("📞 Contact Information")
    st.markdown("""  
    ⏰ **Working Hours:** 10:00 AM – 07:00 PM (Mon – Sun)  
    📞 **Contact Number:** +91 7045871101  
    💬 **WhatsApp:** [Chat Now](https://wa.me/917045871101)  
    ✉️ **Email:** marathegroup1101@gmail.com  
    👤 **Owner:** Parasana Ramesh Marathe  
    👥 **Manager:**  Padma Rajendra Rawat  
    """)
    st.caption("© 2025 Marathe Group | Designed and Developed by Ritika Rawat 💻")

# ----------------- ADMIN PORTAL -----------------
with tab5:
    st.subheader("🧑‍💼 Admin Portal")
    admin_data_path = "admin_users.xlsx"
    if not os.path.exists(admin_data_path):
        pd.DataFrame(columns=["Name", "Email", "Password", "Approved"]).to_excel(admin_data_path, index=False)

    action = st.radio("Choose Action", ["Login", "Register"], key="admin_action")
    if action == "Register":
        name = st.text_input("Full Name", key="admin_name")
        email = st.text_input("Official Email", key="admin_email")
        password = st.text_input("Set Password", type="password", key="admin_password")
        if st.button("Register Admin", key="admin_register"):
            df = pd.read_excel(admin_data_path)
            df.loc[len(df)] = [name, email, password, "Pending"]
            df.to_excel(admin_data_path, index=False)
            st.success("✅ Registration submitted for verification.")
    else:
        email = st.text_input("Email ID", key="admin_login_email")
        password = st.text_input("Password", type="password", key="admin_login_password")
        if st.button("Login", key="admin_login_btn"):
            df = pd.read_excel(admin_data_path)
            user = df[(df["Email"] == email) & (df["Password"] == password)]
            if not user.empty:
                if user["Approved"].iloc[0] == "Yes":
                    st.success(f"Welcome {user['Name'].iloc[0]}!")
                    if os.path.exists("enquiries.xlsx"):
                        with open("enquiries.xlsx", "rb") as f:
                            st.download_button("📥 Download Enquiries Excel", f, file_name="enquiries.xlsx", key="admin_download")
                else:
                    st.warning("⏳ Verification pending from office.")
            else:
                st.error("❌ Invalid credentials.")


# ----------------- CUSTOMER PORTAL -----------------
with tab6:
    st.subheader("👤 Customer Portal")
    cust_data_path = "customer_users.xlsx"
    if not os.path.exists(cust_data_path):
        pd.DataFrame(columns=["Name", "Email", "Password", "Project", "Approved"]).to_excel(cust_data_path, index=False)

    action2 = st.radio("Choose Action", ["Login", "Register"], key="cust_action")
    if action2 == "Register":
        name = st.text_input("Full Name", key="cust_name")
        email = st.text_input("Email ID", key="cust_email")
        password = st.text_input("Set Password", type="password", key="cust_password")
        project = st.selectbox("Your Project", list(projects.keys()) + [p["name"] for p in completed_projects], key="cust_project")
        if st.button("Register Customer", key="cust_register_btn"):
            df = pd.read_excel(cust_data_path)
            df.loc[len(df)] = [name, email, password, project, "Pending"]
            df.to_excel(cust_data_path, index=False)
            st.success("✅ Registration submitted! Office will verify soon.")
    else:
        email = st.text_input("Email", key="cust_login_email")
        password = st.text_input("Password", type="password", key="cust_login_password")
        if st.button("Login", key="cust_login_btn"):
            df = pd.read_excel(cust_data_path)
            user = df[(df["Email"] == email) & (df["Password"] == password)]
            if not user.empty:
                if user["Approved"].iloc[0] == "Yes":
                    st.success(f"Welcome {user['Name'].iloc[0]}! 👋")
                    st.write(f"🏢 Project: {user['Project'].iloc[0]}")
                    st.markdown("📄 [View Sample Payment Receipt](https://example.com/payment-receipt.pdf)")
                    st.markdown("📄 [View Sample Registration Document](https://example.com/registration.pdf)")
                else:
                    st.warning("⏳ Your registration is pending approval.")
            else:
                st.error("❌ Invalid login credentials.")
