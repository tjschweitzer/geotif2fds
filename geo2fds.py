import rasterio, os
import numpy as np
import multimesh

class geo2fds:

    """
    filename = filename for 8 band geotiff from landfire
        1 	Elevation 	DEM
        2 	Slope 	SLP
        3 	Aspect 	ASP
        4 	Fuel model 	FBFM40
        5 	Forest Canopy Cover 	CC
        6 	Forest Canopy Height 	CH
        7 	Forest Canopy Base Height 	CBH
        8 	Forest Canopy Bulk Density 	CBD
    time = duration of fds simulation
    title = title of fds job
    fire_points = a 2d array of xy points of ignition points
    """
    def __init__(self, filename,time,title='',fire_points=[]):
        self.FmDict = {
            91: [0, "Urban"],
            92: [0, "Snow/Ice"],
            93: [0, "Agriculture"],
            98: [0, "Water"],
            99: [0, "Barren"],
            101: [1, "GR1"],
            102: [2, "GR2"],
            103: [3, "GR3"],
            104: [2, "GR4"],
            105: [3, "GR5"],
            106: [3, "GR6"],
            107: [3, "GR7"],
            108: [3, "GR8"],
            109: [3, "GR9"],
            121: [2, "GS1"],
            122: [2, "GS2"],
            123: [2, "GS3"],
            124: [3, "GS4"],
            141: [6, "SH1"],
            142: [5, "SH2"],
            143: [7, "SH3"],
            144: [7, "SH4"],
            145: [4, "SH5"],
            146: [7, "SH6"],
            147: [5, "SH7"],
            148: [7, "SH8"],
            149: [7, "SH9"],
            161: [8, "TU1"],
            162: [10, "TU2"],
            163: [10, "TU3"],
            164: [10, "TU4"],
            165: [5, "TU5"],
            181: [8, "TL1"],
            182: [9, "TL2"],
            183: [8, "TL3"],
            184: [8, "TL4"],
            185: [8, "TL5"],
            186: [9, "TL6"],
            187: [8, "TL7"],
            188: [9, "TL8"],
            189: [9, "TL9"],
            201: [11, "SB1"],
            202: [12, "SB2"],
            203: [12, "SB3"],
            204: [13, "SB4"],
            -9999:[0, "Barren"],
        }
        self.file_name=filename
        self.time=time
        self.title=title
        self.fire_points = fire_points

        self.dataset = rasterio.open(filename)
        self.topo()

    """
    DEM = elevation of each index value
    FM40 = FBFM40 fuel model value
    horz = change in x per index
    vert = change in y per index
    xLR,yLR = x and y coordinates for lower right corner of the index
    xUL,yUL = x and y coordinates for lower right corner of the index
    zMin = min elevation
    zMax = max elevation 
    x,y = number of indexes in the x and y
    """
    def topo(self):
        DEM=self.dataset.read(1)
        FM40= self.dataset.read(4)
        print(self.dataset.transform)
        horz=self.dataset.transform[0]
        vert= self.dataset.transform[4]
        xLR,yLR =self.dataset.transform * (self.dataset.width, self.dataset.height)
        xUL,yUL= self.dataset.transform * (0,0)
        zMin= np.min(DEM)
        zMax=np.max(DEM)

        x,y = DEM.shape
        z=zMax-zMin//x


        horz=round(horz)
        vert= round(vert)
        xLR, yLR = round(xLR),round(yLR)
        xUL, yUL = round(xUL),round(yUL)
        zMin = round(zMin)
        zMax = round(zMax)+50

        # Todo: fix multi mesh
        # creates the multimesh
        # xMesh = multimesh.multiMesh([  yLR,yUL,xUL, xLR,zMin,zMax],[50,50,50],[1,1,1])
        # mesh, mult =xMesh.meshGen()
        #
        # self.allObst = [mesh,mult]
        self.allObst= ["&MESH IJK=100, 100, 100, XB={},{},{},{},{},{}/".format(xUL,xLR,yLR,yUL,zMin,zMax)]
        obst = "&OBST XB= {},{},{},{},{},{},  SURF_ID='{}'/ "
        vent = "&VENT XB= {},{},{},{},{},{},  SURF_ID='{}'/ "

        counter = 0
        for i in FM40:
            for j in i:
                if j <0:
                    counter+=1
        print(counter)

        for row in range(x):
            for col in range(y):
                # id = self.FmDict[FM40[row,col]][-1]
                sID =self.FmDict[FM40[row,col]][0]

                self.allObst.append(obst.format(xUL+(row*horz), xUL+((row+1)*horz),yUL+(col*vert),yUL+((col+1)*vert),zMin,DEM[row,col],sID))

                self.allObst.append(vent.format(xUL+(row*horz), xUL+((row+1)*horz),yUL+(col*vert),yUL+((col+1)*vert),DEM[row,col],DEM[row,col],sID))


    """
    For Point Fire
    fireOut = timeframe for when fire starts and ends
    """
    def fire(self,hrrpua,tStart, tEnd):
        assert tStart<tEnd
        fireOut = "&SURF ID='IGN FIRE', HRRPUA = {}, COLOR = 'RED', RAMP_Q = 'fire' /\n" \
                  "&RAMP ID='fire', T=0, F=0. /\n" \
                  "&RAMP ID='fire', T={}, F=1. /\n" \
                  "&RAMP ID='fire', T={}, F=1. /\n"\
                  "&RAMP ID='fire', T={}, F=0. /\n".format(hrrpua,tStart,tEnd,tEnd+1)
        for fire in self.fire_points:
            print(fire)
            xFire,yFire = fire
            x, y = (self.dataset.bounds.left + float(xFire), self.dataset.bounds.top - float(yFire))
            row, col = self.dataset.index(x, y)
            # print(row, col,x,y)
            z=self.dataset.read(1)[row,col]
            fireOut  += "&OBST XB={},{},{},{},{},{},SURF_ID = 'IGN FIRE' /\n".format(x,x+50,y,y+50,z,z+1)

        return fireOut

    # Todo Add line fire

    # Todo update FM13 to 40
    def fueldata(self):
        fuelOut = "&SURF ID='1', VEG_LSET_FUEL_INDEX=1, RGB=255,254,222/\n" \
                  "&SURF ID='2', VEG_LSET_FUEL_INDEX=2, RGB=255,253,102/\n" \
                  "&SURF ID='3',  VEG_LSET_FUEL_INDEX=3, RGB= 236,212,99/\n" \
                  "&SURF ID='4',  VEG_LSET_FUEL_INDEX=4, RGB=254,193,119/\n" \
                  "&SURF ID='5', VEG_LSET_FUEL_INDEX=5, RGB=249, 197, 92/\n" \
                  "&SURF ID='6',  VEG_LSET_FUEL_INDEX=6, RGB=217, 196, 152/\n" \
                  "&SURF ID='7',  VEG_LSET_FUEL_INDEX=7, RGB=170, 155, 127/\n" \
                  "&SURF ID='8',  VEG_LSET_FUEL_INDEX=8, RGB=229, 253, 214/\n" \
                  "&SURF ID='9',  VEG_LSET_FUEL_INDEX=9, RGB=162, 191, 90/\n" \
                  "&SURF ID='10', VEG_LSET_FUEL_INDEX=10, RGB=162, 191, 90/\n" \
                  "&SURF ID='11',  VEG_LSET_FUEL_INDEX=11, RGB=235, 212, 253/\n" \
                  "&SURF ID='12',  VEG_LSET_FUEL_INDEX=12, RGB=148,212,116/\n" \
                  "&SURF ID='13',  VEG_LSET_FUEL_INDEX=13, RGB=88,212,102/\n" \
                  "&SURF ID='0',  RGB=186, 119, 80/\n"


        return fuelOut



    def make_fds(self,hrrpua=500,tStart =1, tEnd=60):
        # create file...

        job_name = self.file_name.split('/')[-1].split('.')[0]

        outputStr = "&HEAD  CHID='{}', Title='{}' / \n".format(job_name,self.title)
        outputStr += "\n&TIME T_END={} /\n".format(self.time)
        outputStr += "\n&DUMP WRITE_XYZ=.TRUE., DT_PL3D=0.1 /\n"
        outputStr += "&REAC FUEL='CELLULOSE', C=6, H=10, O=5, SOOT_YIELD=0.01, HEAT_OF_COMBUSTION=18607. /\n"
        outputStr += "&MISC LEVEL_SET_MODE=4 /\n"

        outputStr += "\n&VENT MB='XMIN' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='XMAX' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='YMIN' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='YMAX' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='ZMAX' SURF_ID='OPEN' / \n\n\n"


        outputStr += self.fueldata()

        outputStr+= self.fire(hrrpua,tStart, tEnd)

        for line in self.allObst:
            outputStr += line +"\n"

        outputStr += "\n&TAIL /"   #End of File

        return outputStr

if __name__ =="__main__":
    filename = "image/output.tif"
    title = "This is the Title "  # Todo: sys.arg maybeh?
    test = geo2fds(filename,1.0,title)
    temp=test.make_fds()
    try:
        with open(filename.split('.')[0]+'.fds','w') as output_file:
            output_file.write(temp)
    except IOError as e:
        print("Write Error\n", e)



