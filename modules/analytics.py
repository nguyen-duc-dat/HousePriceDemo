# File: pages/1_📊_Phan_tich_Du_lieu.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# File: modules/analytics.py
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def show_analytics(df):
    st.subheader("📊 Phân tích Dữ liệu (EDA)")

    if df is None:
        st.error("Dữ liệu rỗng!")
        return

    # --- Phần 1: Biểu đồ giá (Giữ nguyên) ---
    with st.container(border=True):
        st.write("### 1. Phân bố Giá nhà")
        col_dist1, col_dist2 = st.columns([3, 1])
        with col_dist1:
            fig, ax = plt.subplots(figsize=(10, 3))
            sns.histplot(df['price'], bins=50, kde=True, color='#2ecc71', ax=ax)
            ax.set_xlim(0, 3000000)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000000:.1f}M'))
            st.pyplot(fig)
        with col_dist2:
            st.markdown(f"""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
                <p>Giá TB: <b>${df['price'].mean():,.0f}</b></p>
                <p>Giá Max: <b>${df['price'].max():,.0f}</b></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.write("")

    # --- SỬA ĐOẠN NÀY: Thay st.tabs thành st.radio ---
    st.write("### 3. Phân tích Chi tiết")
    
    # Tạo menu con dạng nút bấm ngang (Radio Button Horizontal)
    # Cách này KHÔNG bị dính CSS của Menu chính -> Không bị lỗi đè lên nhau
    sub_tab = st.radio(
        "Chọn góc nhìn phân tích:",
        ["Chất lượng & View", "Cấu trúc nhà", "Phòng ngủ"],
        horizontal=True,
        label_visibility="collapsed" # Ẩn nhãn đi cho đẹp
    )

    st.write("") # Khoảng cách nhỏ

    # Dùng if/else để hiển thị nội dung tương ứng
    if sub_tab == "Chất lượng & View":
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            st.markdown("**Theo Xếp hạng (Grade)**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.barplot(data=df, x='grade', y='price', palette="viridis", errorbar=None, ax=ax1)
            ax1.set_ylabel("Giá TB (USD)")
            ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            st.pyplot(fig1)
        with col_q2:
            st.markdown("**Theo Mức độ View**")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.barplot(data=df, x='view', y='price', palette="magma", errorbar=None, ax=ax2)
            ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            st.pyplot(fig2)
        st.caption("📝 **Nhận xét:** Grade càng cao, giá càng tăng mạnh.")

    elif sub_tab == "Cấu trúc nhà":
        col_q3, col_q4 = st.columns(2)
        with col_q3:
            st.markdown("**Mặt tiền Sông/Hồ**")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            sns.barplot(data=df, x='waterfront', y='price', palette="coolwarm", errorbar=None, ax=ax3)
            ax3.set_xticklabels(['Không', 'Có'])
            ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            st.pyplot(fig3)
        with col_q4:
            st.markdown("**Tình trạng nhà (Condition)**")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            sns.barplot(data=df, x='condition', y='price', palette="Blues", errorbar=None, ax=ax4)
            ax4.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            st.pyplot(fig4)

    elif sub_tab == "Phòng ngủ":
        st.markdown("**Theo Số lượng Phòng ngủ**")
        fig5, ax5 = plt.subplots(figsize=(10, 4))
        sns.barplot(data=df[df['bedrooms'] <= 9], x='bedrooms', y='price', palette="Set2", errorbar=None, ax=ax5)
        ax5.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
        st.pyplot(fig5)
        st.caption("📝 **Nhận xét:** Giá đạt đỉnh ở mức 8 phòng ngủ.")

    st.write("")
    
    # --- Phần 4: Vị trí (Giữ nguyên) ---
    with st.container(border=True):
         st.write("### 4. Yếu tố Vị trí & Thời gian")
         # ... (Code cũ của bạn) ...
# 1. Cấu hình trang
# st.set_page_config(page_title="Phân tích dữ liệu", page_icon="📊", layout="wide")
def show_analytics(df):
    st.subheader("📊 Dashboard Phân tích Thị trường")

    # 2. Load dữ liệu
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv('kc_house_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            return df
        except:
            return None

    df = load_data()

    if df is None:
        st.error("⚠️ Không tìm thấy file 'kc_house_data.csv'.")
        st.stop()

    # ==============================================================================
    # PHẦN 1: TỔNG QUAN PHÂN BỐ GIÁ
    # ==============================================================================
    with st.container(border=True):
        st.subheader("1. Phân bố Giá nhà (Price Distribution)")
        
        col_dist1, col_dist2 = st.columns([3, 1])
        
        with col_dist1:
            fig, ax = plt.subplots(figsize=(10, 3))
            sns.histplot(df['price'], bins=50, kde=True, color='#2ecc71', ax=ax)
            ax.set_xlabel("Giá nhà (USD)")
            ax.set_xlim(0, 3000000) 
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000000:.1f}M'))
            st.pyplot(fig)
            
        with col_dist2:
            # Thống kê
            st.markdown("""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; border: 1px solid #dee2e6;">
                <p style="margin: 0; font-size: 13px; color: #666;">Giá trung bình (Mean)</p>
                <p style="margin: 0; font-size: 18px; font-weight: bold; color: #2d3436;">${:,.0f}</p>
                <br>
                <p style="margin: 0; font-size: 13px; color: #666;">Giá cao nhất (Max)</p>
                <p style="margin: 0; font-size: 18px; font-weight: bold; color: #d63031;">${:,.0f}</p>
                <br>
                <p style="margin: 0; font-size: 13px; color: #666;">Giá thấp nhất (Min)</p>
                <p style="margin: 0; font-size: 18px; font-weight: bold; color: #00b894;">${:,.0f}</p>
            </div>
            """.format(df['price'].mean(), df['price'].max(), df['price'].min()), unsafe_allow_html=True)

        # NHẬN XÉT 1
        st.info("""
        💡 **Nhận xét từ dữ liệu:**
        Biểu đồ cho thấy phân phối giá bị **lệch phải (Right-skewed)**. 
        - Đa số các căn nhà tại King County tập trung ở phân khúc **300k - 600k USD**.
        - Các bất động sản cao cấp (> 2 triệu USD) chiếm tỷ lệ nhỏ nhưng kéo giá trung bình lên cao hơn so với giá trung vị.
        """)

    st.write("")

    # ==============================================================================
    # PHẦN 2: CÁC BIẾN ĐỊNH LƯỢNG
    # ==============================================================================
    with st.container(border=True):
        st.subheader("2. Tương quan các biến Định lượng")
        col_quan1, col_quan2 = st.columns([1, 1])

        with col_quan1:
            st.markdown("**Heatmap (Hệ số tương quan Pearson)**")
            quant_cols = ['price', 'sqft_living', 'sqft_lot', 'sqft_above', 'sqft_basement', 'yr_built', 'sqft_living15']
            fig_corr, ax_corr = plt.subplots(figsize=(6, 5))
            sns.heatmap(df[quant_cols].corr(), annot=True, cmap='Blues', fmt=".2f", ax=ax_corr)
            st.pyplot(fig_corr)

        with col_quan2:
            st.markdown("**Scatter Plot: Giá vs Diện tích**")
            fig_scat, ax_scat = plt.subplots(figsize=(6, 5))
            sns.scatterplot(data=df, x='sqft_living', y='price', alpha=0.5, color='#3498db', ax=ax_scat)
            sns.regplot(data=df, x='sqft_living', y='price', scatter=False, color='red', ax=ax_scat)
            ax_scat.set_ylabel("Giá (USD)")
            ax_scat.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            st.pyplot(fig_scat)

        # NHẬN XÉT 2
        st.info("""
        💡 **Phân tích Tương quan:**
        - **Diện tích nhà (`sqft_living`)** có tương quan mạnh nhất với giá bán (**0.70**). Đây là yếu tố dự báo quan trọng nhất trong mô hình.
        - Ngược lại, **Diện tích đất (`sqft_lot`)** có hệ số tương quan rất thấp (**0.09**). Điều này cho thấy đất rộng ở vùng xa trung tâm không đắt bằng đất hẹp ở trung tâm.
        """)

    st.write("")

    # ==============================================================================
    # PHẦN 3: CÁC BIẾN ĐỊNH TÍNH
    # ==============================================================================
    with st.container(border=True):
        st.subheader("3. Phân tích các yếu tố Phân loại")
        
        tab_qual1, tab_qual2, tab_qual3 = st.tabs(["Chất lượng & View", "Cấu trúc nhà", "Phòng ngủ"])

        # TAB 1: GRADE & VIEW
        with tab_qual1:
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.markdown("**Theo Xếp hạng (Grade)**")
                fig1, ax1 = plt.subplots(figsize=(6, 4))
                sns.barplot(data=df, x='grade', y='price', palette="viridis", errorbar=None, ax=ax1)
                ax1.set_ylabel("Giá TB (USD)")
                ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
                st.pyplot(fig1)
            with col_q2:
                st.markdown("**Theo Mức độ View**")
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                sns.barplot(data=df, x='view', y='price', palette="magma", errorbar=None, ax=ax2)
                ax2.set_ylabel("Giá TB (USD)")
                ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
                st.pyplot(fig2)
            
            st.caption("📝 **Nhận xét:** Chất lượng xây dựng (`Grade`) có tác động theo hàm mũ. Từ Grade 10 trở lên, giá nhà tăng vọt đột biến.")

        # TAB 2: WATERFRONT & CONDITION
        with tab_qual2:
            col_q3, col_q4 = st.columns(2)
            with col_q3:
                st.markdown("**Mặt tiền Sông/Hồ**")
                fig3, ax3 = plt.subplots(figsize=(6, 4))
                sns.barplot(data=df, x='waterfront', y='price', palette="coolwarm", errorbar=None, ax=ax3)
                ax3.set_xticklabels(['Không', 'Có'])
                ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
                st.pyplot(fig3)
            with col_q4:
                st.markdown("**Tình trạng nhà (Condition)**")
                fig4, ax4 = plt.subplots(figsize=(6, 4))
                sns.barplot(data=df, x='condition', y='price', palette="Blues", errorbar=None, ax=ax4)
                ax4.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
                st.pyplot(fig4)
            
            st.caption("📝 **Nhận xét:** Nhà có mặt tiền sông/hồ (`Waterfront=1`) có giá trung bình gấp 3 lần nhà thường. Trong khi đó, Tình trạng nội thất (`Condition`) ảnh hưởng ít hơn.")

        # TAB 3: BEDROOMS
        with tab_qual3:
            st.markdown("**Theo Số lượng Phòng ngủ**")
            fig5, ax5 = plt.subplots(figsize=(10, 4))
            sns.barplot(data=df[df['bedrooms'] <= 9], x='bedrooms', y='price', palette="Set2", errorbar=None, ax=ax5)
            ax5.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            st.pyplot(fig5)
            st.caption("📝 **Nhận xét:** Giá nhà tăng dần theo số phòng ngủ và đạt đỉnh ở mức 8 phòng. Tuy nhiên, quá nhiều phòng ngủ (>9) không đồng nghĩa với giá cao nhất (có thể là nhà trọ hoặc ký túc xá).")

    st.write("")

    # ==============================================================================
    # PHẦN 4: VỊ TRÍ & THỜI GIAN
    # ==============================================================================
    with st.container(border=True):
        st.subheader("4. Yếu tố Vị trí & Thời gian")
        
        col_loc, col_time = st.columns([1, 1])
        
        with col_loc:
            st.markdown("**Top 10 Zipcode đắt đỏ nhất**")
            top_zips = df.groupby('zipcode')['price'].mean().sort_values(ascending=False).head(10)
            fig_zip, ax_zip = plt.subplots(figsize=(6, 4))
            sns.barplot(x=top_zips.values, y=top_zips.index.astype(str), palette="rocket", ax=ax_zip)
            ax_zip.set_xlabel("Giá trung bình")
            ax_zip.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000000:.1f}M'))
            st.pyplot(fig_zip)

        with col_time:
            st.markdown("**Biến động giá theo Tháng**")
            month_price = df.groupby('month')['price'].mean()
            fig_time, ax_time = plt.subplots(figsize=(6, 4))
            sns.lineplot(x=month_price.index, y=month_price.values, marker="o", color="#e74c3c", linewidth=2, ax=ax_time)
            ax_time.set_xticks(range(1, 13))
            ax_time.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))
            ax_time.grid(True, linestyle='--')
            st.pyplot(fig_time)

        # NHẬN XÉT 4
        st.info("""
        💡 **Kết luận về Vị trí & Thời gian:**
        - **Vị trí (Location):** Khu vực **Medina (Zip 98039)** và vùng ven hồ Washington có giá vượt trội so với phần còn lại.
        - **Tính mùa vụ (Seasonality):** Giá nhà có xu hướng **tăng cao vào Mùa Xuân (tháng 4, 5, 6)** do nhu cầu mua bán sôi động và thời tiết đẹp. Giá thấp nhất rơi vào mùa đông (tháng 1, 2).
        """)

# ==============================================================================
    # PHẦN 5: BẢN ĐỒ NHIỆT VỊ TRÍ & TỔNG KẾT (BỔ SUNG MỚI)
    # ==============================================================================
        
    with st.container(border=True):
        col_map, col_note = st.columns([1.5, 1])
        
        with col_map:
            st.subheader("**5. Bản đồ nhiệt: Phân bố giá theo tọa độ**")
            # Tạo biểu đồ Heatmap mô phỏng phân bố địa lý
            fig_map, ax_map = plt.subplots(figsize=(6, 5))
            
            # Sử dụng scatterplot với dải màu Spectral để thể hiện mật độ giá
            # Đỏ (giá cao) tập trung ở phía Bắc, Xanh (giá thấp) ở phía Nam
            scatter = ax_map.scatter(df['long'], df['lat'], c=df['price'], 
                                   cmap='Spectral_r', alpha=0.5, s=2,
                                   norm=plt.Normalize(df['price'].min(), 1500000)) 
            
            ax_map.set_xlabel("Kinh độ (Longitude)")
            ax_map.set_ylabel("Vĩ độ (Latitude)")
            plt.colorbar(scatter, ax=ax_map, label='Mức giá ($)', format='${x:,.0f}')
            
            # Thêm đường phân cách vùng Bắc - Nam mô phỏng
            ax_map.axhline(y=47.5, color='black', linestyle='--', alpha=0.3)
            ax_map.text(df['long'].min(), 47.52, "Khu vực Phía Bắc (Đắt đỏ)", color='red', fontsize=9, fontweight='bold')
            ax_map.text(df['long'].min(), 47.45, "Khu vực Phía Nam (Giá rẻ)", color='blue', fontsize=9, fontweight='bold')
            
            st.pyplot(fig_map)

        with col_note:
            st.markdown("**📝 Nhận xét tổng kết thị trường**")
            # Sử dụng hộp success để làm nổi bật nhận xét cuối cùng
            st.success("""
            **1. Xu hướng địa lý:** Dữ liệu cho thấy sự phân hóa cực kỳ rõ rệt giữa hai miền Bắc - Nam. Các khu vực phía Bắc (vĩ độ > 47.5) sở hữu mức giá đắt đỏ hơn do gần các trung tâm công nghệ và hồ lớn.
            """)

    st.write("") # Khoảng cách cuối trang