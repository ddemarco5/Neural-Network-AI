import pylab as plb
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pylab
import threading

fig1=plt.figure(1)
ax = fig1.add_subplot(1,1,1)

ax.plot([1,2,3],[4,5,6],'ro-')

#fig1.show()  # this does not show a figure if uncommented
plt.ion()     # turns on interactive mode
plt.show()    # now this should be non-blocking

print "doing something else now"
raw_input('Press Enter to continue...')

#from matplotlib.pyplot import plot, draw, show

#def function():
#	def make_plot():
#		plot([1,2,3])
#		draw()
#		print 'Plot displayed, waiting for it to be closed.'
#
#
#	
#	print('Do something before plotting.')
#	# Now display plot in a window
#	make_plot()
#	# This line was moved up <----
#	show()
#
#	#answer = raw_input('Back to main after plot window closed? ')
#	#if answer == 'y':
#	#	print('Move on')
#	#else:
#	#	print('Nope')
#
#function().start()
#print 'The main program continues to run in foreground.'
#background.join()
#print 'Main program waited until background was done.'

#pylab.ion()


#img = mpimg.imread('pixels.png')
#implot = plt.imshow(img)
#print "before"
#plt.show()
#print "after"


#plt.close()


#pylab.show()

#x = [1,2,3]
#y = [5,6,7]

#fig = plt.figure()
#plt.plot(x, y)

