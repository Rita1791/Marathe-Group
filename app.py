import streamlit as st
import pandas as pd
import datetime
import os

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Marathe Group | Luxury Living", page_icon="🏢", layout="wide")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
body {
    background-color: #0d0d0d;
    color: white;
    font-family: 'Poppins', sans-serif;
}
h1, h2, h3 {
    color: #FFD700;
}
hr {
    border: 1px solid rgba(255,215,0,0.3);
}
button {
    border-radius: 10px;
}
.project-card {
    background: linear-gradient(145deg, #1a1a1a, #141414);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 0px 25px rgba(255, 215, 0, 0.2);
    transition: 0.3s ease-in-out;
    margin-bottom: 30px;
}
.project-card:hover {
    transform: scale(1.02);
    box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.4);
}
.book-btn {
    background: linear-gradient(90deg, #FFD700, #ffb700);
    color: black;
    font-weight: bold;
    padding: 10px 25px;
    border-radius: 12px;
    text-align: center;
    transition: all 0.3s ease;
}
.book-btn:hover {
    background: linear-gradient(90deg, #ffcc00, #ffe680);
    box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.6);
    transform: scale(1.05);
}
.footer {
    text-align: center;
    font-size: 13px;
    color: #999;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------------- HEADER SECTION -----------------
st.markdown("""
    <div style="text-align:center;">
        <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true"
             width="200" style="border-radius:20px; margin-bottom:15px;">
        <h1 style="font-family:'Trebuchet MS';">🏢 Marathe Group</h1>
        <h4 style="color:#ccc;">Luxury Living • Trusted Legacy</h4>
    </div>
""", unsafe_allow_html=True)

st.video("https://github.com/Rita1791/Marathe-Group/raw/refs/heads/main/images/MG%20Video.mp4")

st.markdown("""
<p style="text-align:center; font-style:italic; color:gray;">
Marathe Elenza — Where Luxury Meets Lifestyle ✨
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------- MISSION & VISION -----------------
st.markdown("""
<div style='background: linear-gradient(135deg, #1c1c1c, #111); padding: 40px; border-radius: 15px;'>
<h2 style='text-align:center; color:#FFD700;'>🌟 Our Mission & Vision</h2>
<p style='font-size:18px; text-align:center; color:#f0f0f0;'>
To build homes that redefine comfort, design excellence, and trust.  
Marathe Group is committed to creating living spaces that blend innovation with tradition —  
bringing families closer to their dream lifestyle.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------- PROJECT DETAILS -----------------
projects = {
    "Marathe Sapphire": {
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif",
        "location": "Titwala (E)",
        "address": "Swami Vivekanand Chowk Road, Titwala East",
        "map": "https://www.google.com/maps?q=Marathe+Sapphire+Titwala",
        "flats": [("1 BHK", "₹38 Lakh (Incl. Taxes)"), ("2 BHK", "₹55 Lakh (Incl. Taxes)")]
    },
    "Marathe Tower": {
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true",
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East",
        "map": "https://www.google.com/maps?q=Marathe+Tower+Titwala",
        "flats": [("1 BHK", "₹32 Lakh + Taxes"), ("2 BHK", "₹45 Lakh + Taxes")]
    },
    "Marathe Pride": {
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif",
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East",
        "map": "https://www.google.com/maps?q=Marathe+Pride+Ambernath",
        "flats": [("1 BHK", "₹32 Lakh + Taxes"), ("2 BHK", "₹47 Lakh + Taxes")]
    },
}

st.header("🏗️ Ongoing Projects")

cols = st.columns(3)
for i, (name, data) in enumerate(projects.items()):
    with cols[i % 3]:
        st.markdown(f"""
        <div class='project-card'>
            <img src='{data["image"]}' style='width:100%; border-radius:10px; margin-bottom:10px;'>
            <h3 style='color:#FFD700; text-align:center;'>{name}</h3>
            <p style='text-align:center; color:#bbb;'>📍 {data["location"]}<br>🏠 {data["address"]}</p>
            <p><b>Flat Options:</b></p>
            """, unsafe_allow_html=True)
        for flat, price in data["flats"]:
            st.markdown(f"<p>• {flat} — <b>{price}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<a href='{data['map']}' target='_blank' style='color:#FFD700;'>🧭 View on Google Maps</a>", unsafe_allow_html=True)
        if st.button(f"💛 Book Now", key=f"book_{name}"):
            st.session_state["selected_project"] = name
            st.success(f"Scroll down to the enquiry form for {name}!")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------- ENQUIRY FORM -----------------
st.header("📝 Enquiry Form")

excel_path = "enquiries.xlsx"
if not os.path.exists(excel_path):
    pd.DataFrame(columns=["Name","Phone","Project","Message","Timestamp"]).to_excel(excel_path, index=False)

selected = st.session_state.get("selected_project", list(projects.keys())[0])

with st.form("enquiry_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    project = st.selectbox("Select Project", list(projects.keys()), index=list(projects.keys()).index(selected))
    message = st.text_area("Message / Query")
    submit = st.form_submit_button("Submit")

    if submit:
        if name and phone:
            df = pd.read_excel(excel_path)
            new_entry = pd.DataFrame([[name, phone, project, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], columns=df.columns)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_excel(excel_path, index=False)
            st.success(f"✅ Thank you {name}! Your enquiry for {project} has been recorded.")
        else:
            st.error("⚠️ Please fill in all required fields.")

# ----------------- ADMIN DOWNLOAD -----------------
st.markdown("---")
st.markdown("<h3 style='text-align:center;'>🔐 Admin Access – Download Enquiries</h3>", unsafe_allow_html=True)
admin_pass = st.text_input("Enter Admin Password:", type="password")
if admin_pass == "Marathe@Admin2025":
    with open(excel_path, "rb") as f:
        st.download_button("📥 Download Enquiries Excel File", f, file_name="enquiries.xlsx")
elif admin_pass != "":
    st.error("❌ Incorrect password.")

# ----------------- CONTACT SECTION -----------------
st.markdown("---")
st.header("📞 Contact Us")
st.markdown("""
📍 **Address:** Marathe Group Office, Titwala (E), Maharashtra  
📞 **Phone:** +91 7045871101  
💬 [Chat on WhatsApp](https://wa.me/917045871101)  
✉️ **Email:** marathegroup1101@gmail.com  
👤 **Owner:** Parasana Ramesh Marathe  
""")
st.markdown("<div class='footer'>© 2025 Marathe Group | Designed & Developed by Ritika Rawat 💻</div>", unsafe_allow_html=True)
