import matplotlib.pyplot as plt

def plot_nation(nation_data):

    nations = [item[0] for item in nation_data]
    count_players = [item[1] for item in nation_data]
    
    plt.figure(figsize=(10, 6))
    plt.bar(nations, count_players, color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.title('Count of Items by Country')
    plt.xticks(rotation=45)  
    plt.tight_layout()
    plt.show()

def plot_position(position_count):

    positions = [item[0] for item in position_count]
    count_players = [item[1] for item in position_count]
    
    plt.figure(figsize=(10, 6))
    plt.bar(positions, count_players, color='salmon')
    plt.xlabel('Position')
    plt.ylabel('Count')
    plt.title('Count of Items by Position')
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.show()