#!python3
# Tool to move a box around scans of tumours at multiple stages following treatment, plotting and saving a tumour regression curve to analyse the efficacy of treatment

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pydicom as dicom
import os
from os import listdir

#Specify folder of images
specified_folder = input('Please enter a folder path with dicom images to be analysed.')
count = 0
Areas_for_regression_curve = []
Labels_for_regression_curve = []

if os.path.isdir(specified_folder) == True:
	for image in os.listdir(specified_folder):
		if image.endswith('.dcm'):
			print('Processing: ', str(image))
			image_path = os.path.join(specified_folder, image)
			abc5 = dicom.read_file(image_path).pixel_array
			count+=1

			# Create new figure
			fig2 = plt.figure(2)
			ax = fig2.add_subplot(111)	# Add subplot
			thePlot = ax.imshow(abc5, cmap="Greys_r")	 # Display the input image


			# Create and move box co-ordianates to centre of the image
			origin = (abc5.shape[0]/2, abc5.shape[1]/2)
			rectParams = [origin[0], origin[1], 10, 10]


			# Draws the box inside the image
			rect = patches.Rectangle((rectParams[1], rectParams[0]),rectParams[2], rectParams[3], linewidth=2, edgecolor='r',facecolor='none')
			ax.add_patch(rect)
	
			# Initialise box position 
			global initPos
			initPos = None

			# Event handling functions for the box
			def onPress(event):
				"""
				This function is called when you click the mouse button inside the figure window, allowing movement of the box with the mouse.
				"""
				if event.inaxes == None:
					return	# Ignore clicks outside the axes
				contains = rect.contains(event)
				if not contains:
					return	# Ignore clicks outside the rectangle
		
				global initPos # Grab the global variable to update it
				initPos = [rect.get_x(), rect.get_y(), event.xdata, event.ydata]


			def onMove(event):
				"""
				This function is called when you move the mouse inside the figure window, with the left mouse button pressed down.
				"""
				if initPos is None:
					return	# If you haven't clicked recently, we ignore the event
				if event.inaxes == None:
					return	# ignore movement outside the axes
		
				# Defines values for movement of the box
				dx = event.xdata - initPos[2]
				dy = event.ydata - initPos[3]

				# Move the rectangle by dx and dy
				rect.set_x(initPos[0] + dx)
				rect.set_y(initPos[1] + dy)

				# Update the image of the rectangle
				rect.figure.canvas.draw()


			def onRelease(event):
				"""
				This function is called whenever a mouse button is released inside the figure window, releasing the box at the location specified.
				"""
				global initPos	# Grab the global variable to update it
				initPos = None	# Reset the position ready for next click
		

			# Reset the position ready for next click
			initPos = None
	
			def keyboardInterface(event):
				"""
				This function handles the keyboard interface. It is used to change the size of the
				box to fit around the tumour.
				"""
				if event.key == "right":
					# Make the rectangle wider
					w0 = rect.get_width()
					rect.set_width(w0 + 1)
				elif event.key == "left":
					# Make the rectangle narrower
					w0 = rect.get_width()
					rect.set_width(w0 - 1)
				elif event.key == "up":
					# Make the rectangle shorter
					h0 = rect.get_height()
					rect.set_height(h0 - 1)
				elif event.key == "down":
					# Make the rectangle taller
					h0 = rect.get_height()
					rect.set_height(h0 + 1)


			# Change box size by a factor of 10 with arrow keys.
				elif event.key == "ctrl+right":
					# Make the rectangle wider - faster x10
					w0 = rect.get_width()
					rect.set_width(w0 + 10)
				elif event.key == "ctrl+left":
					# Make the rectangle narrower - faster x10
					w0 = rect.get_width()
					rect.set_width(w0 - 10)
				elif event.key == "ctrl+up":
					# Make the rectangle shorter - faster x10
					h0 = rect.get_height()
					rect.set_height(h0 - 10)
				elif event.key == "ctrl+down":
					# Make the rectangle taller - faster x10
					h0 = rect.get_height()
					rect.set_height(h0 + 10)
		
				rect.figure.canvas.draw()# update the plot window
		
		
			#Connection of button press events
			cid1 = fig2.canvas.mpl_connect('button_press_event', onPress)
			cid2 = fig2.canvas.mpl_connect('motion_notify_event', onMove)
			cid3 = fig2.canvas.mpl_connect('button_release_event', onRelease)
			cid4 = fig2.canvas.mpl_connect('key_press_event', keyboardInterface)
		
			#Show plot
			plt.show()
				
			#Retrieve x,y max and min values, calculate area and print
			indices = [int(rect.get_y()), int(rect.get_y() + rect.get_height()), int(rect.get_x()), int(rect.get_x() + rect.get_width())]
			Box_area = abs((int(rect.get_y()) - int(rect.get_y() + rect.get_height())) * (int(rect.get_x() + rect.get_width()) - int(rect.get_x())))	#Note y axes is flipped, therefore 'yMax' is subtracted from 'yMin' in this case
			print("yMin, yMax, xMin, xMax = ", indices, "\n", "Area = ", Box_area, "R.U", "\n")

			#Generate list for regression curve areas and list for labels

			Areas_for_regression_curve.append(Box_area)
			Labels_for_regression_curve.append(image)
else:
	print('The folder path provided does not exist. Please run the script again and re-enter the folder path.')

# Tells user number of images processed.
print('You have processed', count, ' images.')
print(Labels_for_regression_curve, Areas_for_regression_curve)

# Plot the graph.
plt.plot(Labels_for_regression_curve, Areas_for_regression_curve)
plt.ylabel('Tumour area (R.U)', fontsize=12)
plt.title('Tumour area over time')
plt.show()
plt.savefig(os.path.join(specified_folder,'tumour_regression_curve.png'))

# TODO: Save figure to folder with images for later viewing