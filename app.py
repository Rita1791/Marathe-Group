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

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Ongoing Projects", "🏠 Completed Projects", "📝 Enquiry Form", "📞 Contact Info"])

# ----------------- ONGOING PROJECTS -----------------
with tab1:
    st.subheader("Ongoing Projects")
    for name, data in projects.items():
        st.image(data["image"], caption=name, use_column_width=True)
        st.markdown(f"🏢 **Project:** {name}  \n📍 **Location:** {data['location']}  \n🏠 **Address:** {data['address']}")
        st.markdown("### 🏡 Available Flats:")
        for flat in data["flats"]:
            with st.container():
                st.image(flat["image"], caption=f"{flat['type']} - {flat['area']} - {flat['price']} ({flat['status']})",
                         use_column_width=True)
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
        project = st.selectbox("Select Project", list(projects.keys()) + [p["name"] for p in completed_projects])
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
    👤 **Owner:** Parasana Marathe  
    👥 **Manager:**  Padma Rawat
    """)
    st.caption("© 2025 Marathe Group | Designed and Developed by Ritika Rawat 💻")
