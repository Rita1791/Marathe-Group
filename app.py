import streamlit as st
import pandas as pd
import datetime
import os

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

# ----------------- HEADER -----------------
st.markdown("<h1 style='text-align:center;'>🏢 Marathe Group</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:gray;'>Luxury Living • Trusted Legacy</h4>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80",
         use_column_width=True, caption="Building Dreams Since 1995")
st.markdown("---")

# ----------------- MISSION & VISION -----------------
st.markdown("## 🌟 Our Mission & Vision")
st.markdown("""
### 🏗️ **Mission**
To build homes that redefine comfort and deliver unmatched value through trust, transparency, and excellence in every detail.  

### 🌍 **Vision**
To emerge as a leading name in India’s real estate sector by crafting iconic developments that inspire confidence and elevate modern living experiences.
""")
st.markdown("---")

# ----------------- PROJECT DATA -----------------
ongoing_projects = [
    {
        "name": "Marathe Sapphire",
        "location": "Titwala (E)",
        "address": "1st Floor Sales Office, Marathe Sapphire, Swami Vivekanand Chowk Road, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_sapphire.jpg"
    },
    {
        "name": "Marathe Tower",
        "location": "Titwala (E)",
        "address": "Ground Floor Sales Office, Marathe Tower, Digi1 Road, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_tower.jpg"
    },
    {
        "name": "Marathe Pride",
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Marathe Pride, Ambernath East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_pride.jpg"
    }
]

completed_projects = [
    {
        "name": "Marathe Empress",
        "location": "Titwala (E)",
        "address": "Marathe Empress, Jagat Naka, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_empress.jpg"
    },
    {
        "name": "Marathe Height",
        "location": "Titwala (E)",
        "address": "Marathe Height, Near Ghar Aangan, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_height.jpg"
    },
    {
        "name": "Marathe Fortune",
        "location": "Titwala (E)",
        "address": "Marathe Fortune, Ganesh Mandir Road, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_fortune.jpg"
    },
    {
        "name": "Marathe Empire",
        "location": "Titwala (E)",
        "address": "Marathe Empire, Near Mahaganpati Hospital, Titwala East, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_empire.jpg"
    },
    {
        "name": "Marathe Elenza",
        "location": "Shahad (W)",
        "address": "Ground Floor Sales Office, Marathe Elenza, Shahad West, Maharashtra",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe_elenza.jpg"
    }
]

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Ongoing Projects", "🏠 Completed Projects", "📝 Enquiry Form", "📞 Contact Info"])

# ----------------- ONGOING PROJECTS -----------------
with tab1:
    st.subheader("Ongoing Projects")
    for p in ongoing_projects:
        st.image(p["image"], caption=p["name"], use_column_width=True)
        st.markdown(f"🏗️ **Project:** {p['name']}  \n📍 **Location:** {p['location']}  \n🏠 **Address:** {p['address']}")
        st.markdown("---")

# ----------------- COMPLETED PROJECTS -----------------
with tab2:
    st.subheader("Completed Projects")
    for p in completed_projects:
        st.image(p["image"], caption=p["name"], use_column_width=True)
        st.markdown(f"🏢 **Project:** {p['name']}  \n📍 **Location:** {p['location']}  \n🏠 **Address:** {p['address']}")
        st.markdown("---")

# ----------------- ENQUIRY FORM -----------------
with tab3:
    st.subheader("Flat Enquiry Form 🏡")
    st.write("Please fill the form below and our team will contact you soon:")

    excel_path = "enquiries.xlsx"
    if not os.path.exists(excel_path):
        df = pd.DataFrame(columns=["Name", "Phone", "Project", "Message", "Timestamp"])
        df.to_excel(excel_path, index=False)

    with st.form("enquiry_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        project = st.selectbox("Select Project", [p["name"] for p in ongoing_projects + completed_projects])
        message = st.text_area("Additional Message (optional)")
        submit = st.form_submit_button("Submit")

        if submit:
            if name and phone:
                new_entry = pd.DataFrame({
                    "Name": [name],
                    "Phone": [phone],
                    "Project": [project],
                    "Message": [message],
                    "Timestamp": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })
                df = pd.read_excel(excel_path)
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_excel(excel_path, index=False)
                st.success(f"✅ Thank you {name}! Your enquiry for **{project}** has been recorded.")
            else:
                st.error("Please enter both Name and Phone Number.")

    if os.path.exists(excel_path):
        with open(excel_path, "rb") as f:
            st.download_button("📥 Download Enquiries Excel File", f, file_name="enquiries.xlsx")

# ----------------- CONTACT INFO -----------------
with tab4:
    st.subheader("Contact Information")
    st.markdown("""  
    ⏰ **Working Hours:** 10:00 AM – 07:00 PM (Mon – Sun)  
    📞 **Contact Number:** +91 7045871101  
    💬 **WhatsApp:** [Chat Now](https://wa.me/917045871101)  
    ✉️ **Email:** marathegroup1101@gmail.com  
    👤 **Owner:**  Parasana Marathe   
    👥 **Manager:**  Padma Rawat  
    """)
    st.caption("© 2025 Marathe Group | Designed and Developed by Ritika Rawat 💻")
