import streamlit as st
import pandas as pd
import joblib

# Import các module
from modules.home import show_home
from modules.analytics import show_analytics 
from modules.prediction import show_prediction

# 1. Cấu hình trang
st.set_page_config(
    page_title="Estate Valuation AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 🔥 CSS FINAL: FIX LỖI 2 THANH MÀU, THANH CUỘN & CĂN GIỮA MENU 🔥 ---
# --- 🔥 CSS CẬP NHẬT: ÉP MENU RA GIỮA TUYỆT ĐỐI 🔥 ---
st.markdown("""
    <style>
        /* 1. Ẩn Header mặc định & Thanh cuộn thừa */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        .stApp {
            overflow-x: hidden !important;
        }
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 5rem !important;
        }

        /* 2. ẨN THANH HIGHLIGHT MẶC ĐỊNH */
        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }
        
        div[data-baseweb="tab-list"] {
            border-bottom: none !important; 
        }

        /* 3. KHUNG MENU CHÍNH: CĂN GIỮA TOÀN DIỆN */
        /* Nhắm vào lớp bao ngoài cùng của các nút tab */
        div[data-testid="stVerticalBlock"] > div:first-of-type > .stTabs > div:first-child {
            position: fixed !important;
            top: 0px !important;
            left: 0px !important;
            right: 0px !important;
            height: 80px !important;
            z-index: 999999 !important;
            background-color: white !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
            border-bottom: 1px solid #e0e0e0 !important;
            
            /* Ép toàn bộ container này ra giữa */
            display: flex !important;
            justify-content: center !important;
        }

        /* Nhắm vào danh sách các nút bên trong */
        div[data-baseweb="tab-list"] {
            display: flex !important;
            justify-content: center !important;
            width: auto !important;
            gap: 80px !important; /* Tăng khoảng cách cho thoáng */
            background-color: transparent !important;
            height: 100% !important;
            align-items: center !important;
        }

        /* 4. Đẩy nội dung xuống */
        div[data-testid="stVerticalBlock"] > div:first-of-type > .stTabs {
            padding-top: 6rem !important;
        }
        
        /* 5. STYLE CHỮ MENU */
        div[data-baseweb="tab-list"] button {
            font-size: 24px !important; 
            font-weight: 900 !important; 
            color: #2c3e50 !important;
            background-color: transparent !important;
            border: none !important;
            padding: 10px 20px !important;
            min-width: 150px !important; /* Giúp các nút đều nhau */
        }
        
        div[data-baseweb="tab-list"] button:hover {
            color: #2575fc !important;
        }

        div[data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #6a11cb !important;
            border-bottom: 5px solid #6a11cb !important;
        }
        
        /* Chặn menu con không bị ảnh hưởng bởi căn giữa của menu chính */
        .stTabs .stTabs div[data-baseweb="tab-list"] {
            position: static !important;
            justify-content: flex-start !important;
            gap: 10px !important;
            box-shadow: none !important;
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Load Data & Model
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('kc_house_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        return df
    except: return None

@st.cache_resource
def load_resources():
    try:
        model = joblib.load('house_price_model.pkl')
        zip_map = pd.read_csv('zipcode_coords.csv')
        return model, zip_map
    except: return None, None

df = load_data()
model, zip_map = load_resources()

# 3. MENU ĐIỀU HƯỚNG
tab1, tab2, tab3 = st.tabs([
    "TRANG CHỦ", 
    "PHÂN TÍCH", 
    "DỰ ĐOÁN"
])

# --- TAB 1 ---
with tab1:
    show_home()

# --- TAB 2 ---
with tab2:
    if df is not None:
        show_analytics(df)
    else:
        st.error("⚠️ Chưa có dữ liệu kc_house_data.csv")

# --- TAB 3 ---
with tab3:
    if model is not None and zip_map is not None:
        show_prediction(model, zip_map)
    else:
        st.error("⚠️ Thiếu file Model hoặc Zipcode. Hãy chạy 'train_model.py' trước.")