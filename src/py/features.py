import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def info_player(data_frame, player_name):
    if 'Name' not in data_frame.columns:
        messagebox.showerror("Error", "Kolom 'Name' tidak ditemukan dalam data.")
        return None
    result = data_frame[data_frame['Name'].str.lower() == player_name.lower()]
    if result.empty:
        return None
    return result.iloc[0].to_dict()

def info_team(data_frame, team_name):
    if 'Club' not in data_frame.columns:
        messagebox.showerror("Error", "Kolom 'Club' tidak ditemukan dalam data.")
        return None
    result = data_frame[data_frame['Club'].str.lower() == team_name.lower()]
    if result.empty:
        return None
    return result

def summary(data_frame):
    # Mengembalikan statistik ringkasan untuk kolom numerik
    return data_frame.describe()

def top_player(data_frame, top_n=5):
    if 'Overall' not in data_frame.columns:
        messagebox.showerror("Error", "Kolom 'Overall' tidak ditemukan dalam data.")
        return None
    sorted_df = data_frame.sort_values(by='Overall', ascending=False)
    return sorted_df.head(top_n)

def top_team(data_frame, top_n=5):
    """
    Menghitung rata-rata rating 'Overall' per tim dan mengembalikan top team.
    Pastikan kolom 'Club' dan 'Overall' ada dalam data.
    """
    if 'Club' not in data_frame.columns or 'Overall' not in data_frame.columns:
        messagebox.showerror("Error", "Kolom 'Club' atau 'Overall' tidak ditemukan dalam data.")
        return None
    group = data_frame.groupby('Club')['Overall'].mean().reset_index()
    group = group.sort_values(by='Overall', ascending=False)
    return group.head(top_n)

def visual_data(data_frame, master):
    window = Toplevel(master)
    window.title("Visual Data")
    
    if 'Overall' not in data_frame.columns:
        messagebox.showerror("Error", "Kolom 'Overall' tidak ditemukan dalam data.")
        return
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data_frame['Overall'].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_title("Distribusi Overall Rating")
    ax.set_xlabel("Overall Rating")
    ax.set_ylabel("Frequency")
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
