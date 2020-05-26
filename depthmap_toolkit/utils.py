#convert point into 3D
def convert2Dto3D(intrisics, x, y, z):
  fx = intrisics[0] * float(width)
  fy = intrisics[1] * float(height)
  cx = intrisics[2] * float(width)
  cy = intrisics[3] * float(height)
  tx = (x - cx) * z / fx
  ty = (y - cy) * z / fy
  output = []
  output.append(tx)
  output.append(ty)
  output.append(z)
  return output

#convert point into 2D
def convert3Dto2D(intrisics, x, y, z):
  fx = intrisics[0] * float(width)
  fy = intrisics[1] * float(height)
  cx = intrisics[2] * float(width)
  cy = intrisics[3] * float(height)
  tx = x * fx / z + cx
  ty = y * fy / z + cy
  output = []
  output.append(tx)
  output.append(ty)
  output.append(z)
  return output

#write obj
def exportOBJ(filename):
  with open(filename, 'w') as file:
    for x in range(2, width - 2):
      for y in range(2, height - 2):
        depth = parseDepth(x, y)
        if depth:
         res = convert2Dto3D(calibration[1], x, y, depth)
         if res:
          file.write('v ' + str(res[0]) + ' ' + str(-res[2]) + ' ' + str(res[1]) + '\n')
    print('Pointcloud exported into ' + filename)
    file.close()

#write obj
def exportPCD(filename):
  with open(filename, 'w') as file:
    count = str(getCount())
    file.write('# timestamp 1 1 float 0\n');
    file.write('# .PCD v.7 - Point Cloud Data file format\n')
    file.write('VERSION .7\n')
    file.write('FIELDS x y z c\n')
    file.write('SIZE 4 4 4 4\n')
    file.write('TYPE F F F F\n')
    file.write('COUNT 1 1 1 1\n')
    file.write('WIDTH ' + count + '\n')
    file.write('HEIGHT 1\n')
    file.write('VIEWPOINT 0 0 0 1 0 0 0\n')
    file.write('POINTS ' + count + '\n')
    file.write('DATA ascii\n');
    for x in range(2, width - 2):
      for y in range(2, height - 2):
        depth = parseDepth(x, y)
        if depth:
          res = convert2Dto3D(calibration[1], x, y, depth)
          if res:
            file.write(str(-res[0]) + ' ' + str(res[1]) + ' ' + str(res[2]) + ' ' + str(parseConfidence(x, y)) + '\n')
    print('Pointcloud exported into ' + filename)
    file.close()

#get valid points in depthmaps
def getCount():
  count = 0
  for x in range(2, width - 2):
    for y in range(2, height - 2):
      depth = parseDepth(x, y)
      if depth:
        res = convert2Dto3D(calibration[1], x, y, depth)
        if res:
          count = count + 1
  return count

#getter
def getWidth():
  return width

#getter
def getHeight():
  return height

#parse calibration file
def parseCalibration(filepath):
  global calibration
  with open(filepath, 'r') as file:
    calibration = []
    file.readline()[:-1]
    calibration.append(parseNumbers(file.readline()))
    #print(str(calibration[0]) + '\n') #color camera intrinsics - fx, fy, cx, cy
    file.readline()[:-1]
    calibration.append(parseNumbers(file.readline()))
    #print(str(calibration[1]) + '\n') #depth camera intrinsics - fx, fy, cx, cy
    file.readline()[:-1]
    calibration.append(parseNumbers(file.readline()))
    #print(str(calibration[2]) + '\n') #depth camera position relativelly to color camera in meters
    calibration[2][1] *= 8.0  #workaround for wrong calibration data
  return calibration
    
#get confidence of the point in scale 0-1
def parseConfidence(tx, ty):
  return ord(data[(int(ty) * width + int(tx)) * 3 + 2]) / maxConfidence

#parse depth data
def parseData(filename):
  global width, height, depthScale, maxConfidence, data
  with open('data', 'rb') as file:
    line = str(file.readline())#[2:-3]
    header = line.split('_')
    res = header[0].split('x')
    width = int(res[0])
    height = int(res[1])
    depthScale = float(header[1])
    maxConfidence = float(header[2])
    data = file.read()
    file.close()

#get depth of the point in meters
def parseDepth(tx, ty):
  depth = ord(data[(int(ty) * width + int(tx)) * 3 + 0]) << 8
  depth += ord(data[(int(ty) * width + int(tx)) * 3 + 1])
  depth *= depthScale
  return depth

#parse line of numbers
def parseNumbers(line):
  output = []
  values = line.split(' ')
  for value in values:
    output.append(float(value))
  return output

#parse PCD
def parsePCD(filepath):
  with open(filepath, 'r') as file:
    data = []
    while 1:
      line = str(file.readline())
      if line.startswith('DATA'):
        break

    while 1:
      line = str(file.readline())
      if not line:
        break
      else:
        values = parseNumbers(line)
        data.append(values)
  return data

#parse line of values
def parseValues(line):
  output = []
  values = line.split(' ')
  for value in values:
    output.append(value)
  return output

#setter
def setWidth(value):
  global width
  width = value

#setter
def setHeight(value):
  global height
  height = value
