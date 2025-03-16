import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd  # Untuk ekspor Excel
import webbrowser
import load
import features

# --- Kelas AutocompleteCombobox ---
class AutocompleteCombobox(ttk.Combobox):
    """
    Combobox dengan fitur autocomplete sederhana.
    Saat mengetik, dropdown akan menyajikan saran yang sesuai.
    """
    def __init__(self, master=None, **kwargs):
        # Jangan set state="readonly" agar user bisa mengetik manual.
        super().__init__(master, **kwargs)
        self._completion_list = []
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list

    def handle_keyrelease(self, event):
        # Abaikan tombol navigasi tertentu
        if event.keysym in ("BackSpace", "Left", "Right", "Up", "Down", "Return", "Escape"):
            return
        text = self.get()
        if text == '':
            self['values'] = self._completion_list
        else:
            filtered = [item for item in self._completion_list if item.lower().startswith(text.lower())]
            self['values'] = filtered if filtered else self._completion_list

# --- Kelas aplikasi utama ---
class FIFAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FIFA Data Viewer")
        self.configure(bg="#f0f0f0")
        self.data_frame = None

        # Setup tampilan dengan ttk.Style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10))
        
        self.create_widgets()
        self.ask_for_csv()  # Meminta input file CSV di awal
        
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        
    def create_widgets(self):
        # Header frame: Judul, status, dan tombol pilih CSV
        header_frame = ttk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="FIFA Data Viewer", style="Header.TLabel")
        title_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.status_label = ttk.Label(header_frame, text="Silakan pilih file CSV")
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        load_button = ttk.Button(header_frame, text="Pilih CSV", command=self.ask_for_csv)
        load_button.pack(side=tk.RIGHT)
        
        # Tidak dibuat content frame (Treeview) agar tidak muncul box kosong di awal.
        
        # Frame tombol fitur tambahan (diletakkan di bagian bawah)
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        info_player_button = ttk.Button(button_frame, text="Info Player", command=self.show_info_player)
        info_player_button.grid(row=0, column=0, padx=5, pady=5)
        
        info_team_button = ttk.Button(button_frame, text="Info Team", command=self.show_info_team)
        info_team_button.grid(row=0, column=1, padx=5, pady=5)
        
        summary_button = ttk.Button(button_frame, text="Summary", command=self.show_summary)
        summary_button.grid(row=0, column=2, padx=5, pady=5)
        
        top_player_button = ttk.Button(button_frame, text="Top Player", command=self.show_top_player)
        top_player_button.grid(row=0, column=3, padx=5, pady=5)
        
        visual_data_button = ttk.Button(button_frame, text="Visual Data", command=self.show_visual_data)
        visual_data_button.grid(row=0, column=4, padx=5, pady=5)
        
    def ask_for_csv(self):
        file_path = filedialog.askopenfilename(
            title="Pilih file CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            self.load_data(file_path)
        else:
            messagebox.showwarning("Peringatan", "Tidak ada file CSV yang dipilih!")
            self.status_label.config(text="Tidak ada file CSV yang dipilih!")
    
    def load_data(self, file_path):
        try:
            self.data_frame = load.load_csv_data(file_path)
            self.status_label.config(text="Data berhasil dimuat!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text=str(e))
            return
        # Data dimuat ke memori tanpa langsung ditampilkan di GUI.
        
    def show_info_player(self):
        """Tampilkan Info Player dengan AutocompleteCombobox; hasil info ditampilkan dalam Treeview (tanpa scrollbar horizontal)."""
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        win = tk.Toplevel(self)
        win.title("Info Player")
        
        label = ttk.Label(win, text="Masukkan atau pilih nama pemain:")
        label.pack(pady=5)
        
        try:
            player_list = sorted(self.data_frame['Name'].dropna().unique().tolist())
        except KeyError:
            messagebox.showerror("Error", "Kolom 'Name' tidak ditemukan dalam data.")
            win.destroy()
            return
        
        combo = AutocompleteCombobox(win)
        combo.set_completion_list(player_list)
        combo.pack(pady=5, padx=10, fill=tk.X)
        
        def on_select():
            player_name = combo.get().strip()
            info = features.info_player(self.data_frame, player_name)
            if info is None:
                messagebox.showinfo("Info Player", f"Data untuk pemain '{player_name}' tidak ditemukan.")
            else:
                # Tampilkan hasil info dalam Treeview dengan dua kolom: Attribute dan Value
                player_win = tk.Toplevel(self)
                player_win.title(f"Info Player: {player_name}")
                
                frame_player = ttk.Frame(player_win)
                frame_player.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Hanya scrollbar vertikal (tanpa scrollbar horizontal)
                scroll_y = ttk.Scrollbar(frame_player, orient="vertical")
                scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
                
                tree = ttk.Treeview(frame_player,
                                    columns=("attribute", "value"),
                                    show="headings",
                                    yscrollcommand=scroll_y.set)
                tree.heading("attribute", text="Attribute")
                tree.heading("value", text="Value")
                
                for k, v in info.items():
                    tree.insert("", tk.END, values=(k, v))
                
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scroll_y.config(command=tree.yview)
                
                # Jika ada baris dengan attribute 'url', biarkan double-click membuka URL
                def on_double_click(event):
                    item = tree.identify_row(event.y)
                    if item:
                        values = tree.item(item, "values")
                        if values and values[0].lower() == "url" and str(values[1]).startswith("http"):
                            webbrowser.open(str(values[1]))
                tree.bind("<Double-1>", on_double_click)
                
                player_win.update()
                player_win.minsize(player_win.winfo_width(), player_win.winfo_height())
            win.destroy()
        
        button = ttk.Button(win, text="Tampilkan Info", command=on_select)
        button.pack(pady=5)
        
        win.update()
        win.minsize(win.winfo_width(), win.winfo_height())
        
    def show_info_team(self):
        """Tampilkan Info Team dengan AutocompleteCombobox; hasil ditampilkan dalam Treeview yang fit dan rapi."""
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        win = tk.Toplevel(self)
        win.title("Info Team")
        
        label = ttk.Label(win, text="Masukkan atau pilih nama tim:")
        label.pack(pady=5)
        
        try:
            team_list = sorted(self.data_frame['Club'].dropna().unique().tolist())
        except KeyError:
            messagebox.showerror("Error", "Kolom 'Club' tidak ditemukan dalam data.")
            win.destroy()
            return
        
        combo = AutocompleteCombobox(win)
        combo.set_completion_list(team_list)
        combo.pack(pady=5, padx=10, fill=tk.X)
        
        def on_select():
            team_name = combo.get().strip()
            team_data = features.info_team(self.data_frame, team_name)
            if team_data is None or team_data.empty:
                messagebox.showinfo("Info Team", f"Data untuk tim '{team_name}' tidak ditemukan.")
            else:
                team_win = tk.Toplevel(self)
                team_win.title(f"Info Team: {team_name}")
                
                label_title = ttk.Label(team_win, text=f"Data untuk tim: {team_name}", style="Header.TLabel")
                label_title.pack(pady=5)
                
                frame_team = ttk.Frame(team_win)
                frame_team.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                scroll_y = ttk.Scrollbar(frame_team, orient="vertical")
                scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
                scroll_x = ttk.Scrollbar(frame_team, orient="horizontal")
                scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
                
                tree = ttk.Treeview(frame_team,
                                    columns=list(team_data.columns),
                                    show="headings",
                                    yscrollcommand=scroll_y.set,
                                    xscrollcommand=scroll_x.set)
                for col in team_data.columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100, anchor="center")
                for _, row in team_data.iterrows():
                    tree.insert("", tk.END, values=list(row))
                
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scroll_y.config(command=tree.yview)
                scroll_x.config(command=tree.xview)
                
                team_win.update()
                team_win.minsize(team_win.winfo_width(), team_win.winfo_height())
            win.destroy()
        
        button = ttk.Button(win, text="Tampilkan Info", command=on_select)
        button.pack(pady=5)
        
        win.update()
        win.minsize(win.winfo_width(), win.winfo_height())
        
    def show_summary(self):
        """Ekspor summary sebagai file Excel (XLSX/XLS)."""
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        extract_location = filedialog.asksaveasfilename(
            title="Pilih lokasi untuk menyimpan hasil ekstrak data",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("Excel Files", "*.xls"),
                ("All Files", "*.*")
            ]
        )
        if not extract_location:
            messagebox.showwarning("Peringatan", "Lokasi ekstrak tidak dipilih!")
            return
        
        summary_stats = features.summary(self.data_frame)
        try:
            if not isinstance(summary_stats, pd.DataFrame):
                summary_stats = pd.DataFrame(summary_stats)
            summary_stats.to_excel(extract_location, index=True)
            messagebox.showinfo("Success", f"Summary data berhasil diekstrak ke: {extract_location}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan summary data: {e}")
        
    def show_top_player(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        top_players = features.top_player(self.data_frame)
        if top_players is None or top_players.empty:
            messagebox.showinfo("Top Player", "Data top player tidak tersedia.")
            return
        
        window = tk.Toplevel(self)
        window.title("Top Players")
        
        frame_top = ttk.Frame(window)
        frame_top.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(frame_top, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = ttk.Scrollbar(frame_top, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        tree = ttk.Treeview(frame_top,
                            columns=list(top_players.columns),
                            show="headings",
                            yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set)
        for col in top_players.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        for _, row in top_players.iterrows():
            tree.insert("", tk.END, values=list(row))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        window.update()
        window.minsize(window.winfo_width(), window.winfo_height())
            
    def show_visual_data(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        features.visual_data(self.data_frame, self)

if __name__ == "__main__":
    app = FIFAApp()
    app.mainloop()
