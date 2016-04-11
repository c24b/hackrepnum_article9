#
# histogram has the ability to plot multiple data in parallel ...
# Note the new color kwarg, used to override the default, which
# uses the line color cycle.
#
import pylab as P
mu, sigma = 200, 25
x = mu + sigma*P.randn(10000)

# the histogram of the data with histtype='step'
#n, bins, patches = P.hist(x, 50, normed=1, histtype='stepfilled')
#P.step(patches, 'facecolor', 'g', 'alpha', 0.75)

# add a line showing the expected distribution
#y = P.normpdf( bins, mu, sigma)
#l = P.plot(bins, y, 'k--', linewidth=1.5)

#P.figure()

# create a new data-set
x = mu + sigma*P.randn(1000,3)

n, bins, patches = P.hist(x, 10, normed=1, histtype='bar',
                            color=['crimson', 'burlywood', 'chartreuse'],
                            label=['Crimson', 'Burlywood', 'Chartreuse'])
P.legend()

#
# ... or we can stack the data
#
#P.figure()

n, bins, patches = P.hist(x, 10, normed=1, histtype='bar', stacked=True)

P.show()
