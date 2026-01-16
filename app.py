import streamlit as st
import pandas as pd
import os
from streamlit_mic_recorder import mic_recorder

# --- 1. SETTINGS ---
st.set_page_config(page_title="AgriBridge AI", page_icon="🌾", layout="wide")

# --- 2. MULTI-LANGUAGE DICTIONARY ---
LANG_DATA = {
    "English": {
        "home": "Home", "farmer_tab": "Hire Labor", "labor_tab": "Find Work", "market_tab": "Market", "rent_tab": "Rentals", "lease_tab": "Land Lease",
        "name": "Full Name", "loc": "Village", "addr": "Full Address", "phone": "Phone", "crop": "Crop Name", "price": "Price", "qty": "Quantity", "submit": "Submit Details", 
        "call": "📞 Call Now", "near_me": "Search Village", "workers": "Workers Needed", "work_type": "Work Type", "last_date": "Last Date/Expiry", "days": "Rental Days", "house": "House?", "owner": "Owner", "m_name": "Machine Name", "reg_worker": "Register as Worker", "avail_lab": "Available Laborers", "jobs_need": "Jobs Needing Workers"
    },
    "Telugu (తెలుగు)": {
        "home": "హోమ్", "farmer_tab": "కూలీలు కావాలి", "labor_tab": "పని కావాలి", "market_tab": "మార్కెట్", "rent_tab": "యంత్రాలు", "lease_tab": "కౌలు భూమి",
        "name": "పూర్తి పేరు", "loc": "గ్రామం", "addr": "పూర్తి చిరునామా", "phone": "ఫోన్ నంబర్", "crop": "పంట పేరు", "price": "ధర", "qty": "పరిమాణం", "submit": "సమర్పించు", 
        "call": "📞 కాల్ చేయండి", "near_me": "గ్రామం వెతకండి", "workers": "కూలీల సంఖ్య", "work_type": "పని రకం", "last_date": "చివరి తేదీ", "days": "ఎన్ని రోజులు?", "house": "ఇల్లు ఉందా?", "owner": "యజమాని", "m_name": "యంత్రం పేరు", "reg_worker": "కూలీగా నమోదు చేసుకోండి", "avail_lab": "అందుబాటులో ఉన్న కూలీలు", "jobs_need": "పనులు ఉన్నాయి"
    },
    "Hindi (हिन्दी)": {
        "home": "होम", "farmer_tab": "मजदूर चाहिए", "labor_tab": "काम चाहिए", "market_tab": "बाज़ार भाव", "rent_tab": "किराया", "lease_tab": "पट्टा",
        "name": "नाम", "loc": "गाँव", "addr": "पूरा पता", "phone": "फोन", "crop": "फसल", "price": "कीमत", "qty": "मात्रा", "submit": "जमा करें", 
        "call": "📞 कॉल", "near_me": "गाँव खोजें", "workers": "मजदूर संख्या", "work_type": "काम का प्रकार", "last_date": "अंतिम तिथि", "days": "कितने दिन?", "house": "घर है?", "owner": "मालिक", "m_name": "मशीन का नाम", "reg_worker": "मजदूर पंजीकरण", "avail_lab": "उपलब्ध मजदूर", "jobs_need": "काम की जरूरत है"
    },
    "Kannada (ಕನ್ನಡ)": {
        "home": "ಮುಖಪುಟ", "farmer_tab": "ಕೂಲಿ ಬೇಕು", "labor_tab": "ಕೆಲಸ ಬೇಕು", "market_tab": "ಮಾರುಕಟ್ಟೆ", "rent_tab": "ಬಾಡಿಗೆ", "lease_tab": "ಗುತ್ತಿಗೆ",
        "name": "ಹೆಸರು", "loc": "ಗ್ರಾಮ", "addr": "ಪೂರ್ಣ ವಿಳಾಸ", "phone": "ಫೋನ್", "crop": "ಬೆಳೆ", "price": "ಬೆಲೆ", "qty": "ಪ್ರಮಾಣ", "submit": "ಸಲ್ಲಿಸಿ", 
        "call": "📞 ಕರೆ", "near_me": "ಹುಡುಕಿ", "workers": "ಕೂಲಿ ಸಂಖ್ಯೆ", "work_type": "ಕೆಲಸದ ಪ್ರಕಾರ", "last_date": "ಕೊನೆಯ ದಿನಾಂಕ", "days": "ಎಷ್ಟು ದಿನ?", "house": "ಮನೆ ಇದೆಯೇ?", "owner": "ಮಾಲೀಕರು", "m_name": "ಯಂತ್ರದ ಹೆಸರು", "reg_worker": "ಕಾರ್ಮಿಕರ ನೋಂದಣಿ", "avail_lab": "ಲಭ್ಯವಿರುವ ಕಾರ್ಮಿಕರು", "jobs_need": "ಕೆಲಸ ಬೇಕಾಗಿದೆ"
    }
}

# --- 3. DATA FUNCTIONS ---
def save_data(df, filename): df.to_csv(filename, index=False)
def load_data(filename, columns):
    if os.path.exists(filename): return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

# --- 4. UI COMPONENTS ---
selected_lang = st.sidebar.selectbox("Language / భాష", list(LANG_DATA.keys()))
T = LANG_DATA[selected_lang]
menu = st.sidebar.radio("Navigate", [T["home"], T["farmer_tab"], T["labor_tab"], T["market_tab"], T["rent_tab"], T["lease_tab"]])
search_query = st.sidebar.text_input(T["near_me"]).lower()

def voice_input_field(label, key):
    c1, c2 = st.columns([0.85, 0.15])
    with c1: text = st.text_input(label, key=f"in_{key}")
    with c2: 
        st.write(" ")
        mic_recorder(start_prompt="🎙️", stop_prompt="✅", key=f"mic_{key}")
    return text

# --- 5. PAGES ---
if menu == T["home"]:
    st.markdown("<h1 style='text-align: center; color: green;'>🌾 AgriBridge AI</h1>", unsafe_allow_html=True)
    st.divider()
    st.write("### Welcome / స్వాగతం / स्वागत है")

elif menu == T["farmer_tab"]:
    st.header(f"👨‍🌾 {T['farmer_tab']}")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Post a Job")
        with st.container(border=True):
            n = voice_input_field(T["name"], "f_n")
            wt = voice_input_field(T["work_type"], "f_wt")
            l = voice_input_field(T["loc"], "f_l")
            c = st.number_input(T["workers"], 1)
            ld = st.date_input(T["last_date"], key="f_date")
            ph = voice_input_field(T["phone"], "f_ph")
            if st.button(T["submit"]):
                df = load_data('jobs.csv', ["name", "work_type", "loc", "workers", "last_date", "phone"])
                save_data(pd.concat([df, pd.DataFrame([[n, wt, l, c, str(ld), ph]], columns=df.columns)]), 'jobs.csv')
                st.success("Success!")
    with col2:
        st.subheader(T["avail_lab"])
        l_df = load_data('laborers.csv', ["name", "skill", "loc", "phone"])
        for _, row in l_df.iterrows():
            if search_query in str(row['loc']).lower():
                with st.container(border=True):
                    st.write(f"👷 **{row['name']}**")
                    st.write(f"🛠️ {row['skill']} | 📍 {row['loc']}")
                    st.link_button(T["call"], f"tel:{row['phone']}")

elif menu == T["labor_tab"]:
    st.header(f"🔨 {T['labor_tab']}")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(T["reg_worker"])
        with st.container(border=True):
            n = voice_input_field(T["name"], "l_n")
            sk = voice_input_field("Skill", "l_sk")
            l = voice_input_field(T["loc"], "l_l")
            ph = voice_input_field(T["phone"], "l_ph")
            if st.button(T["submit"]):
                df = load_data('laborers.csv', ["name", "skill", "loc", "phone"])
                save_data(pd.concat([df, pd.DataFrame([[n, sk, l, ph]], columns=df.columns)]), 'laborers.csv')
                st.success("Registered!")
    with col2:
        st.subheader(T["jobs_need"])
        j_df = load_data('jobs.csv', ["name", "work_type", "loc", "workers", "last_date", "phone"])
        for _, row in j_df.iterrows():
            if search_query in str(row['loc']).lower():
                with st.container(border=True):
                    st.write(f"💼 **{row['work_type']}**")
                    st.write(f"📅 {row['last_date']} | 📍 {row['loc']}")
                    st.link_button(T["call"], f"tel:{row['phone']}")

elif menu == T["rent_tab"]:
    st.header(f"🚜 {T['rent_tab']}")
    o = voice_input_field(T["owner"], "rt_o")
    m = voice_input_field(T["m_name"], "rt_m")
    l = voice_input_field(T["loc"], "rt_l")
    d = st.number_input(T["days"], 1)
    exp = st.date_input(T["last_date"], key="rt_exp")
    ph = voice_input_field(T["phone"], "rt_ph")
    if st.button(T["submit"]):
        df = load_data('rent.csv', ["owner", "machine", "loc", "days", "expiry", "phone"])
        save_data(pd.concat([df, pd.DataFrame([[o, m, l, d, str(exp), ph]], columns=df.columns)]), 'rent.csv')
        st.rerun()
    r_df = load_data('rent.csv', ["owner", "machine", "loc", "days", "expiry", "phone"])
    for _, row in r_df.iterrows():
        if search_query in str(row['loc']).lower():
            with st.container(border=True):
                st.write(f"⚙️ {row['machine']} | 📅 {row['expiry']}")
                st.write(f"📍 {row['loc']} | 👤 {row['owner']}")
                st.link_button(T["call"], f"tel:{row['phone']}")

elif menu == T["market_tab"]:
    st.header(f"🛒 {T['market_tab']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("🌾 Paddy", "₹2,183/q", "Live")
    c2.metric("☁️ Cotton", "₹7,020/q", "Live")
    c3.metric("🌽 Maize", "₹1,962/q", "Live")
    st.divider()
    n = voice_input_field(T["name"], "mkt_n")
    c = voice_input_field(T["crop"], "mkt_c")
    q = voice_input_field(T["qty"], "mkt_q")
    p = voice_input_field(T["price"], "mkt_p")
    ph = voice_input_field(T["phone"], "mkt_ph")
    if st.button(T["submit"]):
        df = load_data('market.csv', ["name", "crop", "qty", "price", "phone"])
        save_data(pd.concat([df, pd.DataFrame([[n, c, q, p, ph]], columns=df.columns)]), 'market.csv')
        st.rerun()
    m_df = load_data('market.csv', ["name", "crop", "qty", "price", "phone"])
    for _, row in m_df.iterrows():
        st.info(f"🌾 {row['crop']} - ₹{row['price']} | 📞 {row['phone']}")

elif menu == T["lease_tab"]:
    st.header(f"🤝 {T['lease_tab']}")
    o = voice_input_field(T["owner"], "ls_o")
    sz = voice_input_field("Acres", "ls_sz")
    l = voice_input_field(T["loc"], "ls_l")
    h = st.radio(T["house"], ["Yes", "No"])
    ph = voice_input_field(T["phone"], "ls_ph")
    if st.button(T["submit"]):
        df = load_data('lease.csv', ["owner", "size", "loc", "house", "phone"])
        save_data(pd.concat([df, pd.DataFrame([[o, sz, l, h, ph]], columns=df.columns)]), 'lease.csv')
        st.rerun()
    l_df = load_data('lease.csv', ["owner", "size", "loc", "house", "phone"])
    for _, row in l_df.iterrows():
        if search_query in str(row['loc']).lower():
            with st.expander(f"🌳 {row['size']} Acres - {row['loc']}"):
                st.write(f"House: {row['house']} | Owner: {row['owner']} | 📞 {row['phone']}")
