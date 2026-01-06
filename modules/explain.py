import streamlit as st
import shap
import matplotlib.pyplot as plt
import pandas as pd

# --- HÀM TÍNH TOÁN (Dùng Cache) ---
@st.cache_data(show_spinner=False)
def calculate_shap_values(_model, X_sample):
    explainer = shap.TreeExplainer(_model)
    shap_values = explainer.shap_values(X_sample)
    return shap_values

def show_explanation(model, df_original):
    st.title("PHÂN TÍCH TOÀN CỤC (GLOBAL SHAP)")
    st.markdown("---")

    # --- 1. LÝ THUYẾT ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("1. Phương pháp SHAP")
        st.markdown("""
        **SHAP (Shapley Additive exPlanations)** là phương pháp dựa trên Lý thuyết trò chơi, giúp giải thích mức độ đóng góp của từng biến số (feature) vào kết quả dự đoán.
        
        Hệ thống sử dụng thuật toán **TreeExplainer**, tối ưu cho mô hình Random Forest để đảm bảo tốc độ và độ chính xác cao.
        """)

    with col2:
        st.subheader("2. Cách đọc biểu đồ Summary")
        st.markdown("""
        * **Mỗi dấu chấm:** Là 1 căn nhà (1 giá trị SHAP Cục bộ).
        * **Trục tung (Y):** Thứ tự quan trọng (Trên cùng = Quan trọng nhất).
        * **Trục hoành (X):** Tác động đến giá (Phải = Tăng giá, Trái = Giảm giá).
        * **Màu sắc:** 🔴 **Đỏ** (Giá trị cao) - 🔵 **Xanh** (Giá trị thấp).
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. BIỂU ĐỒ PHÂN TÍCH ---
    st.subheader("Biểu đồ Tổng quan Thị trường")
    
    feature_cols = [
        'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
        'waterfront', 'view', 'condition', 'grade',
        'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated',
        'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15', 'sell_month'
    ]
    available_cols = [c for c in feature_cols if c in df_original.columns]
    X = df_original[available_cols]

    with st.spinner("Đang tải dữ liệu phân tích..."):
        X_sample = X.sample(100, random_state=42)
        shap_values = calculate_shap_values(model, X_sample)
        
        # --- KỸ THUẬT "NHỐT" BIỂU ĐỒ VÀO GIỮA ---
        # Vẫn dùng cột giữa để giới hạn chiều ngang cho gọn
        left_col, center_col, right_col = st.columns([1, 2, 1])
        
        with center_col:
            # 1. Tăng chiều cao lên (figsize=(6, 8)) để chứa đủ 19 dòng mà không bị díu chữ
            fig, ax = plt.subplots(figsize=(6, 8))
            
            # 2. max_display=20: Để hiển thị hết toàn bộ các đặc trưng
            shap.summary_plot(shap_values, X_sample, max_display=20, show=False)
            plt.tight_layout()
            
            # 3. Hiển thị
            st.pyplot(fig, use_container_width=True)
            
        # --- NHẬN XÉT (Đã chỉnh sửa theo đúng ảnh em gửi) ---
        st.info("""
        **💡 Nhận xét từ dữ liệu thực tế:**
        Quan sát biểu đồ, ta thấy sự phân hóa rõ rệt về mức độ ảnh hưởng:
        
        1.  **Nhóm "Quyền lực nhất" (Top 3):**
            * **`grade` (Chất lượng)**: Yếu tố số 1. Dải màu đỏ nằm hẳn về bên phải -> Chất lượng xây dựng cao là yếu tố đảm bảo tăng giá mạnh nhất.
            * **`sqft_living` (Diện tích)**: Diện tích lớn (đỏ) luôn kéo giá trị nhà đi lên.
            * **`lat` (Vĩ độ/Vị trí)**: Có dải phân bố rất rộng, cho thấy vị trí địa lý tại King County cực kỳ nhạy cảm với giá.
        
        2.  **Nhóm ít ảnh hưởng nhất:** * `yr_renovated`, `sqft_basement`, `floors` nằm ở đáy biểu đồ. Điều này cho thấy AI ít dựa vào các chỉ số này để định giá so với vị trí và diện tích.
        """)

 # --- 🔥 CẬP NHẬT: GIẢI THÍCH CƠ CHẾ CHI TIẾT & DỄ HIỂU 🔥 ---
        with st.expander("📚 Tìm hiểu chuyên sâu: Cơ chế Toán học của SHAP (Cục bộ vs Toàn cục)"):
            st.markdown("""
            ### 1. Sự khác biệt cốt lõi (So sánh nhanh)
            | Đặc điểm | SHAP Cục bộ (Local) | SHAP Toàn cục (Global) |
            | :--- | :--- | :--- |
            | **Mục tiêu** | Giải thích cho **1 căn nhà** cụ thể. | Giải thích cho **toàn bộ thị trường**. |
            | **Câu hỏi** | "Tại sao căn nhà này đắt/rẻ?" | "Yếu tố nào quan trọng nhất nói chung?" |
            | **Đầu ra** | Số tiền cộng/trừ cụ thể (VD: +$50k). | Bảng xếp hạng độ quan trọng. |
            | **Cách tính** | Dựa trên lý thuyết trò chơi. | **Trung bình cộng** các giá trị Cục bộ. |

            ---

            ### 2. Cơ chế tính toán SHAP Toàn cục (Global Importance)
            Làm sao AI biết được **`grade` (Chất lượng)** quan trọng hơn **`view` (Tầm nhìn)**? Nó dùng công thức **Trung bình Giá trị Tuyệt đối (Mean Absolute Value)**.

            #### Công thức toán học:
            Độ quan trọng ($I_j$) của yếu tố $j$ được tính trên $N$ căn nhà:

            $$I_j = \\frac{1}{N} \sum_{i=1}^{N} |\\phi_j^{(i)}|$$

            #### Giải thích ký hiệu:
            * $I_j$: Độ quan trọng toàn cục của yếu tố $j$ (Ví dụ: Độ quan trọng của `grade`).
            * $N$: Tổng số căn nhà được khảo sát (Ví dụ: 100 căn).
            * $\phi_j^{(i)}$: Giá trị SHAP cục bộ của yếu tố $j$ tại căn nhà thứ $i$.
            * $|...|$: **Giá trị tuyệt đối** (Lấy số dương, không quan tâm dấu âm/dương).

            ---

            ### 3. Ví dụ minh họa "Siêu dễ hiểu"
            Giả sử ta xét độ quan trọng của yếu tố **Chất lượng nhà (`grade`)** trên 3 căn nhà:

            * **Nhà A (Xịn):** Grade cao $\rightarrow$ Làm giá tăng **+\$100k**.
            * **Nhà B (Nát):** Grade thấp $\rightarrow$ Làm giá giảm **-\$100k**.
            * **Nhà C (Thường):** Grade bình thường $\rightarrow$ Không tăng giảm **\$0**.

            👉 **AI tính toán độ quan trọng ($I_{grade}$):**
            Nó không cộng trực tiếp ($100 - 100 + 0 = 0$ -> Sai, vì Grade rất ảnh hưởng!), mà nó lấy **giá trị tuyệt đối** (độ tác động mạnh hay nhẹ):

            $$I_{grade} = \\frac{|100| + |-100| + |0|}{3} = \\frac{100 + 100 + 0}{3} \\approx 66.7k$$

            **Kết luận:** Trung bình mỗi lần thay đổi Grade, giá nhà bị "rung lắc" khoảng **$66.7k**. Đây là con số rất lớn, nên `grade` được xếp hạng **Top 1 Quan trọng**.
            """)