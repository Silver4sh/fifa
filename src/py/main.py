import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd  
import webbrowser
import load
import features

class AutocompleteCombobox(ttk.Combobox):
    """
    Combobox dengan fitur autocomplete.
    Dropdown akan muncul saat fokus masuk tanpa input,
    dan menyajikan saran sesuai input.
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._completion_list = []
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind("<FocusIn>", self.on_focusin)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list

    def on_focusin(self, event):
        if not self.get():
            self['values'] = self._completion_list
            self.event_generate('<Down>')

    def handle_keyrelease(self, event):
        if event.keysym in ("BackSpace", "Left", "Right", "Up", "Down", "Return", "Escape"):
            return
        text = self.get()
        if text == '':
            self['values'] = self._completion_list
        else:
            filtered = [item for item in self._completion_list if item.lower().startswith(text.lower())]
            self['values'] = filtered if filtered else self._completion_list

class FIFAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FIFA Data Viewer")
        self.configure(bg="#f0f0f0")
        self.data_frame = None

        # Setup style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10))
        
        self.create_widgets()
        self.ask_for_csv()  
        
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())
        
    def create_widgets(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="FIFA Data Viewer", style="Header.TLabel")
        title_label.pack(side=tk.LEFT, padx=(0,20))
        
        self.status_label = ttk.Label(header_frame, text="Silakan pilih file CSV")
        self.status_label.pack(side=tk.LEFT, padx=(0,20))
        
        load_button = ttk.Button(header_frame, text="Pilih CSV", command=self.ask_for_csv)
        load_button.pack(side=tk.RIGHT)
        
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Info Player", command=self.show_info_player)\
            .grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Info Team", command=self.show_info_team)\
            .grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Summary", command=self.show_summary)\
            .grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Top Player", command=self.show_top_player)\
            .grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Top Team", command=self.show_top_team)\
            .grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(button_frame, text="Visual Data", command=self.show_visual_data)\
            .grid(row=0, column=5, padx=5, pady=5)
        
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
        # Data disimpan ke memori (tidak langsung ditampilkan)
        
    def show_info_player(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        win = tk.Toplevel(self)
        win.title("Info Player")
        
        ttk.Label(win, text="Masukkan atau pilih nama pemain:").pack(pady=5)
        try:
            player_list = sorted(self.data_frame['Name'].dropna().unique().tolist())
        except KeyError:
            messagebox.showerror("Error", "Kolom 'Name' tidak ditemukan.")
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
                player_win = tk.Toplevel(self)
                player_win.title(f"Info Player: {player_name}")
                
                frame_player = ttk.Frame(player_win)
                frame_player.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
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
                
                def on_double_click(event):
                    item = tree.identify_row(event.y)
                    if item:
                        values = tree.item(item, "values")
                        if values and str(values[1]).lower().startswith("http"):
                            webbrowser.open(str(values[1]))
                tree.bind("<Double-1>", on_double_click)
                
                player_win.minsize(400, 300)
            win.destroy()
        
        ttk.Button(win, text="Tampilkan Info", command=on_select).pack(pady=5)
        win.minsize(300, 120)
        
    def show_info_team(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        win = tk.Toplevel(self)
        win.title("Info Team")
        
        ttk.Label(win, text="Masukkan atau pilih nama tim:").pack(pady=5)
        try:
            team_list = sorted(self.data_frame['Club'].dropna().unique().tolist())
        except KeyError:
            messagebox.showerror("Error", "Kolom 'Club' tidak ditemukan.")
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
                
                ttk.Label(team_win, text=f"Data untuk tim: {team_name}", style="Header.TLabel")\
                    .pack(pady=5)
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
                
                def on_double_click(event):
                    item = tree.identify_row(event.y)
                    if item:
                        values = tree.item(item, "values")
                        for cell in values:
                            if str(cell).lower().startswith("http"):
                                webbrowser.open(str(cell))
                                break
                tree.bind("<Double-1>", on_double_click)
                
                team_win.minsize(500, 300)
            win.destroy()
        
        ttk.Button(win, text="Tampilkan Info", command=on_select).pack(pady=5)
        win.minsize(300, 120)
        
    def show_summary(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        extract_location = filedialog.asksaveasfilename(
            title="Pilih lokasi untuk menyimpan summary",
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("Excel Files", "*.xls"), ("All Files", "*.*")]
        )
        if not extract_location:
            messagebox.showwarning("Peringatan", "Lokasi ekstrak tidak dipilih!")
            return
        
        summary_stats = features.summary(self.data_frame)
        try:
            if not isinstance(summary_stats, pd.DataFrame):
                summary_stats = pd.DataFrame(summary_stats)
            summary_stats.to_excel(extract_location, index=True)
            messagebox.showinfo("Success", f"Summary berhasil disimpan di: {extract_location}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan summary: {e}")
        
    def show_top_player(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return

        sel_win = tk.Toplevel(self)
        sel_win.title("Pilih Kriteria Top Player")
        sel_win.resizable(False, False)
        
        ttk.Label(sel_win, text="Pilih kriteria:")\
            .grid(row=0, column=0, padx=10, pady=10, sticky="w")
        choice_var = tk.StringVar(value="overall")
        ttk.Radiobutton(sel_win, text="Overall", variable=choice_var, value="overall")\
            .grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(sel_win, text="Berdasarkan Posisi", variable=choice_var, value="position")\
            .grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        frame_combo = ttk.Frame(sel_win)
        frame_combo.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        ttk.Label(frame_combo, text="Pilih posisi:")\
            .grid(row=0, column=0, padx=5, pady=5, sticky="w")
        pos_combo = AutocompleteCombobox(frame_combo, state="disabled")
        pos_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        def update_combo(*args):
            if choice_var.get() == "position":
                try:
                    pos_list = sorted(self.data_frame['Position'].dropna().unique().tolist())
                except KeyError:
                    messagebox.showerror("Error", "Kolom 'Position' tidak ditemukan.")
                    sel_win.destroy()
                    return
                pos_combo.set_completion_list(pos_list)
                pos_combo.config(state="normal")
            else:
                pos_combo.set("")
                pos_combo.config(state="disabled")
        choice_var.trace("w", update_combo)
        update_combo()
        
        def on_select():
            if choice_var.get() == "overall":
                top_players = features.top_player(self.data_frame)
            else:
                pos = pos_combo.get().strip()
                if not pos:
                    messagebox.showwarning("Warning", "Silakan pilih posisi terlebih dahulu.")
                    return
                top_players = features.top_player_by_position(self.data_frame, pos)
            if top_players is None or top_players.empty:
                messagebox.showinfo("Top Player", "Data top player tidak tersedia.")
                return

            res_win = tk.Toplevel(self)
            res_win.title("Top Players")
            res_frame = ttk.Frame(res_win)
            res_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            res_win.rowconfigure(0, weight=1)
            res_win.columnconfigure(0, weight=1)
            
            tree = ttk.Treeview(res_frame, columns=list(top_players.columns), show="headings")
            tree.grid(row=0, column=0, sticky="nsew")
            scroll_y = ttk.Scrollbar(res_frame, orient="vertical", command=tree.yview)
            scroll_y.grid(row=0, column=1, sticky="ns")
            scroll_x = ttk.Scrollbar(res_frame, orient="horizontal", command=tree.xview)
            scroll_x.grid(row=1, column=0, sticky="ew")
            tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            res_frame.rowconfigure(0, weight=1)
            res_frame.columnconfigure(0, weight=1)
            
            for col in top_players.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")
            for row in top_players.itertuples(index=False):
                tree.insert("", tk.END, values=list(row))
            
            res_win.minsize(500, 300)
            sel_win.destroy()
        
        ttk.Button(sel_win, text="Tampilkan Top Player", command=on_select)\
            .grid(row=2, column=2, padx=10, pady=10, sticky="e")
        sel_win.focus_force()
        
    def show_top_team(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        
        top_teams = features.top_team(self.data_frame)
        if top_teams is None or top_teams.empty:
            messagebox.showinfo("Top Team", "Data top team tidak tersedia.")
            return
        
        win = tk.Toplevel(self)
        win.title("Top Teams")
        frame = ttk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=list(top_teams.columns), show="headings")
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        
        for col in top_teams.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        for _, row in top_teams.iterrows():
            tree.insert("", tk.END, values=list(row))
            
        win.minsize(500, 300)
        
    def show_visual_data(self):
        if self.data_frame is None:
            messagebox.showwarning("Warning", "Data belum dimuat!")
            return
        features.visual_data(self.data_frame, self)

if __name__ == "__main__":
    app = FIFAApp()
    app.mainloop()
