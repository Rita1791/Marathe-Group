import streamlit as st
import pandas as pd
import datetime
import os

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

# ----------------- CUSTOM STYLES -----------------
st.markdown("""
    <style>
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #0b0b0b;
        color: white;
    }
    .navbar {
        position: fixed; top:0; left:0; width:100%;
        background: rgba(20,20,20,0.95);
        padding: 15px 0;
        z-index: 999;
        text-align:center;
        border-bottom: 1px solid rgba(255,215,0,0.3);
    }
    .navbar a {
        text-decoration:none;
        color:#FFD700;
        margin:0 25px;
        font-weight:600;
        font-size:16px;
        transition:0.3s;
    }
    .navbar a:hover { color:white; }
    .hero { text-align:center; margin-top:90px; padding:40px 10px;
        background:linear-gradient(to bottom,#1a1a1a,#0b0b0b);}
    .hero h1{color:#FFD700;font-size:50px;text-shadow:1px 1px 10px rgba(255,215,0,0.8);}
    .hero h4{color:gray;font-size:20px;font-weight:300;}
    h2{color:#FFD700;text-align:center;margin-top:60px;}
    .card{background:#141414;border:1px solid rgba(255,215,0,0.3);
        border-radius:15px;padding:20px;margin-bottom:30px;
        box-shadow:0px 0px 15px rgba(255,215,0,0.2);}
    .floating-btn{position:fixed;bottom:25px;right:25px;z-index:999;}
    .floating-btn a{
        display:block;margin-top:10px;text-decoration:none;
        background:linear-gradient(45deg,#FFD700,#b59410);
        color:black;font-weight:bold;padding:12px 18px;border-radius:50px;
        box-shadow:0px 0px 10px rgba(255,215,0,0.6);text-align:center;
        transition:all 0.3s ease-in-out;}
    .floating-btn a:hover{background:white;color:black;
        box-shadow:0px 0px 20px rgba(255,215,0,0.9);transform:scale(1.05);}
    </style>
""", unsafe_allow_html=True)

# ----------------- NAVBAR -----------------
st.markdown("""
<div class="navbar">
    <a href="#home">Home</a>
    <a href="#projects">Projects</a>
    <a href="#enquiry">Enquiry</a>
    <a href="#portal">Customer Portal</a>
    <a href="#gallery">Gallery</a>
    <a href="#contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# ----------------- HERO -----------------
st.markdown("""
<div id="home" class="hero">
    <img src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true"
         width="250" style="border-radius:15px; margin-bottom:20px;">
    <h1>🏢 Marathe Group</h1>
    <h4>Luxury Living • Trusted Legacy</h4>
</div>
""", unsafe_allow_html=True)
st.video("https://github.com/Rita1791/Marathe-Group/raw/refs/heads/main/images/MG%20Video.mp4")

st.markdown("<p style='text-align:center;color:gray;'>Building trust and timeless spaces since 1995.</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- PROJECTS -----------------
st.markdown("<h2 id='projects'>🏗️ Our Projects</h2>", unsafe_allow_html=True)
projects = {
    "Marathe Sapphire": "₹38 L (Inc Taxes) – 1 BHK | ₹55 L (Inc Taxes) – 2 BHK",
    "Marathe Pride": "₹32 L + Taxes – 1 BHK | ₹47 L + Taxes – 2 BHK",
    "Marathe Tower": "₹32 L – 1 BHK | ₹45 L – 2 BHK",
    "Marathe Elenza": "₹90 L – 2 BHK | ₹1.2 Cr – 3 BHK"
}
for project, price in projects.items():
    st.markdown(f"""
    <div class="card">
        <h3 style="color:#FFD700;">{project}</h3>
        <p style="color:#ccc;">{price}</p>
        <a href="#enquiry" style="color:#FFD700;font-weight:bold;">💛 Book Now</a>
    </div>
    """, unsafe_allow_html=True)

# ----------------- ENQUIRY FORM -----------------
st.markdown("<h2 id='enquiry'>📝 Enquiry Form</h2>", unsafe_allow_html=True)
excel_path="enquiries.xlsx"
if not os.path.exists(excel_path):
    pd.DataFrame(columns=["Name","Phone","Project","Message","Timestamp"]).to_excel(excel_path,index=False)
with st.form("enquiry"):
    n=st.text_input("Full Name")
    ph=st.text_input("Phone Number")
    proj=st.selectbox("Select Project",list(projects.keys()))
    msg=st.text_area("Additional Message")
    sub=st.form_submit_button("Submit Enquiry")
    if sub:
        if n and ph:
            df=pd.read_excel(excel_path)
            df.loc[len(df)] = [n,ph,proj,msg,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            df.to_excel(excel_path,index=False)
            st.success(f"✅ Thank you {n}! Your enquiry for {proj} is recorded.")
        else: st.error("⚠️ Please fill all required fields.")
st.markdown("---")

# ----------------- CUSTOMER PORTAL -----------------
st.markdown("<h2 id='portal'>👤 Customer Portal</h2>", unsafe_allow_html=True)
path="customer_users.xlsx"
if not os.path.exists(path):
    pd.DataFrame(columns=["Name","Email","Password","Project","Approved"]).to_excel(path,index=False)
tab1,tab2=st.tabs(["Login","Register"])
with tab2:
    nm=st.text_input("Full Name",key="nm")
    em=st.text_input("Email ID",key="em")
    pw=st.text_input("Set Password",type="password",key="pw")
    pj=st.selectbox("Your Project",list(projects.keys()),key="pj")
    if st.button("Register"):
        df=pd.read_excel(path)
        df.loc[len(df)]=[nm,em,pw,pj,"Pending"]
        df.to_excel(path,index=False)
        st.success("✅ Registration submitted! Office will verify soon.")
with tab1:
    le=st.text_input("Email",key="le")
    lp=st.text_input("Password",type="password",key="lp")
    if st.button("Login"):
        df=pd.read_excel(path)
        user=df[(df["Email"]==le)&(df["Password"]==lp)]
        if not user.empty:
            if user["Approved"].iloc[0]=="Yes":
                st.success(f"Welcome {user['Name'].iloc[0]} 👋")
                st.markdown(f"🏢 Project: **{user['Project'].iloc[0]}**")
                st.markdown("<h3 style='color:#FFD700;'>📊 Dashboard</h3>",unsafe_allow_html=True)
                st.progress(80)
                col1,col2=st.columns(2)
                with col1:
                    st.markdown("<div class='card'><b>💰 Payment Status</b><br>Paid: ₹45 L  |  Pending: ₹10 L<br>Next Due: Dec 2025</div>",unsafe_allow_html=True)
                with col2:
                    st.markdown("<div class='card'><b>📄 Documents</b><br><a href='https://example.com/agreement.pdf' target='_blank'>Agreement</a><br><a href='https://example.com/receipt.pdf' target='_blank'>Receipts</a></div>",unsafe_allow_html=True)
                st.markdown("<div class='card'><b>🏗️ Construction Update</b><br>Flooring work in progress – Handover expected April 2026.</div>",unsafe_allow_html=True)
                st.markdown("<div class='card'><b>🧾 Service Request</b></div>",unsafe_allow_html=True)
                q=st.text_area("Describe your issue:")
                if st.button("Submit Request"): st.success("✅ Your request has been submitted.")
            else: st.warning("⏳ Awaiting office approval.")
        else: st.error("❌ Invalid credentials.")

# ----------------- GALLERY -----------------
st.markdown("<h2 id='gallery'>📸 Project Gallery</h2>", unsafe_allow_html=True)
st.image([
    "https://images.unsplash.com/photo-1560185008-5b12a1e0e27d",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
    "https://images.unsplash.com/photo-1600607687920-4e24d07d1c07"
], caption=["Elenza Exterior","Luxury Interiors","Amenities Zone"], use_column_width=True)
st.video("https://github.com/Rita1791/Marathe-Group/raw/refs/heads/main/images/MG%20Video.mp4")

# ----------------- AI CHATBOT (Simple) -----------------
st.markdown("<h2 style='color:#FFD700;'>🤖 Ask Marathe AI</h2>", unsafe_allow_html=True)
prompt = st.text_input("Ask anything about Marathe Group projects:")
if prompt:
    st.write("💬 Marathe AI:", "We’re here to assist you! Our sales team will contact you shortly.")

# ----------------- CONTACT -----------------
st.markdown("<h2 id='contact'>📞 Contact Us</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
<p>⏰ <b>Hours:</b> 10 AM–7 PM</p>
<p>📞 <b>Phone:</b> +91 7045871101</p>
<p>💬 <b>WhatsApp:</b> <a href='https://wa.me/917045871101' target='_blank' style='color:#FFD700;'>Chat Now</a></p>
<p>✉️ <b>Email:</b> marathegroup1101@gmail.com</p>
<p>👤 <b>Owner:</b> Parasana Ramesh Marathe</p>
</div>
<p style='text-align:center;color:gray;'>© 2025 Marathe Group | Designed by Ritika Rawat 💻</p>
""", unsafe_allow_html=True)

# ----------------- FLOATING BUTTONS -----------------
st.markdown("""
<div class='floating-btn'>
    <a href='#enquiry'>📩 Enquiry</a>
    <a href='https://wa.me/917045871101' target='_blank'>💬 WhatsApp</a>
</div>
""", unsafe_allow_html=True)
