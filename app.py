import streamlit as st
import psycopg2
import pandas as pd
from io import StringIO

# Cấu hình kết nối tới PostgreSQL
DB_CONFIG = {
    'host': '193.200.105.32',
    'dbname': 'postgres',
    'user': 'phuongpml',
    'password': '!!sunjin@123',
    'port': '5433'  # thường là 5432
}

# Hàm lấy dữ liệu từ PostgreSQL
def fetch_data(start_date, product_name):
    query = """
        SELECT * FROM production_qm.production_formulas
        WHERE date = %s
    """
    params = [start_date]
    
    if product_name != "All":
        query += " AND product_name = %s"
        params.append(product_name)
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df

# Giao diện Streamlit
st.title("Formula Data Extractor")

# Bộ lọc người dùng
st.sidebar.header("Filter Conditions")
start_date = st.sidebar.date_input("Date")

# Kết nối để lấy danh sách sản phẩm (tuỳ chọn)
with psycopg2.connect(**DB_CONFIG) as conn:
    products = pd.read_sql_query('SELECT DISTINCT product_name FROM production_qm.production_formulas', conn)
product_list = ["All"] + products["product_name"].tolist()
product_name = st.sidebar.selectbox("Product", product_list)

# Nút tải dữ liệu
if st.sidebar.button("Extract Data"):
    df = fetch_data(start_date, product_name)

    if not df.empty:
        st.success(f"Found {len(df)} records.")
        st.dataframe(df)

        # Tải về CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_buffer.getvalue(),
            file_name="formula_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data found for the selected conditions.")