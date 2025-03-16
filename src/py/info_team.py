import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_team_radar(data, input_team):

    attributes = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality']
    
    club_info = data.loc[data['Club'] == input_team]
    if club_info.empty:
        print(f"Klub '{input_team}' tidak ditemukan.")
        return
    
    avg_attr = club_info[attributes].mean().round(2)
    
    num_attributes = len(attributes)
    angles = np.linspace(0, 2 * np.pi, num_attributes, endpoint=False).tolist()
    angles += angles[:1]  
    
    values = avg_attr.values
    values = np.append(values, values[0])
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], attributes, color='black', size=10)
    
    ax.fill(angles, values, 'b', alpha=0.1)
    ax.plot(angles, values, color='b', linewidth=2)
    ax.set_yticklabels([])
    
    plt.title(input_team, size=20, color='black', y=1.1)
    
    for i in range(num_attributes):
        angle_rad = angles[i]
        ax.text(angle_rad, values[i] + 5, str(values[i]), ha='center', va='center', color='red', fontsize=10)
    
    plt.tight_layout()
    plt.show()