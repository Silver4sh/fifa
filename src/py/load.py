import pandas as pd
import os

def load_csv_data(file_path=None):
    if file_path is None:
        file_path = os.path.join("data", "data.csv")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file tidak ditemukan: {file_path}")
    
    try:
        data_frame = pd.read_csv(file_path)
        # Hilangkan semua kolom "Unnamed: ..." (misalnya "Unnamed: 0")
        data_frame = data_frame.loc[:, ~data_frame.columns.str.startswith('Unnamed')]
    except Exception as e:
        raise Exception(f"Gagal membaca CSV file: {e}")
    
    return data_frame