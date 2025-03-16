import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class FIFAPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FIFA Match Prediction")
        self.root.geometry("500x350")
        
        self.data = None
        self.model = None
        self.teams = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Tombol untuk memuat file CSV
        self.load_button = tk.Button(self.root, text="Load CSV Data", command=self.load_data)
        self.load_button.pack(pady=10)
        
        # Dropdown untuk memilih tim kandang dan tandang
        self.home_team_var = tk.StringVar(self.root)
        self.away_team_var = tk.StringVar(self.root)
        
        tk.Label(self.root, text="Pilih Tim Kandang:").pack()
        self.home_team_dropdown = ttk.Combobox(self.root, textvariable=self.home_team_var, state="readonly")
        self.home_team_dropdown.pack(pady=5)
        
        tk.Label(self.root, text="Pilih Tim Tandang:").pack()
        self.away_team_dropdown = ttk.Combobox(self.root, textvariable=self.away_team_var, state="readonly")
        self.away_team_dropdown.pack(pady=5)
        
        # Tombol untuk melakukan prediksi
        self.predict_button = tk.Button(self.root, text="Predict Match Result", command=self.predict_result, state="disabled")
        self.predict_button.pack(pady=20)
        
        # Label untuk menampilkan hasil prediksi
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)
    
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                # Memuat data dari CSV
                self.data = pd.read_csv(file_path)
                
                # Validasi kolom yang dibutuhkan
                required_columns = {'home_team', 'away_team', 'home_score', 'away_score'}
                if not required_columns.issubset(self.data.columns):
                    messagebox.showerror("Error", "CSV harus memuat kolom: home_team, away_team, home_score, dan away_score.")
                    return
                
                # Membuat kolom target: 1 = kemenangan kandang, 0 = seri, -1 = kemenangan tandang
                self.data['result'] = self.data.apply(
                    lambda row: 1 if row['home_score'] > row['away_score'] 
                    else (-1 if row['home_score'] < row['away_score'] else 0), axis=1)
                
                # Mengambil daftar tim yang unik
                teams = pd.concat([self.data['home_team'], self.data['away_team']]).unique()
                self.teams = list(teams)
                self.home_team_dropdown['values'] = self.teams
                self.away_team_dropdown['values'] = self.teams
                
                # Mempersiapkan fitur dengan one-hot encoding untuk kolom tim
                features = pd.get_dummies(self.data[['home_team', 'away_team']])
                target = self.data['result']
                
                # Pisahkan data untuk training (di sini hanya untuk demonstrasi)
                X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
                
                # Melatih model RandomForestClassifier
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                self.model.fit(X_train, y_train)
                
                messagebox.showinfo("Success", "Data berhasil dimuat dan model telah dilatih!")
                self.predict_button.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat data: {e}")
    
    def predict_result(self):
        home_team = self.home_team_var.get()
        away_team = self.away_team_var.get()
        
        # Validasi input dropdown
        if not home_team or not away_team:
            messagebox.showwarning("Input Error", "Pilih kedua tim kandang dan tandang.")
            return
        if home_team == away_team:
            messagebox.showwarning("Input Error", "Tim kandang dan tim tandang tidak boleh sama.")
            return
        
        # Mempersiapkan data input untuk prediksi
        input_df = pd.DataFrame({
            'home_team': [home_team],
            'away_team': [away_team]
        })
        input_features = pd.get_dummies(input_df)
        
        # Menjamin bahwa input memiliki kolom yang sama dengan data training
        training_columns = self.model.feature_names_in_ if hasattr(self.model, "feature_names_in_") else pd.get_dummies(self.data[['home_team', 'away_team']]).columns
        for col in training_columns:
            if col not in input_features.columns:
                input_features[col] = 0
        input_features = input_features[training_columns]
        
        # Melakukan prediksi
        prediction = self.model.predict(input_features)[0]
        if prediction == 1:
            result_text = f"{home_team} diprediksi menang!"
        elif prediction == -1:
            result_text = f"{away_team} diprediksi menang!"
        else:
            result_text = "Prediksi hasil: Seri!"
        
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FIFAPredictionApp(root)
    root.mainloop()
