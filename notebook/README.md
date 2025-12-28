# 📓 Tài liệu Phân tích & Huấn luyện Mô hình (Research Notebooks)

Thư mục này chứa các mã nguồn (Source Code) phục vụ cho quá trình nghiên cứu, xử lý dữ liệu lớn và huấn luyện mô hình học máy.

## 📂 Danh sách các file

1.  **`DA.ipynb` (Data Analysis):**
    * Phân tích khám phá dữ liệu (EDA).
    * Vẽ biểu đồ phân bố, tương quan (sử dụng Matplotlib/Seaborn).
    * *Môi trường chạy:* Jupyter Notebook / Google Colab.

2.  **`DE.ipynb` (Data Engineering):**
    * **Công nghệ:** Apache Spark (PySpark).
    * **Nhiệm vụ:** Đọc dữ liệu từ HDFS, làm sạch, lọc nhiễu và Feature Engineering.
    * *Lưu ý:* Code được cấu hình để chạy trên `SparkSession` (có thể chạy Local hoặc Cluster).

3.  **`DS.ipynb` (Data Science / Modeling):**
    * **Công nghệ:** Spark MLlib.
    * **Nhiệm vụ:** Huấn luyện mô hình Random Forest trên tập dữ liệu lớn.
    * **Kết quả:** Xuất ra tham số tối ưu (Hyperparameters) để đóng gói sang môi trường Production.

---

## ⚠️ Lưu ý về Môi trường Thực thi (Environment)

Do giới hạn về tài nguyên phần cứng khi nộp đồ án (không thể gửi kèm cả cụm Cluster Hadoop), các file notebook trong thư mục này đã được tinh chỉnh để có thể **chạy được ở chế độ Local (Standalone)** hoặc **Google Colab** nhằm mục đích Demo cho giảng viên.

### Sự khác biệt giữa Demo và Thực tế:

| Đặc điểm | Môi trường Demo (Tại đây) | Môi trường Thực tế (Hadoop Cluster) |
| :--- | :--- | :--- |
| **Dữ liệu input** | File CSV cục bộ (`../kc_house_data.csv`) | HDFS Path (`hdfs://namenode:9000/data/...`) |
| **Engine** | Spark Local Mode / Pandas | Spark YARN Cluster Mode |
| **Mục đích** | Kiểm thử logic code, Demo luồng xử lý | Xử lý song song phân tán (Distributed Processing) |

### Hướng dẫn chạy (trên Local)
Để chạy các file này, bạn cần cài đặt thư viện `pyspark`:

```bash
pip install pyspark pandas seaborn matplotlib