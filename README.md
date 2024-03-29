# **Pair Trading Upgrade: Data Preprocessing and Pairs Formation**

## **Giới thiệu project**
- Project này sử dụng dữ liệu giá cổ phiếu của các công ty niêm yết trên các sàn chứng khoán tại Việt Nam, phân tích, và xác định các cặp cổ phiếu có tính chất đồng liên kết, nhằm phục vụ cho chiến lược giao dịch theo cặp.
- Tác giả: Nguyễn Trần Minh Nhựt (đồng thời chủ sở hữu của repo này dưới tên gọi nhut-ntm)
- Email: nhutntmuel@gmail.com

## **Tổ chức của REPO**

### **I. Data**
1. Folder `data` chứa file raw data, data tạm (data sinh ra trong quá trình tiền xử lý), và data đã xử lý (được dùng cho các bước tiếp theo)
2. Folder `data/processed` chứa các data đã được tiền xử lý 
    - Folder này gồm các folder con chứa data theo từng lĩnh vực: Finance, Tech, và Consumer Good
    - Mỗi folder con của từng lĩnh vực chứa 3 file data đã được xử lý được đặt theo 3 khung thời gian - Cú pháp đặt tên là: `df_{tên_lĩnh_vực}_processed_{thứ_tự_khung_thời_gian}_period_{ngày_sinh_ra_data}.csv`
3. Folder `data/interim` chứa data tạm, được sinh ra trong quá trình tiền xử lý dữ liệu 
    - Các file chứa mã `selected`: là các file data đã được lọc ra top 10 cổ phiếu có giá trị trung bình Volume cao nhất
    - Các file chứa mã `filled`: là các file data đã được điền khuyết dữ liệu rỗng
    - Các file chứa mã `pivoted`: là các file data đã được đưa về format với giá của mỗi cổ phiếu ở dạng cột
4. Folder `data/raw`: chứa file data gốc

### **II. Notebooks**
1. Folder `notebooks` chứa các Jupyter Notebook cho quá trình tiền xử lý dữ liệu và chọn cặp 
2. Folder `notebooks/archived` (chứa các notebook cũ không dùng) và `notebooks/colab_notebooks` (notebook chạy trên Google Colab)
    - CÓ THỂ BỎ QUA 
3. Folder `notebooks/main_notebooks`chứa các notebook chính dùng để chạy quá trình tiền xử lý và chọn cặp 
    - Folder `notebooks/main_notebooks/data_preprocessing/data_preprocessing` chứa notebook tiền xử lý dữ liệu 
        - File `1_data_preprocessing_raw_stock_selection.ipynb` là file Jupyter Notebook dùng để tiền xử lý dữ liệu cho ba ngành bao gồm có các bước chính là: chia thời gian cổ phiếu của mỗi ngành theo ba khung, điền khuyết dữ liệu, và pivot dữ liệu 
    - Folder `notebooks/main_notebooks/pairs_formation` chứa các notebooks để tìm cặp 
        - Folder này bao gồm 3 folder con tương ứng 3 ngành. 
        - Mỗi folder con có 3 file tương ứng với 3 khung thời gian. Như vậy sẽ có 3 kết quả tìm cặp tương ứng cho 3 khung thời gian 
    - File `config.yaml` chứa các thông số cài đặt cho code tìm cặp 
        - QUAN TRỌNG: `split_ratio` là tỉ lệ chia thời gian tìm cặp (train) và thời gian trade (test)
            - Thông số `train_period` và `test_period` là hai thông số tương ứng với tỉ lệ `split_ratio`. 
            - BỎ QUA hai thông số này. CHỈ sử dụng `split_ratio`
        - Các thông số về chia khung thời gian gồm có 
            - `start_date_phase_1`
            - `end_date_phase_1`
            - `start_date_phase_2`
            - `end_date_phase_2`
            - `start_date_phase_3`
            - `end_date_phase_3`
        - Các thông số còn lại là các đường dẫn đến file data 
            - CÓ THỂ BỎ QUA 

### **III. Results**
1. Folder `results/pairs_formation` chứa kết quả chọn cặp 
    - Folder này gồm 3 folder con tương ứng với 3 ngành
    - Mỗi folder con chứa 3 file `csv` tương ứng với kết quả chọn cặp cho 3 khung thời gian 
    - Cú pháp mỗi file kết quả bao gồm `{tên_ngành}_pairs_formation_{khung_thời_gian}_period_{ngày_sinh_ra_kết_qủa}.csv`

### **IV. Source code**
1. BỎ QUA folder `src/__pycache__`
2. Các file source code tổ chức như sau 
    - `config_snippets.py`: chứa hàm đọc file config.yaml
    - `data_transformation_snippets.py`: chứa hàm để transform data 
    - `engle_granger_cointegration_method.py`: chứa hàm để thực hiện kiểm định Engle-Granger
    - `explore_stats.py`: chứa hàm để tính toán các thống kê (ví dụ như tỉ lệ giá trị rỗng) cho bước tiền xử lý dữ liệu
    - `explore_stock.py`: chứa hàm để tính toán các thống kê về đặc điểm của cổ phiếu (ví dụ giá trị trung bình khối lượng giao dịch) phục vụ cho bước chọn các cổ phiếu để phân tích
    - `gatev_distance_method.py`: chứa hàm để chọn cặp theo phương pháp Gatev
    - `handling_dataframe.py`: chứa hàm để xử lý các task liên quan đến dataframe 
        - QUAN TRỌNG: bao gồm các hàm liên quan đến pivot dữ liệu; tổng hợp kết quả chọn cặp
    - `johansen_cointegration_method.py`: chứa hàm để thực hiện kiểm định Johansen
    - `splitting_data`: chứa hàm để chia dữ liệu thành tập dữ liệu dùng chọn cặp và tập dữ liệu trading. Có hai cách chia: theo tỉ lệ hoặc theo ngày tháng cụ thể 
    - `time_series_analysis_snippets.py`: chứa hàm dùng để phân tích chuỗi thời gian 



