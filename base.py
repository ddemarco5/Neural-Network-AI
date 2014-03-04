from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from PIL import Image
import math

#for file listings
import os
import shutil

#to display the image
import webbrowser

def AvgColor( pixels, segment, width, height):
	
	###Setup our R, G, and B variables for some math!
	r = 0
	g = 0
	b = 0
	avgCount = 0

	x_start = width*segment[0]
	y_start = height*segment[1]
	
	##Debug info
	#print "x_start", x_start
	#print "y_start", y_start
	#print "width", width
	#print "height", height
	#print "rangex", range(x_start, width+x_start)
	#print "rangey", range(y_start, height+y_start)
	###Average the RGB values in the segment
	for x in range(x_start, width+x_start):
		for y in range(y_start, height+y_start):
			r+=pixels[x,y][0]
			g+=pixels[x,y][1]
			b+=pixels[x,y][2]
			
			avgCount+=1
	
	#print "avgCount=", avgCount
	###Get the averages, and return!
	rAvg = r/avgCount
	gAvg = g/avgCount
	bAvg = b/avgCount
	return (rAvg, gAvg, bAvg)

def ProcessImage( filename, segments ):
	"a function to return the array of an image to test the network with"
	
	img = Image.open(filename)
	
	###Grab the width, height, and build a list of each pixel in the image.
	width, height = img.size
	
	#cannot partition the image past pixels
	fwidth=float(width)
	fheight=float(height)
	if (segments > width) or (segments > height):
		print "Cannot choose partitions finer than the base pixel value"
		return None
	#if (fwidth/fheight > 1):
	#	minval = math.ceil(fwidth/fheight)
	#	print fwidth, fheight
	#	#print math.ceil(fwidth/fheight)
	#	if (segments > (fheight/minval)):
	#		print "Cannot segment higher than", height/minval , "in order to maintain proper ratios"
	#		return None
	#
	#if (fheight/fwidth > 1):
	#	minval = math.ceil(fheight/fwidth)
	#	print fheight, fwidth
	#	#print math.ceil(fheight/fwidth)
	#	if (segments > (fwidth/minval)):
	#		print "Cannot segment higher than", width/minval , "in order to maintain proper ratios"
	#		return None
		
	print "width:", width, " height:", height
	print width, "/", segments
	print height, "/", segments
	segment_width = width/segments
	segment_height = height/segments
	print "segment width:", segment_width, " segment height:", segment_height
	
	pixels = img.load()
	data = []
	for x in range(segment_width):
		for y in range(segment_height):
			cpixel = pixels[x, y]
			data.append(cpixel)
	#current segment will be an array showing the x and y coordinates of the segment
	avg = []
	
	#generate output image based on color averages
	out_image = Image.new('RGB', (segments,segments))
	standardavg = []
	
	for y in range(0, segments):
		for x in range(0, segments):
			rgb_avg = AvgColor(pixels, [x,y], segment_width, segment_height)
			hex_avg = '%02x%02x%02x' % rgb_avg
			standardavg.append(rgb_avg)
			avg.append(int(hex_avg, 16))
	
	out_image.putdata(standardavg)
	out_image.save("pixels.png", 'PNG')
	#out_image.show()
	
	#return '%02x%02x%02x' % avg
	return avg

def RunNet(net, dataset, train_epochs):
	"a function to build a neural net and test on it, for testing purposes right now"
	#print net.activate([2, 1])
	#ds = SupervisedDataSet(15, 1)
	#ds.addSample((1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), (100))
	#ds.addSample((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), (0))

	#trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99, verbose = True)
	trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.5, verbose = True)
	
	trainer.trainOnDataset(dataset, train_epochs)
	
	trainer.testOnData(verbose = True)

	#while True:
	#	number = raw_input("What number do you want to test on? (will be an array of 15): ")
	#	testdata = []
	#	for x in range(0,15):
	#		testdata.append(float(number))
	#
	#	print "Test Data:", testdata, "\n"
	#	net.sortModules()
	#	print "Returned Data", net.activate(testdata)

def	ActivateNet (data):
	return net.activate(data)

#main program execution	

partition_size = int(raw_input("Partition size: "))

#dataset
dataset = SupervisedDataSet(partition_size*partition_size, 2)

load = raw_input("Do you want to load the dataset from file?: ")

if (load == 'y'):
	dataset = dataset.loadFromFile("dataset")

else:
	for filename in os.listdir("Images(Training)/A"):
		print filename
		image_file='Images(Training)/A/'+ filename
		colordata = ProcessImage(image_file, partition_size)
		#webbrowser.open("pixels.png")
		#raw_input()
		dataset.addSample(colordata, (1, 0))
		
	for filename in os.listdir("Images(Training)/B"):
		print filename
		image_file='Images(Training)/B/'+ filename
		colordata = ProcessImage(image_file, partition_size)
		#webbrowser.open("pixels.png")
		#raw_input()
		dataset.addSample(colordata, (0, 1))
	
	dataset.saveToFile("dataset")



net = buildNetwork(partition_size*partition_size, 35, 8, 2)

epochs = int(raw_input("How many epochs do you want to train the network for?: "))

RunNet(net, dataset, epochs)

prompt = raw_input("Do you want to choose specific files?: ")

if (prompt == 'y'):
	while 1 == 1:
		file = raw_input("Filename: ")
		weights = ActivateNet(ProcessImage("Images(Unclassified)/" + file, partition_size))
		print weights[0], weights[1]
		#print ((math.fabs(1-weights)/weights)*100)

else:

	#remove previous matches
	for filename in os.listdir("Images(MatchA)"):
		os.remove('Images(MatchA)/' + filename)
	#remove previous non-matches
	for filename in os.listdir("Images(MatchB)"):
		os.remove('Images(MatchB)/' + filename)
		
	for filename in os.listdir("Images(Unclassified)"):
		weights= ActivateNet(ProcessImage("Images(Unclassified)/" + filename, partition_size))
		#weights=float(weights)
		diffA = math.fabs(weights[0]-1)
		diffB = math.fabs(weights[1]-1)
		#percent = math.fabs(((math.fabs(1-weights))/weights)*100)
		srcfile = "Images(Unclassified)/" + filename
		print "weights:", weights
		print "A:", diffA, "\nB:", diffB
		#raw_input()
		if (diffA <= diffB):
			print "Closer to A"
			shutil.copy(srcfile, "Images(MatchA)")
		else:
			print "Closer to B"
			shutil.copy(srcfile, "Images(MatchB)")

#webbrowser.open("pixels.png")
#print ProcessImage('Images(Classified)/blank.jpg', partition_size)