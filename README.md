# 🏡 Hệ Thống Dự Đoán Giá Nhà King County (Estate Valuation AI)

Đây là đồ án môn học xây dựng ứng dụng Web giúp định giá bất động sản tại King County (USA). Dự án kết hợp quy trình xử lý dữ liệu lớn (Big Data) và thuật toán **Machine Learning (Random Forest)** để đưa ra dự đoán chính xác.

---

## 🚀 Chức năng chính

Hệ thống được chia thành 2 module (Tab):

### 1. Phân tích dữ liệu (Dashboard)
- Biểu đồ phân bố giá nhà, biểu đồ nhiệt (Heatmap) tương quan đa biến.
- Phân tích sâu các yếu tố: Vị trí (Zipcode), Chất lượng xây dựng (Grade), Tính mùa vụ (Seasonality)...
- Trực quan hóa dữ liệu giúp người dùng có cái nhìn toàn cảnh về thị trường.

### 2. Dự đoán & Giải thích Cục bộ (Prediction & Local SHAP)
- Dự đoán: Nhập liệu 18 thông số chi tiết -> Trả về giá trị ước tính thời gian thực.
- Giải thích (New): Tích hợp biểu đồ thác nước (SHAP Waterfall Plot) ngay sau khi dự đoán.
   + Trả lời câu hỏi: "Tại sao căn nhà này lại có giá đó?"
   + Chỉ rõ từng yếu tố (View sông, Diện tích lớn...) đã cộng thêm hay trừ bớt bao nhiêu tiền vào giá gốc.

### 3. Phân tích Toàn cục (Global SHAP Explanation)
- Cơ chế (New): Sử dụng lý thuyết trò chơi (Game Theory) để phân tích "khẩu vị" của mô hình AI trên toàn bộ thị trường.
- Biểu đồ Summary: Xếp hạng các yếu tố quan trọng nhất (như grade, lat, sqft_living) ảnh hưởng đến giá nhà.
- Giúp người dùng hiểu được quy luật chung của thị trường bất động sản.
---

## 🛠️ Công nghệ & Kiến trúc Hệ thống

Dự án áp dụng mô hình kiến trúc **Offline Training - Online Serving** để giải quyết bài toán Big Data trên môi trường ứng dụng:

### 1. Tầng Xử lý Dữ liệu Lớn (Offline Layer) - `notebook/`
* **Công nghệ:** Apache Spark (PySpark).
* **Nhiệm vụ:**
    * Xử lý toàn bộ tập dữ liệu gốc (Full Dataset) với dung lượng lớn.
    * Làm sạch dữ liệu, xử lý ngoại lai (Outliers) và Feature Engineering phân tán.
    * Thực hiện *Hyperparameter Tuning* trên toàn bộ dữ liệu để tìm ra bộ tham số tối ưu (Best Params).

### 2. Chiến lược Chuyển đổi (Migration Strategy) - `train_model.py`
Do ứng dụng Web chạy trên môi trường giới hạn tài nguyên (không có Cluster Hadoop), nhóm áp dụng kỹ thuật **Representative Sampling (Lấy mẫu đại diện)**:
* Thay vì load 100% dữ liệu lớn vào ứng dụng (gây tràn RAM), nhóm trích xuất một mẫu đại diện (Sampled Data) đã được làm sạch bởi Spark.
* Mẫu dữ liệu này đảm bảo tính phân phối thống kê tương đương với tập dữ liệu gốc.

### 3. Tầng Ứng dụng & Triển khai (Online Layer) - `app.py`
* **Công nghệ:** Scikit-Learn (Python) & Streamlit.
* **Nhiệm vụ:** **Model Serving**.
    * Huấn luyện lại một mô hình nhẹ (Lightweight Model) trên tập mẫu, sử dụng đúng bộ tham số tối ưu mà Spark đã tìm ra.
    * **Lợi ích:** Giúp ứng dụng khởi động nhanh, chiếm ít tài nguyên bộ nhớ và phản hồi người dùng tức thì (Real-time Inference) mà vẫn giữ được độ chính xác tiệm cận với mô hình gốc trên Spark.

---

## ⚙️ Hướng dẫn Cài đặt & Chạy

**Lưu ý:** Bạn không cần huấn luyện lại mô hình vì file model đã có sẵn (`house_price_model.pkl`).

### Bước 1: Mở dự án
Tải thư mục dự án về máy và mở bằng **VS Code**.

### Bước 2: Tạo & Kích hoạt môi trường ảo
Mở Terminal tại thư mục dự án và chạy lệnh:

```bash
# Tạo venv (nếu chưa có)
python -m venv venv

# Kích hoạt (Windows)
.\venv\Scripts\activate

### Bước 3: Cài đặt thư viện
Chạy lệnh sau để cài đặt các gói cần thiết từ file requirements.txt:

```bash
pip install -r requirements.txt
```

### Bước 4: Khởi chạy Ứng dụng
Gõ lệnh sau để mở trang web:
```bash
streamlit run app.py
```
👉 Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ: http://localhost:8501

(Trong trường hợp chưa có file model, chạy lệnh python train_model.py để tạo lại)


### Cấu trúc thư mục
```Plaintext
HousePriceDemo/
├── venv/                   # Môi trường ảo Python
├── notebook/               # KHÔNG GIAN NGHIÊN CỨU (Spark/Big Data)
│   ├── DA.ipynb            # Phân tích khám phá (Data Analysis)
│   ├── DE.ipynb            # Xử lý dữ liệu với PySpark
│   └── DS.ipynb            # Huấn luyện mô hình Spark MLlib
├── modules/                  # Các trang giao diện Web App
│   ├── 1_analytics.py
│   └── 2_explain.py
│   └── 3_home.py
│   └── 4_prediction.py
├── app.py                  # Trang chủ (Homepage)
├── kc_house_data.csv       # Dữ liệu gốc
├── zipcode_coords.csv      # Dữ liệu tọa độ (Lookup table)
├── house_price_model.pkl   # Model Scikit-Learn (Optimized for Web App)
├── train_model.py          # Script đóng gói model (Model Distillation)
├── requirements.txt        # Danh sách thư viện
└── README.md               # Hướng dẫn sử dụng
```

