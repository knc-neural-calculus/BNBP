import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def plot_weights_hist(dirname, idx_str):

    fig, ax = plt.subplots(1,1)
    bins = np.linspace(-3.0,2.0, 50)
    
    print('reading files:')
    for n in range(0,3000,100):
        filename = dirname + idx_str + '/weights_' + idx_str + '_e-%d.csv' % n
        print('\t' + filename)
        
        if not os.path.isfile(filename):
            break
        else:
            all_weights = np.genfromtxt(filename, delimiter=',').flatten()
            hist, _ = np.histogram(all_weights,bins)
            ax.set_title(dirname)

            plt.plot(bins[:-1], hist, label=('e=%d' % n), c=[(n/100) / 30, 0.2, 0.2])


    plt.show()

def plot_weights_neg_percent(dirname, idx_str):
    bins = np.linspace(-2.0,2.0, 50)
    

    x = range(0,3000,100)
    y = []
    print('reading files:')
    for n in range(0,3000,100):
        filename = dirname + idx_str + '/weights_' + idx_str + '_e-%d.csv' % n
        print('\t' + filename)
        
        if not os.path.isfile(filename):
            break
        else:
            all_weights = np.genfromtxt(filename, delimiter=',').flatten()
            n_neg = 0
            for w in all_weights:
                if w < 0:
                    n_neg += 1 
            y.append(100 * n_neg / len(all_weights))
    plt.plot(x, y)
    plt.show()

def heatmap(dirname, idx_str, fig, ax, epoch):
    filename = dirname + idx_str + '/weights_' + idx_str + '_e-%d.csv' % epoch
    W = np.genfromtxt(filename, delimiter=',')

    X = range(0, W.shape[0])
    Y = range(0, W.shape[1])
    
    im = ax.imshow(W, cmap='seismic', interpolation='nearest')

    ax.set_title("epoch = %d, idx_str = %s" % (epoch, idx_str))
    cbar = ax.figure.colorbar(im, ax=ax)

def heatmap2(dirname, idx_str, fig, ax, epoch, row_idx):
    filename = dirname + idx_str + '/weights_' + idx_str + '_e-%d.csv' % epoch
    W = np.genfromtxt(filename, delimiter=',')
    W = W[row_idx][:-1]
    W = W.reshape((28, 28))

    X = range(0, W.shape[0])
    Y = range(0, W.shape[1])
    
    im = ax.imshow(W, cmap='seismic', interpolation='nearest')

#    ax.set_title("e %d, r %d" % (epoch, row_idx))
#    cbar = ax.figure.colorbar(im, ax=ax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    


if __name__ == "__main__":
#    fig, axs = plt.subplots(4,1)
#    heatmap(sys.argv[1], 'W2', fig, axs[0], 0)
#    heatmap(sys.argv[1], 'W2', fig, axs[1], 3000)
#    heatmap(sys.argv[1], 'W2', fig, axs[2], 7000)
#    heatmap(sys.argv[1], 'W2', fig, axs[3], 11900)

#    plot_weights_hist(sys.argv[1], "W1")
#    plot_weights_neg_percent(sys.argv[1], "W1")

#    epochs = [0, 500, 1000, 1500, 1900 ]
#    rows = [70 + i for i in range(30)]
#    fig, axs = plt.subplots(len(epochs), len(rows))
#
#    for i, r in enumerate(rows):
#        for j, e in enumerate(epochs):
#            print(i, j)
#            heatmap2(sys.argv[1], 'W1', fig, axs[j][i], e, r) 

    # Plot all at max epoch
    epoch = 1900
    fig, axs = plt.subplots(10, 10)
    for r in range(100): 
        print(r)
        heatmap2(sys.argv[1], 'W1', fig, axs[r % 10][r // 10], epoch, r) 
    plt.subplots_adjust(
            left=0.0, 
            right=0.45, 
            bottom=0.1, 
            top=0.9, 
            wspace=0.0, 
            hspace=0.1)

#    fig.tight_layout()
    plt.savefig('cool.png')
    plt.show()
