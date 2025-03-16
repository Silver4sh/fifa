import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_player_radar(data, input_team, input_player):
    club_info = data.loc[data['Club'] == input_team]
    
    list_player = club_info[['Name', 'Position']].sort_values('Position', ascending=False)
    
    get_player = club_info.loc[club_info['Name'] == input_player]
    
    if get_player.empty:
        print("Pemain tidak ditemukan dalam klub tersebut.")
        return
    
    attributes = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality']
    average_attributes = get_player[attributes].values[0]
    
    num_attributes = len(attributes)
    
    angles = np.linspace(0, 2 * np.pi, num_attributes, endpoint=False).tolist()
    angles += angles[:1]
    
    values = np.append(average_attributes, average_attributes[0])
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    
    plt.xticks(angles[:-1], attributes, color='black', size=10)
    ax.set_yticklabels([])
    
    plt.title(input_player, size=20, color='black', y=1.1)
    
    for i in range(num_attributes):
        angle_rad = angles[i]
        ax.text(angle_rad, values[i] + 5, str(values[i]), ha='center', va='center', color='red', fontsize=10)
    
    plt.tight_layout()
    plt.show()