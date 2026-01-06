import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt

def show_prediction(model, zip_map):
    # --- CSS GIỮ NGUYÊN NHƯ CŨ ---
    st.markdown("""
        <style>
            .main-title { font-size: 2.8rem !important; font-weight: 800 !important; color: #5e17eb; text-align: center; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
            .header-blue { font-size: 1.2rem !important; font-weight: 700 !important; color: #0984e3 !important; border-bottom: 2px solid #0984e3; padding-bottom: 8px; margin-bottom: 15px; display: flex; align-items: center; }
            .badge-blue { background-color: #0984e3; color: white; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px; font-size: 0.9rem; }
            .header-purple { font-size: 1.2rem !important; font-weight: 700 !important; color: #6c5ce7 !important; border-bottom: 2px solid #6c5ce7; padding-bottom: 8px; margin-bottom: 15px; display: flex; align-items: center; }
            .badge-purple { background-color: #6c5ce7; color: white; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px; font-size: 0.9rem; }
            .header-teal { font-size: 1.2rem !important; font-weight: 700 !important; color: #00b894 !important; border-bottom: 2px solid #00b894; padding-bottom: 8px; margin-bottom: 15px; display: flex; align-items: center; }
            .badge-teal { background-color: #00b894; color: white; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px; font-size: 0.9rem; }
            button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #0984e3 0%, #8e44ad 100%) !important; color: white !important; font-size: 20px !important; font-weight: 800 !important; padding: 0.8rem 3rem !important; border: none !important; border-radius: 50px !important; width: 100% !important; box-shadow: 0 4px 15px rgba(142, 68, 173, 0.4) !important; transition: all 0.3s ease !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
            button[data-testid="baseButton-primary"]:hover { transform: translateY(-3px) !important; box-shadow: 0 8px 25px rgba(142, 68, 173, 0.6) !important; filter: brightness(1.1) !important; }
            .compact-result-box { background-color: white; border-radius: 15px; padding: 25px; width: 350px; margin: 25px auto 0 auto; text-align: center; border-left: 6px solid #6c5ce7; box-shadow: 0 10px 30px rgba(0,0,0,0.1); animation: slideUp 0.5s ease-out; }
            @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            .compact-label { font-size: 0.9rem; color: #636e72; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; font-weight: 700; }
            .compact-value { font-size: 2.8rem; color: #2d3436; font-weight: 800; font-family: 'Segoe UI', sans-serif; margin: 0; line-height: 1.2; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">🤖 Dự đoán Giá nhà AI</h1>', unsafe_allow_html=True)

    with st.form(key='prediction_form', clear_on_submit=False):
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown('<div class="header-blue"><span class="badge-blue">1</span> Vị trí & Đất đai</div>', unsafe_allow_html=True)
            list_zip = sorted(zip_map['zipcode'].unique())
            selected_zip = st.selectbox("Mã Bưu Chính (Zipcode)", list_zip)
            sqft_living = st.number_input("Diện tích nhà (sqft)", value=1800, step=10)
            sqft_lot = st.number_input("Diện tích đất (sqft)", value=5000, step=10)

        with col2:
            st.markdown('<div class="header-purple"><span class="badge-purple">2</span> Tiện nghi & View</div>', unsafe_allow_html=True)
            bedrooms = st.number_input("Số phòng ngủ", value=3)
            bathrooms = st.number_input("Số phòng tắm", value=2.0, step=0.25)
            floors = st.number_input("Số tầng", value=1.0, step=0.5)
            waterfront = st.selectbox("Mặt tiền sông/hồ?", ["Không", "Có"])
            view = st.slider("Mức độ View (0-4)", 0, 4, 0)
            condition = st.slider("Tình trạng nhà (1-5)", 1, 5, 3)

        with col3:
            st.markdown('<div class="header-teal"><span class="badge-teal">3</span> Cấu trúc & Năm xây</div>', unsafe_allow_html=True)
            grade = st.slider("Chất lượng (Grade 1-13)", 1, 13, 7)
            sqft_above = st.number_input("Diện tích sàn trên (sqft)", value=1500)
            sqft_basement = st.number_input("Diện tích tầng hầm (sqft)", value=0)
            yr_built = st.number_input("Năm xây dựng", value=1995)
            yr_renovated = st.number_input("Năm sửa chữa", value=0)
            sell_month = st.selectbox("Tháng giao dịch", range(1, 13), index=5)

        st.write("")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            submit_btn = st.form_submit_button(" ĐỊNH GIÁ NGAY", type="primary", use_container_width=True)

    if submit_btn:
        row = zip_map[zip_map['zipcode'] == selected_zip].iloc[0]
        lat, long = row['center_lat'], row['center_long']
        waterfront_val = 1 if waterfront == "Có" else 0
        sqft_living15, sqft_lot15 = sqft_living, sqft_lot

        input_data = pd.DataFrame({
            'bedrooms': [bedrooms], 'bathrooms': [bathrooms], 'sqft_living': [sqft_living], 
            'sqft_lot': [sqft_lot], 'floors': [floors], 'waterfront': [waterfront_val], 
            'view': [view], 'condition': [condition], 'grade': [grade],
            'sqft_above': [sqft_above], 'sqft_basement': [sqft_basement], 
            'yr_built': [yr_built], 'yr_renovated': [yr_renovated],
            'lat': [lat], 'long': [long], 'sqft_living15': [sqft_living15], 
            'sqft_lot15': [sqft_lot15], 'sell_month': [sell_month]
        })
        
        try:
            pred = model.predict(input_data)[0]
            
            st.markdown(f"""
            <div class="compact-result-box">
                <div class="compact-label">Giá trị ước tính</div>
                <div class="compact-value">${pred:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.write("")
            st.markdown("---")
            st.subheader("🔍 Tại sao AI đưa ra mức giá này?")
            
            with st.spinner("Đang phân tích các yếu tố tăng/giảm giá..."):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer(input_data)
                
                # Vẽ biểu đồ (Thu nhỏ và hiện 10 dòng)
                fig, ax = plt.subplots(figsize=(6, 4))
                shap.plots.waterfall(shap_values[0], max_display=10, show=False)
                
                col_chart_1, col_chart_2, col_chart_3 = st.columns([1, 6, 1])
                with col_chart_2:
                    st.pyplot(fig)
                
                base_val = shap_values[0].base_values
                st.info(f"""
                **Cách đọc biểu đồ:**
                - Giá trung bình thị trường (E[f(x)]): **${base_val:,.0f}**.
                - Thanh **ĐỎ**: Các yếu tố kéo giá nhà **TĂNG LÊN**.
                - Thanh **XANH**: Các yếu tố kéo giá nhà **GIẢM XUỐNG**.
                """)

                # --- 🔥 PHẦN MỚI: GIẢI THÍCH CƠ CHẾ SHAP CỤC BỘ 🔥 ---
                with st.expander("📚 Tìm hiểu: Cơ chế tính toán của SHAP Cục bộ (Local Interpretation)"):
                    st.markdown("""
                    ### 1. Nguyên lý Trò chơi (Game Theory)
                    SHAP coi việc dự đoán giá nhà như một **trò chơi đồng đội**, trong đó mỗi "người chơi" là một đặc trưng (Diện tích, Vị trí, Số phòng...).
                    Mục tiêu là chia thưởng (hoặc phạt) công bằng cho từng người chơi dựa trên đóng góp của họ vào kết quả cuối cùng (Giá nhà).

                    ### 2. Công thức Phân rã (Decomposition)
                    Giá trị dự đoán cho căn nhà này $f(x)$ được phân rã thành:
                    
                    $$f(x) = E[f(x)] + \sum_{i=1}^{M} \phi_i$$

                    Trong đó:
                    * $f(x)$: Giá dự đoán cuối cùng (Ví dụ: $260k).
                    * $E[f(x)]$: Giá trị trung bình cơ sở (Base Value) của toàn thị trường (Ví dụ: $541k).
                    * $\phi_i$: Giá trị SHAP (Shapley Value) của đặc trưng thứ $i$. Đây chính là chiều dài các thanh màu Đỏ/Xanh trên biểu đồ.

                    ### 3. Cơ chế "Thử - Sai" (Counterfactual Analysis)
                    Để tính được $\phi_i$ (ví dụ: tác động của *View sông*), thuật toán thực hiện hàng loạt giả định:
                    * **Bước 1:** Giả sử không biết thông tin về View sông -> AI dự đoán giá là bao nhiêu?
                    * **Bước 2:** Cung cấp thông tin "Có View sông" -> AI dự đoán giá mới là bao nhiêu?
                    * **Bước 3:** Sự chênh lệch giữa hai lần dự đoán chính là đóng góp của yếu tố View sông.
                    """)
            
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")