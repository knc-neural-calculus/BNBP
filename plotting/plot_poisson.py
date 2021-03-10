import matplotlib.pyplot as plt
spiketrains = []
idx = 10
with open('../mnist/OUT_POISSON_' + str(idx) + '.txt', "r") as fl:
    for line in fl:
        spiketrains.append([int(e.strip()) for e in line.split(',') if e != '\n'])

x_pos = []
y_pos = []
for spiketrain in spiketrains:
    for spike in spiketrain:
        x_pos.append(spike)
        y_pos.append(idx) 
    idx += 1
plt.scatter(x_pos, y_pos, s = 0.4)
plt.savefig("poisson.png")

# Plot 2d histogram 
x_pos = []
y_pos = []
idx = 1
for spiketrain in spiketrains:
    for spike in spiketrain:
        x_pos.append(idx % 28)
        y_pos.append(idx / 28)
    idx += 1
print(len(x_pos))

plt.hist2d(x_pos, y_pos, bins = (20,20))
plt.savefig("poisson_histogram.png")
