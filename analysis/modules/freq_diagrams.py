from matplotlib import pyplot as plt

def plot_freq_graph(data:dict, plot_name='plot', x_name = 'Names', y_name = 'Frequency', reverse = False, bars = 10):

    plt.clf()    
    n_bars = bars
    
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    
    if reverse == False:
        # Separate names and frequencies into lists
        names = list(data.keys())[:n_bars]
        frequencies = list(data.values())[:n_bars]
    else: 
        # Separate names and frequencies into lists
        names = list(data.values())[:n_bars]
        frequencies = list(data.keys())[:n_bars]

    # Create a bar plot
    plt.bar(names, frequencies)

    # Add labels and title
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(plot_name.replace('_',' '))
    plt.xticks(rotation=90)
    
    plt.savefig(f'.\\graphs\\freq\\{plot_name}.png', bbox_inches='tight', pad_inches=0)
    
def get_freq_dict(list_items:list):
    
    freq_dict = dict()
    for item in list_items:
        if item in freq_dict.keys():
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    return freq_dict