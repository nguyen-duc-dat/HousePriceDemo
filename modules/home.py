# File: modules/home.py
import streamlit as st

def show_home():
    # ------------------------------------------------------------------------
    # 1. KHAI BÁO CÁC BIẾN HTML/CSS (ĐỂ SÁT LỀ TRÁI ĐỂ TRÁNH LỖI HIỂN THỊ)
    # ------------------------------------------------------------------------
    
    # CSS STYLE
    custom_css = """
    <style>
        /* Tiêu đề Gradient */
        .hero-title {
            background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            font-weight: 800 !important;
            text-align: center;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .hero-subtitle {
            text-align: center; font-size: 1.1rem; color: #57606f; margin-bottom: 30px;
        }

        /* WORKFLOW BOX */
        .workflow-box {
            background-color: white;
            border-radius: 15px;
            padding: 30px 10px;
            margin-bottom: 40px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid #f0f2f6;
        }
        .step-container {
            display: flex; justify-content: center; align-items: flex-start; flex-wrap: wrap; gap: 10px;
        }
        .step-item {
            flex: 1; min-width: 120px; text-align: center; position: relative;
        }
        .step-icon-circle {
            width: 60px; height: 60px;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white; border-radius: 50%;
            display: inline-flex; align-items: center; justify-content: center;
            font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;
            box-shadow: 0 5px 15px rgba(37, 117, 252, 0.3);
            transition: transform 0.3s;
        }
        .step-item:hover .step-icon-circle { transform: scale(1.1); }
        .step-title { font-weight: 700; color: #2d3436; font-size: 1rem; margin-bottom: 5px; }
        .step-desc { font-size: 0.8rem; color: #636e72; line-height: 1.3; padding: 0 5px; }
        .arrow-next { font-size: 1.5rem; color: #b2bec3; margin-top: 15px; font-weight: 900; }

        /* CARDS */
        .feature-card {
            background-color: #f8f9fa; border-radius: 12px; padding: 25px; height: 100%;
            border: 1px solid #dee2e6; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            background-color: white; border-color: #2575fc;
        }
        .card-icon { font-size: 2.5rem; margin-bottom: 10px; text-align: center; }
        .card-title-blue { color: #2575fc; font-size: 1.3rem; font-weight: 700; text-align: center; margin-bottom: 10px;}
        .card-title-purple { color: #6a11cb; font-size: 1.3rem; font-weight: 700; text-align: center; margin-bottom: 10px;}
        .card-text { color: #2d3436; font-size: 0.95rem; font-weight: 500; line-height: 1.5; text-align: justify; }
        .cta-box { display: block; padding: 8px; border-radius: 6px; text-align: center; font-weight: 700; font-size: 0.9rem; margin-top: 15px; }
        .cta-blue { background-color: #e3f2fd; color: #1565c0; }
        .cta-purple { background-color: #f3e5f5; color: #7b1fa2; }
    </style>
    """

    # HTML CHO WORKFLOW (QUAN TRỌNG: KHÔNG THỤT ĐẦU DÒNG)
    workflow_html = """
<div class="workflow-box">
    <div style="text-align:left; margin-bottom:20px; font-weight:700; color:#b2bec3; text-transform:uppercase; letter-spacing:1px; font-size:0.8rem;">
        ⚙️ Kiến trúc hệ thống (Data Pipeline)
    </div>
    <div class="step-container">
        <div class="step-item">
            <div class="step-icon-circle">📂</div>
            <div class="step-title">Thu thập</div>
            <div class="step-desc">Raw Data từ nguồn dữ liệu gốc.</div>
        </div>
        <div class="arrow-next">➜</div>
        <div class="step-item">
            <div class="step-icon-circle">🐘</div>
            <div class="step-title">Hadoop & Spark</div>
            <div class="step-desc">Lưu trữ lớn & Xử lý phân tán.</div>
        </div>
        <div class="arrow-next">➜</div>
        <div class="step-item">
            <div class="step-icon-circle">🔎</div>
            <div class="step-title">EDA & Clean</div>
            <div class="step-desc">Làm sạch & Khám phá dữ liệu.</div>
        </div>
        <div class="arrow-next">➜</div>
        <div class="step-item">
            <div class="step-icon-circle">🧠</div>
            <div class="step-title">Huấn luyện AI</div>
            <div class="step-desc">Phân tích EDA & Train Model.</div>
        </div>
        <div class="arrow-next">➜</div>
        <div class="step-item">
            <div class="step-icon-circle">💻</div>
            <div class="step-title">Web App</div>
            <div class="step-desc">Triển khai ứng dụng Streamlit.</div>
        </div>
    </div>
</div>
"""

    # HTML CHO CARD PHÂN TÍCH
    card_analytics_html = """
<div class="feature-card">
    <div class="card-icon">📊</div>
    <div class="card-title-blue">Phân tích Dữ liệu</div>
    <div class="card-text">
        Hiểu rõ thị trường thông qua các biểu đồ trực quan:
        <ul style="margin-bottom:0; padding-left: 20px;">
            <li><b>Xu hướng:</b> Biến động giá theo thời gian.</li>
            <li><b>Vị trí:</b> Bản đồ nhiệt (Heatmap) khu vực đắt đỏ.</li>
            <li><b>Tương quan:</b> Yếu tố nào ảnh hưởng giá nhất?</li>
        </ul>
    </div>
    <div class="cta-box cta-blue">👉 Vào Tab "Phân tích"</div>
</div>
"""

    # HTML CHO CARD DỰ ĐOÁN
    card_prediction_html = """
<div class="feature-card">
    <div class="card-icon">🤖</div>
    <div class="card-title-purple">Dự đoán AI</div>
    <div class="card-text">
        Định giá căn nhà tự động dựa trên mô hình máy học:
        <ul style="margin-bottom:0; padding-left: 20px;">
            <li><b>Công nghệ:</b> Random Forest Regressor tối ưu.</li>
            <li><b>Đầu vào:</b> Xử lý 18 thông số chi tiết.</li>
            <li><b>Tốc độ:</b> Trả kết quả định giá ngay lập tức.</li>
        </ul>
    </div>
    <div class="cta-box cta-purple">👉 Vào Tab "Dự đoán"</div>
</div>
"""

    # ------------------------------------------------------------------------
    # 2. HIỂN THỊ GIAO DIỆN (RENDER)
    # ------------------------------------------------------------------------
    
    # Render CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Render Hero Title
    st.markdown('<h1 class="hero-title">Estate Valuation AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Hệ thống Phân tích & Định giá Bất động sản King County</p>', unsafe_allow_html=True)

    # Render Workflow
    st.markdown(workflow_html, unsafe_allow_html=True)

    # Render Cards
    c_space1, col1, col2, c_space2 = st.columns([0.5, 4, 4, 0.5], gap="large")
    
    with col1:
        st.markdown(card_analytics_html, unsafe_allow_html=True)
        
    with col2:
        st.markdown(card_prediction_html, unsafe_allow_html=True)