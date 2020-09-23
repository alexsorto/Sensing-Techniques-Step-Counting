import numpy as np
import matplotlib.pyplot as plt
from csv import reader

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
#TODO Read the measurements into array variables and return them
def read_data(filename):
  #TODO implementation
  timestampArr = []
  xArr = []
  yArr = []
  zArr = []


  with open(filename, 'r') as accelRaws:
    accelReader = reader(accelRaws)

    for row in accelReader:
      timestampArr.append(row[0])
      xArr.append(row[1])
      yArr.append(row[2])
      zArr.append(row[3])

  return timestampArr, xArr, yArr, zArr

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr):
  #TODO: Actual implementation
  rv = []
  
#Variables used to track limits and tresholds, plus some used to plot the data.
  xMax = 0
  xMin = 0
  xTrshld = 0

  xTrs = []
  xCurrs = []
  mTrs = []

  xCurrent = 0
#Used to ignore drops that are too sensible. Drops below treshold that do not surpass the margin, are not counted as steps 
  decreaseMargin = 1

  declineCounter = 0
  inclined = True
  declined = False

  samplingPoints = []
  itr = 0
  toProcessAmnt = len(timestamps)

  while(itr < toProcessAmnt):
    
    xCurrent = float(x_arr[itr])

    if(xMax == 0):
      xMax = xCurrent
      xMin = xCurrent 

    if(xCurrent > xMax):
      xMax = xCurrent

    if(xCurrent < xMin):
      xMin = xCurrent

#If treshold is not set yet then wait for it to be generated. When the acceleration drops below, the treshold (minus the decreaseMargin) it is recorded as ONE step.
#Another step can only happen when the acceleration climbs past the treshold and falls down again
    if(xTrshld != 0):
      if((xCurrent < (xTrshld - decreaseMargin)) and (declined == False) and (inclined == True)):
        declined = True
        inclined = False
        print("Current point " + str(xCurrent) + " is LOWER than Treshold " + str(xTrshld))
        print("Decline")

      if((xCurrent > xTrshld) and (inclined != True) and (declined == False)):
        inclined = True
        print("Current point " + str(xCurrent) + " is HIGHER than Treshold " + str(xTrshld))
        print("Incline")

#Treshold is updated at this point, every 50 readings
    if(itr % 50 == 0):

      xTPrev = xTrshld
      xTrshld = (xMax + xMin) / 2
        
      print(itr)
      print("Treshold UPDATED to " + str(xTrshld))

      xMax = 0
      xMin = 0


#If a decline is detected then it is reported as one step.
    if((declined == True)):
      declineCounter += 1
      rv.append(str(itr))
      declined = False
      print("Writing decline " + str(declineCounter) + "at index" + str(len(rv)))
    else:
      print("No step detected")

#Plotting some lines to visualize the data along with their treshold values
    samplingPoints.append(itr)
    xTrs.append(xTrshld)
    xCurrs.append(xCurrent)

    itr = itr + 1
  
  plt.figure(3)
  plt.plot(samplingPoints, xTrs, color = "blue",linewidth=1.0)
  plt.plot(samplingPoints, xCurrs, color = "red",linewidth=1.0)

  plt.show()

  return rv

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 50000 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main():
  #read data from a measurement file, change the inoput file name if needed
  timestamps, x_array, y_array, z_array = read_data("out.csv")
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  st = count_steps(timestamps, x_array, y_array, z_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array)

main()

