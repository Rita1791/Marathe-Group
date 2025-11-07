import streamlit as st
import pandas as pd
import datetime
import os

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

# ----------------- HEADER -----------------
st.markdown("""
    <div style="text-align:center;">
        <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true" width="220">
        <h1>🏢 Marathe Group</h1>
        <h4 style="color:gray;">Luxury Living • Trusted Legacy</h4>
    </div>
""", unsafe_allow_html=True)
st.image(
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80",
    use_column_width=True,
    caption="Building Dreams Since 1985"
)
st.markdown("---")

# ----------------- MARATHE ELENZA PROMO SECTION -----------------
st.markdown("""
<style>
.home-section {
    text-align: center;
    padding: 30px 0;
}
.video-box {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0px 4px 25px rgba(255, 215, 0, 0.4);
    margin-top: 15px;
}
.audio-player {
    display: none;
}
.fadeIn {
    animation: fadeIn 2s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="home-section fadeIn">
    <h2 style="color:#FFD700;">✨ Marathe Elenza — Elevating Luxury Living ✨</h2>
    <div class="video-box">
        <video width="100%" height="auto" autoplay loop muted playsinline>
            <source src="https://github.com/Rita1791/Marathe-Group/raw/refs/heads/main/images/MG%20Video.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <audio autoplay loop class="audio-player">
        <source src="https://cdn.pixabay.com/audio/2022/02/15/audio_28a23d0e8b.mp3" type="audio/mpeg">
    </audio>
</div>
""", unsafe_allow_html=True)

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
        "map_link": "https://www.google.com/maps?q=Marathe+Sapphire+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Sapphire.avif",
        "flats": [
            {"type": "1 BHK", "area": "650 sq.ft", "price": "₹38 Lakh (Incl. Taxes)", "status": "Available"},
            {"type": "2 BHK", "area": "950 sq.ft", "price": "₹55 Lakh (Incl. Taxes)", "status": "Available"},
        ]
    },
    "Marathe Tower": {
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East, Maharashtra",
        "map_link": "https://www.google.com/maps?q=Marathe+Tower+Titwala",
        "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Tower.jpg?raw=true",
        "flats": [
            {"type": "1 BHK", "area": "620 sq.ft", "price": "₹32 Lakh + Taxes", "status": "Available"},
            {"type": "2 BHK", "area": "910 sq.ft", "price": "₹45 Lakh + Taxes", "status": "Available"},
        ]
    },
    "Marathe Pride": {
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East, Maharashtra",
        "map_link": "https://www.google.com/maps?q=Marathe+Pride+Ambernath",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Pride.avif",
        "flats": [
            {"type": "1 BHK", "area": "640 sq.ft", "price": "₹32 Lakh + Taxes", "status": "Available"},
            {"type": "2 BHK", "area": "900 sq.ft", "price": "₹47 Lakh + Taxes", "status": "Available"},
        ]
    }
}

completed_projects = [
    {"name": "Marathe Empress", "location": "Titwala (E)", "address": "Jagat Naka, Titwala East, Maharashtra",
     "map_link": "https://www.google.com/maps?q=Marathe+Empress+Titwala",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Empress.webp?raw=true"},
    {"name": "Marathe Height", "location": "Titwala (E)", "address": "Near Ghar Aangan, Titwala East, Maharashtra",
     "map_link": "https://www.google.com/maps?q=Marathe+Height+Titwala",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/marathe%20Height.png?raw=true"},
    {"name": "Marathe Fortune", "location": "Titwala (E)", "address": "Ganesh Mandir Road, Titwala East, Maharashtra",
     "map_link": "https://www.google.com/maps?q=Marathe+Fortune+Titwala",
     "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/refs/heads/main/images/Marathe%20Fortune.avif"},
    {"name": "Marathe Empire", "location": "Titwala (E)", "address": "Near Mahaganpati Hospital, Titwala East, Maharashtra",
     "map_link": "https://www.google.com/maps?q=Marathe+Empire+Titwala",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Empire.jpg?raw=true"},
    {"name": "Marathe Elenza", "location": "Shahad (W)", "address": "Sales Office, Shahad West, Maharashtra",
     "map_link": "https://www.google.com/maps?q=Marathe+Elenza+Shahad",
     "image": "https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Elenza.jpeg?raw=true",
     "flats": [
        {"type": "2 BHK", "area": "1100 sq.ft", "price": "₹90 Lakh", "status": "Available"},
        {"type": "3 BHK", "area": "1450 sq.ft", "price": "₹1.2 Crore", "status": "Available"},
     ]},
]

# ----------------- STYLING FOR FLAT CARDS -----------------
st.markdown("""
<style>
.flat-card {
    background: linear-gradient(135deg, #2d2d2d, #1e1e1e);
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.3);
    color: white;
    transition: all 0.3s ease-in-out;
}
.flat-card:hover {
    transform: scale(1.02);
    box-shadow: 0px 0px 25px rgba(255, 215, 0, 0.6);
}
.flat-type {
    font-size: 22px;
    font-weight: bold;
    color: #FFD700;
}
.flat-price {
    font-size: 18px;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Ongoing Projects", "🏠 Completed Projects", "📝 Enquiry Form", "📞 Contact Info"])

# ----------------- ONGOING PROJECTS -----------------
with tab1:
    st.subheader("🏗️ Ongoing Projects")
    for name, data in projects.items():
        st.image(data["image"], caption=name, use_column_width=True)
        st.markdown(f"🏢 **Project:** {name}")
        st.markdown(f"📍 **Location:** {data['location']}")
        st.markdown(f"🏠 **Address:** {data['address']}")
        st.markdown(f"🧭 [View on Google Maps]({data['map_link']})")

        st.markdown("### 🏡 Available Flats:")
        for flat in data["flats"]:
            st.markdown(
                f"""
                <div class='flat-card'>
                    <div class='flat-type'>🏠 {flat['type']}</div>
                    <div class='flat-price'>📏 {flat['area']} | 💰 {flat['price']} | 🟢 {flat['status']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button(f"📅 Book a Visit for {name}", key=f"visit_{name}"):
            st.session_state["selected_project"] = name
            st.success(f"Redirecting to enquiry form for {name}... Go to the 📝 Enquiry Form tab below 👇")

        st.markdown("---")

# ----------------- ENQUIRY FORM -----------------
with tab3:
    st.subheader("📝 Flat Enquiry Form")
    st.write("Please fill the form below and our team will contact you soon:")

    excel_path = "enquiries.xlsx"
    if not os.path.exists(excel_path):
        pd.DataFrame(columns=["Name", "Phone", "Project", "Message", "Timestamp"]).to_excel(excel_path, index=False)

    selected_project = st.session_state.get("selected_project", None)
    project = st.selectbox("Select Project", list(projects.keys()) + [p["name"] for p in completed_projects],
                           index=(list(projects.keys()) + [p["name"] for p in completed_projects]).index(selected_project)
                           if selected_project else 0)

    with st.form("enquiry_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
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

# ----------------- CONTACT INFO -----------------
with tab4:
    st.subheader("📞 Contact Information")
    st.markdown("""  
    ⏰ **Working Hours:** 10:00 AM – 07:00 PM (Mon – Sun)  
    📞 **Contact Number:** +91 7045871101  
    💬 **WhatsApp:** [Chat Now](https://wa.me/917045871101)  
    ✉️ **Email:** marathegroup1101@gmail.com  
    👤 **Owner:** Parasana Ramesh Marathe   
    """)
    st.caption("© 2025 Marathe Group | Designed and Developed by Marathe Group 💻")

# ----------------- FLOATING CONTACT BUTTON -----------------
st.markdown("""
<style>
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.6); }
  70% { box-shadow: 0 0 0 25px rgba(255, 215, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
}
.floating-btn {
    position: fixed;
    width: 70px;
    height: 70px;
    bottom: 25px;
    right: 25px;
    background: linear-gradient(135deg, #FFD700, #ffcc00);
    color: black;
    border-radius: 50%;
    text-align: center;
    font-size: 32px;
    animation: pulse 2s infinite;
    z-index: 999;
    cursor: pointer;
}
.contact-options {
    position: fixed;
    bottom: 100px;
    right: 35px;
    z-index: 998;
    display: none;
}
.contact-options a {
    display: block;
    background-color: white;
    color: black;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    text-decoration: none;
    font-weight: 500;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
.contact-options a:hover {
    background-color: #FFD700;
}
</style>

<div class="floating-btn" id="contactBtn">📞</div>

<div class="contact-options" id="contactOptions">
    <a href="https://wa.me/917045871101" target="_blank">💬 WhatsApp</a>
    <a href="tel:+917045871101">📲 Call Now</a>
    <a href="mailto:marathegroup1101@gmail.com">✉️ Email</a>
</div>

<script>
const btn = document.getElementById('contactBtn');
const options = document.getElementById('contactOptions');
let isVisible = false;
btn.addEventListener('click', () => {
    options.style.display = isVisible ? 'none' : 'block';
    isVisible = !isVisible;
});
</script>
""", unsafe_allow_html=True)
