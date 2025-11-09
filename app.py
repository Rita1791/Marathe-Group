# app.py - Marathe Group (Professional site + AI assistant)
import streamlit as st
import pandas as pd
import datetime
import os
import difflib
import openai
from dotenv import load_dotenv

# Load .env locally if present
load_dotenv()

# ----------------- Config -----------------
st.set_page_config(page_title="Marathe Group", page_icon="🏢", layout="wide")

# Try to get OpenAI key from Streamlit secrets, then env
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# ----------------- SITE DATA (single source of truth) -----------------
PROJECTS = {
    "Marathe Sapphire": {
        "location": "Titwala (E)",
        "address": "Swami Vivekanand Chowk Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Sapphire+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Sapphire.avif",
        "flats": {
            "1 BHK": {"area": "650 sq.ft", "price": "₹38 Lakh (Incl. Taxes)"},
            "2 BHK": {"area": "950 sq.ft", "price": "₹55 Lakh (Incl. Taxes)"}
        }
    },
    "Marathe Tower": {
        "location": "Titwala (E)",
        "address": "Digi1 Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Tower+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Tower.jpg",
        "flats": {
            "1 BHK": {"area": "620 sq.ft", "price": "₹32 Lakh + Taxes"},
            "2 BHK": {"area": "910 sq.ft", "price": "₹45 Lakh + Taxes"}
        }
    },
    "Marathe Pride": {
        "location": "Ambernath (E)",
        "address": "Plot No. 220 & 221, Ambernath East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Pride+Ambernath",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Pride.avif",
        "flats": {
            "1 BHK": {"area": "640 sq.ft", "price": "₹32 Lakh + Taxes"},
            "2 BHK": {"area": "900 sq.ft", "price": "₹47 Lakh + Taxes"}
        }
    },
    "Marathe Elenza": {
        "location": "Shahad (W)",
        "address": "Sales Office, Shahad West, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Elenza+Shahad",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Elenza.jpeg",
        "flats": {
            "2 BHK": {"area": "1100 sq.ft", "price": "₹90 Lakh"},
            "3 BHK": {"area": "1450 sq.ft", "price": "₹1.2 Crore"}
        }
    },
    "Marathe Empire": {
        "location": "Titwala (E)",
        "address": "Near Mahaganpati Hospital, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Empire+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Empire.jpg"
    },
    "Marathe Height": {
        "location": "Titwala (E)",
        "address": "Near Ghar Aangan, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Height+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/marathe%20Height.png"
    },
    "Marathe Fortune": {
        "location": "Titwala (E)",
        "address": "Ganesh Mandir Road, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Fortune+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Fortune.avif"
    },
    "Marathe Empress": {
        "location": "Titwala (E)",
        "address": "Jagat Naka, Titwala East, Maharashtra",
        "map": "https://www.google.com/maps?q=Marathe+Empress+Titwala",
        "image": "https://raw.githubusercontent.com/Rita1791/Marathe-Group/main/images/Marathe%20Empress.webp"
    }
}

# Build a small FAQ knowledge base (fallback)
KB = {
    "hours": "Working Hours: 10:00 AM – 07:00 PM (Mon–Sun). Reach us via phone/WhatsApp during these hours.",
    "contact": "Phone: +91 7045871101 · WhatsApp: https://wa.me/917045871101 · Email: marathegroup1101@gmail.com",
    "marathe elenza price": "Marathe Elenza prices: 2 BHK — ₹90 Lakh, 3 BHK — ₹1.2 Crore.",
    "booking process": "Booking: 1) Contact sales → 2) Pay booking amount → 3) Sign agreement → 4) Office issues receipts. We'll verify documents at the main office.",
    "documents": "Customers can view/download booking agreement and receipts from the Customer Portal once verified.",
    "payment schedule": "Typical plan: Initial booking, staged construction-linked payments, final payment at handover. Contact sales for exact schedule."
}

# Helper to run fuzzy match against KB and project names
def local_answer(query: str):
    q = query.lower()
    # check project names
    names = list(PROJECTS.keys())
    match = difflib.get_close_matches(q, names, n=1, cutoff=0.5)
    if match:
        p = match[0]
        info = PROJECTS[p]
        flats = info.get("flats", {})
        flat_lines = []
        for ft, meta in flats.items():
            flat_lines.append(f"{ft}: {meta.get('area','')} — {meta.get('price','')}")
        flats_text = "\n".join(flat_lines) if flat_lines else "No flat details available."
        return f"**{p}** — {info.get('address')}\n\nAvailable types:\n{flats_text}\n\nGoogle Maps: {info.get('map')}"
    # check KB
    keys = list(KB.keys())
    best = difflib.get_close_matches(q, keys, n=1, cutoff=0.4)
    if best:
        return KB[best[0]]
    # some direct keywords
    if "price" in q:
        # try to find project mention in query
        for p in PROJECTS:
            if p.lower() in q:
                flats = PROJECTS[p].get("flats", {})
                return " ; ".join([f"{k}: {v['price']}" for k, v in flats.items()]) if flats else "Price info not available."
    return None

# OpenAI call wrapper
def ask_openai_chat(system_prompt, user_prompt, api_key=None, model="gpt-3.5-turbo", max_tokens=400):
    if not api_key:
        raise RuntimeError("OpenAI API key not provided.")
    # construct messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.1,
        n=1
    )
    return resp.choices[0].message.content.strip()

# Simple chat UI helpers
def render_chat_messages():
    for i, msg in enumerate(st.session_state["chat_history"]):
        role = msg["role"]
        text = msg["content"]
        if role == "user":
            st.markdown(f"<div style='text-align:right; background:#0f0f0f; padding:10px; border-radius:10px; margin-bottom:6px;'>{text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; background:#111; padding:12px; border-radius:10px; margin-bottom:8px; border:1px solid rgba(255,215,0,0.08);'>{text}</div>", unsafe_allow_html=True)

# ----------------- UI (header + layout) -----------------
st.markdown("""
<style>
body {background-color:#050505;}
.header {text-align:center; padding-top:12px;}
.logo {width:220px; border-radius:12px; box-shadow: 0 10px 30px rgba(255,215,0,0.12);}
.h1 {color:#FFD700; font-size:36px; font-weight:700;}
.h2 {color:#FFD700;}
.card {background:#121212; border:1px solid rgba(255,215,0,0.06); padding:16px; border-radius:12px; margin-bottom:16px;}
.small{color:gray; font-size:14px;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="header">
  <img class="logo" src="https://github.com/Rita1791/Marathe-Group/blob/main/images/Marathe%20Group%20Logo.webp?raw=true" />
  <div class="h1">🏢 Marathe Group</div>
  <div class="small">Luxury Living • Trusted Legacy</div>
</div>
""", unsafe_allow_html=True)

# Video highlight
st.markdown("---")
st.markdown("### Marathe Elenza — Featured")
st.video("https://github.com/Rita1791/Marathe-Group/raw/refs/heads/main/images/MG%20Video.mp4")
st.markdown("---")

# Projects summary (compact)
st.markdown("### Projects at a glance")
cols = st.columns(3)
project_keys = list(PROJECTS.keys())
for i, col in enumerate(cols):
    for p in project_keys[i::3]:
        with col:
            st.image(PROJECTS[p]["image"], use_column_width=True, caption=p)
            st.markdown(f"**{p}**  \n{PROJECTS[p]['address']}  \n[{PROJECTS[p]['map']}]({PROJECTS[p]['map']})")
            # small book button
            if st.button(f"Book — {p}", key=f"book_{p}"):
                st.session_state["book_target"] = p
                st.experimental_rerun()
st.markdown("---")

# Enquiry form area (keeps working)
st.markdown("### Enquiry")
excel_path = "enquiries.xlsx"
if not os.path.exists(excel_path):
    pd.DataFrame(columns=["Name","Phone","Project","Message","Timestamp"]).to_excel(excel_path, index=False)

with st.form("enquiry_form", clear_on_submit=False):
    default_proj = st.session_state.get("book_target", None)
    name = st.text_input("Full Name", key="enq_name")
    phone = st.text_input("Phone Number", key="enq_phone")
    project = st.selectbox("Select Project", list(PROJECTS.keys()), index=list(PROJECTS.keys()).index(default_proj) if default_proj in PROJECTS else 0, key="enq_project")
    message = st.text_area("Message (optional)", key="enq_msg")
    submitted = st.form_submit_button("Submit Enquiry")
    if submitted:
        if not name or not phone:
            st.error("Please enter name and phone.")
        else:
            df = pd.read_excel(excel_path)
            df.loc[len(df)] = [name, phone, project, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            df.to_excel(excel_path, index=False)
            st.success(f"Thank you {name}! We recorded your enquiry for {project}.")
            # reset book_target so the next user isn't preselected
            if "book_target" in st.session_state:
                del st.session_state["book_target"]

st.markdown("---")

# ----------------- Customer Portal (minimal, for professional flow) -----------------
st.markdown("### Customer Portal")
cust_path = "customer_users.xlsx"
if not os.path.exists(cust_path):
    pd.DataFrame(columns=["Name","Email","Password","Project","Approved"]).to_excel(cust_path, index=False)

c_tab = st.tabs(["Customer Login/Register", "Admin — Approvals & Downloads"])
with c_tab[0]:
    st.subheader("Register")
    r_name = st.text_input("Name", key="reg_name")
    r_email = st.text_input("Official Email", key="reg_email")
    r_pass = st.text_input("Set Password", type="password", key="reg_pass")
    r_proj = st.selectbox("Project", list(PROJECTS.keys()), key="reg_proj")
    if st.button("Register (Request verification)", key="reg_btn"):
        df = pd.read_excel(cust_path)
        df.loc[len(df)] = [r_name, r_email, r_pass, r_proj, "Pending"]
        df.to_excel(cust_path, index=False)
        st.success("Registration submitted. Office will verify and approve within working hours.")

    st.markdown("---")
    st.subheader("Login")
    lg_email = st.text_input("Email", key="lg_email")
    lg_pass = st.text_input("Password", type="password", key="lg_pass")
    if st.button("Login", key="lg_btn"):
        df = pd.read_excel(cust_path)
        user = df[(df["Email"] == lg_email) & (df["Password"] == lg_pass)]
        if user.empty:
            st.error("Invalid credentials.")
        else:
            if user["Approved"].iloc[0] == "Yes":
                st.success(f"Welcome {user['Name'].iloc[0]} — Verified Customer.")
                st.markdown("**Your documents & payments**")
                # sample docs - replace with real links or S3 links
                st.markdown("- [Booking Agreement (PDF)](https://example.com/agreement.pdf)")
                st.markdown("- [Payment Receipt (PDF)](https://example.com/receipt.pdf)")
                st.markdown("**Payment summary**")
                st.progress(60)
                st.markdown("Next due: 15th Dec 2025")
            else:
                st.warning("Account pending approval. Contact office if delayed.")

with c_tab[1]:
    st.subheader("Admin — Approvals & Downloads (Office use)")
    admin_pass = st.text_input("Admin password", type="password", key="admin_pw")
    if admin_pass == "Marathe@Admin2025":
        st.success("Admin access granted.")
        # Approve users
        df = pd.read_excel(cust_path)
        st.dataframe(df)
        st.markdown("**Approve a user by row index**")
        idx = st.number_input("Row index to approve", min_value=0, max_value=max(0, len(df)-1), step=1)
        if st.button("Approve selected"):
            df.loc[idx, "Approved"] = "Yes"
            df.to_excel(cust_path, index=False)
            st.success("User approved.")
        # Download enquiries
        if os.path.exists(excel_path):
            with open(excel_path, "rb") as f:
                st.download_button("Download Enquiries (Excel)", f, file_name="enquiries.xlsx")
    elif admin_pass:
        st.error("Incorrect admin password.")

st.markdown("---")

# ----------------- Gallery -----------------
st.markdown("### Gallery & Project Updates")
# Use your own images - placeholders used here
st.image([
    "https://images.unsplash.com/photo-1560185008-5b12a1e0e27d",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
    "https://images.unsplash.com/photo-1600607687920-4e24d07d1c07"
], caption=["Elenza Exterior","Luxury Interiors","Amenities"], use_column_width=True)

st.markdown("---")

# ----------------- AI ASSISTANT (Ask Marathe AI) -----------------
st.markdown("### 🤖 Ask Marathe AI — (project-aware assistant)")

# initialize chat session
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Hello — I'm Marathe AI. Ask me about projects, prices, booking steps, documents, or how to reach the office."}
    ]

render_chat_messages()

user_input = st.text_input("Type your question here (e.g. 'Is 2 BHK available in Elenza?')", key="ai_input")
if st.button("Send", key="ai_send"):
    if not user_input.strip():
        st.warning("Please type a question.")
    else:
        # append user message
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        # First try local KB
        local_resp = local_answer(user_input)
        if local_resp and not OPENAI_API_KEY:
            # fallback: use local answer when no OpenAI key
            st.session_state["chat_history"].append({"role": "assistant", "content": local_resp})
            render_chat_messages()
        else:
            # Build system prompt with concise project context
            project_summary_lines = []
            for name, info in PROJECTS.items():
                flats = info.get("flats", {})
                flats_summary = "; ".join([f"{ft}={meta['price']}" for ft, meta in flats.items()]) if flats else "No flats listed"
                project_summary_lines.append(f"{name} | {info.get('location')} | {info.get('address')} | {flats_summary}")
            system_prompt = (
                "You are Marathe Group assistant. Use the following project data to answer exactly and professionally. "
                "If the user asks for steps (booking/document/payment), be concise and give clear next steps. "
                "Be friendly, formal and brief.\n\nProjects:\n" + "\n".join(project_summary_lines)
            )

            # Call OpenAI (if available)
            if OPENAI_API_KEY:
                try:
                    answer = ask_openai_chat(system_prompt, user_input, api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
                except Exception as e:
                    # fallback to local
                    answer = local_resp or "Sorry, I couldn't fetch an online answer — please contact sales at +91 7045871101."
                    st.error(f"(OpenAI API error: {str(e)})")
            else:
                # If no API key but local_resp exists, use it, else generic fallback
                answer = local_resp or "I don't have an internet AI connected. Please contact sales: +91 7045871101."

            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            render_chat_messages()

st.markdown("---")

# ----------------- Contact footer -----------------
st.markdown("""
<div style="background:#0d0d0d; padding:12px; border-radius:8px;">
**Contact:** +91 7045871101 · <a href="https://wa.me/917045871101">WhatsApp</a> · marathegroup1101@gmail.com  
Working hours: 10:00 AM–07:00 PM (Mon–Sun)
</div>
""", unsafe_allow_html=True)
