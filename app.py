import streamlit as st
import pandas as pd
import datetime
import os
import difflib
import openai
from dotenv import load_dotenv

# ----------------- CONFIGURATION -----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

load_dotenv()
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# ----------------- PROJECT DATABASE -----------------
PROJECTS = {
    "Marathe Elenza": {
        "location": "Shahad (W)",
        "address": "Sales Office, Shahad West, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Elenza+Shahad",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Elenza.jpeg",
        "flats": {
            "2 BHK": {"area": "1100 sq.ft", "price": "₹90 Lakh"},
            "3 BHK": {"area": "1450 sq.ft", "price": "₹1.2 Crore"}
        },
        "bookable": True
    },
    "Marathe Tower": {
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Tower+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Tower.jpg",
        "flats": {
            "1 BHK": {"area": "620 sq.ft", "price": "₹32 Lakh + Taxes"},
            "2 BHK": {"area": "910 sq.ft", "price": "₹45 Lakh + Taxes"}
        },
        "bookable": True
    },
    "Marathe Pride": {
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Pride+Ambernath",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Pride.avif",
        "flats": {
            "1 BHK": {"area": "640 sq.ft", "price": "₹32 Lakh + Taxes"},
            "2 BHK": {"area": "900 sq.ft", "price": "₹47 Lakh + Taxes"}
        },
        "bookable": True
    },
    # 🆕 NEW PROJECT ADDED HERE
    "Marathe Icon": {
        "location": "Titwala (E)",
        "address": "Near Hari Om Valley, Digi1 Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Icon+Titwala",
        "image": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=1000&q=80",  # You can replace with your own image later
        "flats": {
            "1 BHK": {"area": "650 sq.ft", "price": "₹34 Lakh (Expected)"},
            "2 BHK": {"area": "940 sq.ft", "price": "₹49 Lakh (Expected)"}
        },
        "bookable": False  # Coming soon — not bookable yet
    },
    "Marathe Sapphire": {
        "location": "Titwala (E)",
        "address": "Swami Vivekanand Chowk Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Sapphire+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Sapphire.avif",
        "flats": {
            "1 BHK": {"area": "650 sq.ft", "price": "₹38 Lakh (Incl. Taxes)"},
            "2 BHK": {"area": "950 sq.ft", "price": "₹55 Lakh (Incl. Taxes)"}
        },
        "bookable": False
    },
    "Marathe Empire": {
        "location": "Titwala (E)",
        "address": "Near Mahaganpati Hospital, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Empire+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Empire.jpg",
        "bookable": False
    },
    "Marathe Height": {
        "location": "Titwala (E)",
        "address": "Near Ghar Aangan, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Height+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe%20Height.png",
        "bookable": False
    },
    "Marathe Fortune": {
        "location": "Titwala (E)",
        "address": "Ganesh Mandir Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Fortune+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Fortune.avif",
        "bookable": False
    },
    "Marathe Empress": {
        "location": "Titwala (E)",
        "address": "Jagat Naka, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Empress+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Empress.webp",
        "bookable": False
    }
}

BOOKABLE = [p for p, d in PROJECTS.items() if d.get("bookable")]

# ----------------- UI HEADER -----------------
st.markdown("""
    <style>
    body {background-color:#0b0b0b; color:white; font-family:'Poppins', sans-serif;}
    h2, h3, h4 {color:#FFD700;}
    .card {background:#141414; border:1px solid rgba(255,215,0,0.3); border-radius:15px; padding:20px; margin-bottom:25px;}
    .book-btn {color:#FFD700; font-weight:bold; text-decoration:none;}
    .disabled {color:gray; font-style:italic;}
    </style>
""", unsafe_allow_html=True)

st.image("https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true", width=220)
st.markdown("<h1 style='color:#FFD700;'>🏢 Marathe Group</h1>", unsafe_allow_html=True)
st.video("https://github.com/Rita1791/Marathe-Group/raw/refs/heads/main/images/MG%20Video.mp4")
st.markdown("---")

# ----------------- PROJECT SECTION -----------------
st.subheader("🏗️ Our Projects")

for name, data in PROJECTS.items():
    st.image(data["image"], caption=name, use_column_width=True)
    st.markdown(f"📍 **Location:** {data['location']}  \n🏠 **Address:** {data['address']}")
    if "flats" in data:
        st.markdown("### 💰 Price Details:")
        for flat_type, info in data["flats"].items():
            st.markdown(f"- {flat_type}: {info['area']} — {info['price']}")
    if data.get("bookable"):
        if st.button(f"🟢 Book Now — {name}", key=f"book_{name}"):
            st.session_state["selected_project"] = name
    else:
        st.markdown("<p class='disabled'>Bookings Closed / Coming Soon</p>", unsafe_allow_html=True)
    st.markdown("---")

# ----------------- ENQUIRY FORM -----------------
st.subheader("📝 Flat Enquiry Form (Only for Active Projects)")

excel_path = "enquiries.xlsx"
if not os.path.exists(excel_path):
    pd.DataFrame(columns=["Name", "Phone", "Project", "Message", "Timestamp"]).to_excel(excel_path, index=False)

with st.form("enquiry_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    project = st.selectbox("Select Project", BOOKABLE)
    message = st.text_area("Additional Message")
    submit = st.form_submit_button("Submit Enquiry")

    if submit:
        if not name or not phone:
            st.error("Please enter both Name and Phone Number.")
        else:
            df = pd.read_excel(excel_path)
            df.loc[len(df)] = [name, phone, project, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            df.to_excel(excel_path, index=False)
            st.success(f"✅ Thank you {name}! Your enquiry for **{project}** has been recorded.")

st.markdown("---")

# ----------------- AI ASSISTANT -----------------
st.subheader("🤖 Ask Marathe AI")

def local_answer(q):
    q = q.lower()
    for p, d in PROJECTS.items():
        if p.lower() in q:
            flats = d.get("flats", {})
            price_info = "; ".join([f"{f} - {v['price']}" for f, v in flats.items()]) if flats else "No pricing data."
            return f"**{p}** — Located at {d['address']} ({d['location']}). Prices: {price_info}."
    if "price" in q:
        return "Bookable projects: Elenza (₹90L+), Tower (₹32–45L), Pride (₹32–47L). New project Icon coming soon!"
    if "contact" in q:
        return "📞 +91 7045871101 | ✉️ marathegroup1101@gmail.com | 📍 Titwala East, Maharashtra"
    return None

if "chat" not in st.session_state:
    st.session_state.chat = [{"role": "assistant", "content": "Hello 👋 I'm Marathe AI. Ask about projects, pricing, or booking!"}]

for msg in st.session_state.chat:
    align = "right" if msg["role"] == "user" else "left"
    st.markdown(f"<div style='text-align:{align}; margin:5px 0;'><b>{msg['content']}</b></div>", unsafe_allow_html=True)

user_q = st.text_input("Your Question:")
if st.button("Ask"):
    if user_q:
        st.session_state.chat.append({"role": "user", "content": user_q})
        reply = local_answer(user_q)
        if not reply and OPENAI_API_KEY:
            try:
                prompt = f"You are Marathe AI, assistant for Marathe Group. Use these projects: {', '.join(PROJECTS.keys())}."
                ans = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_q}],
                    max_tokens=250
                )
                reply = ans.choices[0].message.content
            except:
                reply = "I'm having trouble accessing live info now, please contact sales ☎️ +91 7045871101."
        elif not reply:
            reply = "I'm here to help! You can ask about Elenza, Tower, Pride or our upcoming project — Marathe Icon."
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.experimental_rerun()

st.markdown("---")

# ----------------- CONTACT INFO -----------------
st.subheader("📞 Contact Information")
st.markdown("""
📍 **Office:** Titwala (E), Maharashtra  
⏰ **Working Hours:** 10:00 AM – 07:00 PM (Mon – Sun)  
📞 **Contact:** +91 7045871101  
💬 **WhatsApp:** [Chat Now](https://wa.me/917045871101)  
✉️ **Email:** marathegroup1101@gmail.com  
👤 **Owner:** Parasana Ramesh Marathe  
""")

st.caption("© 2025 Marathe Group | Designed & Developed by Ritika Rawat 💻")
