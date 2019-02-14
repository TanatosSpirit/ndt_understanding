import numpy as np
import pylab

pylab.ion()
x = np.arange(0, 4*np.pi, 0.1)
y = [np.sin(i) for i in x]
for n in range(50):
    y = [np.sin(i+n/10) for i in x]

    pylab.clf()

    pylab.plot(x, y, 'g-', linewidth=1.5, markersize=4)

    pylab.draw()

    pylab.pause(0.01)
