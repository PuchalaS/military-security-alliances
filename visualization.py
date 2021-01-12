import matplotlib.pyplot as plt

def create_bar_plot(data, title):
    data = data[:10]
    data.sort(key=lambda x: x[1],reverse=True)
    #labels = [x+1 for x in range(len(data))]
    # = [labels, [n for _,n in data]]
  
    #lt.bar(new_data)
    fig = plt.figure(figsize=(9,9))
    plt.title(title)
    
    plt.bar(*zip(*data))
    plt.show()
