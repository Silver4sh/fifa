import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class FIFAMatchPrediction:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ FIFA Match Prediction")
        self.root.geometry("500x400")
        
        ttk.Label(root, text="🔮 FIFA Match Prediction", font=("Arial", 14)).pack(pady=10)
        
        self.file_csv = None
        self.select_file_button = ttk.Button(root, text="📂 Pilih File CSV", command=self.load_csv)
        self.select_file_button.pack(pady=5)
        
        self.file_status_label = ttk.Label(root, text="⚠️ Belum ada file CSV yang dimuat!", foreground="red")
        self.file_status_label.pack(pady=5)
        
        ttk.Label(root, text="🏟️ Tim Kandang:").pack()
        self.home_team_combobox = ttk.Combobox(root, state="readonly")
        self.home_team_combobox.pack()
        
        ttk.Label(root, text="🚀 Tim Tandang:").pack()
        self.away_team_combobox = ttk.Combobox(root, state="readonly")
        self.away_team_combobox.pack()
        
        self.predict_button = ttk.Button(root, text="🔮 Prediksi Hasil", command=self.predict_match, state="disabled")
        self.predict_button.pack(pady=10)
        
        self.result_label = ttk.Label(root, text="", font=("Arial", 12), foreground="blue")
        self.result_label.pack(pady=10)
        
        self.model_home = None
        self.model_away = None
        self.label_encoder = None
    
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        df = pd.read_csv(file_path)
        if not {'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'}.issubset(df.columns):
            messagebox.showerror("Error", "CSV harus memiliki kolom: HomeTeam, AwayTeam, FTHG, FTAG")
            return
        
        self.file_csv = file_path
        self.model_home, self.model_away, self.label_encoder = self.train_model(df)
        self.load_teams()
        self.file_status_label.config(text=f"✅ Data telah dimuat!", foreground="green")
        self.predict_button.config(state="normal")
    
    def load_teams(self):
        if self.label_encoder:
            teams = list(self.label_encoder.classes_)
            self.home_team_combobox["values"] = teams
            self.away_team_combobox["values"] = teams
        else:
            messagebox.showerror("Error", "Gagal memuat tim!")
    
    def train_model(self, df):
        label_encoder = LabelEncoder()
        all_teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
        label_encoder.fit(all_teams)

        df['HomeTeam'] = label_encoder.transform(df['HomeTeam'])
        df['AwayTeam'] = label_encoder.transform(df['AwayTeam'])

        X = df[['HomeTeam', 'AwayTeam']]
        y_home = df['FTHG']
        y_away = df['FTAG']

        X_train_home, X_test_home, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
        model_home = RandomForestClassifier(n_estimators=100, random_state=42)
        model_home.fit(X_train_home, y_train_home)

        X_train_away, X_test_away, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)
        model_away = RandomForestClassifier(n_estimators=100, random_state=42)
        model_away.fit(X_train_away, y_train_away)

        return model_home, model_away, label_encoder
    
    def predict_match(self):
        home_team = self.home_team_combobox.get()
        away_team = self.away_team_combobox.get()
        
        if not home_team or not away_team:
            messagebox.showerror("Input Salah", "Pilih tim kandang dan tandang!")
            return
        if home_team == away_team:
            messagebox.showerror("Input Salah", "Tim kandang dan tandang tidak boleh sama!")
            return
        
        home_encoded = self.label_encoder.transform([home_team])[0]
        away_encoded = self.label_encoder.transform([away_team])[0]
        
        new_match = pd.DataFrame({'HomeTeam': [home_encoded], 'AwayTeam': [away_encoded]})
        
        predicted_home_goals = self.model_home.predict(new_match)
        predicted_away_goals = self.model_away.predict(new_match)
        
        score_text = f"{home_team} {predicted_home_goals[0]} - {predicted_away_goals[0]} {away_team}"
        
        if predicted_home_goals[0] > predicted_away_goals[0]:
            result = f"{home_team} Menang"
        elif predicted_home_goals[0] < predicted_away_goals[0]:
            result = f"{away_team} Menang"
        else:
            result = "Seri"
        
        self.result_label.config(text=f"🔮 Hasil: {result} (Skor: {score_text})", foreground="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = FIFAMatchPrediction(root)
    root.mainloop()
