import rasterio
import math




class geo2fds:

    meta_info = ['width', 'height', 'count']


    def __init__(self, filename,time,title=''):
        self.raw_layers=[]
        self.file_name=filename
        self.time=time
        self.title=title

        with rasterio.open(filename) as dataset:
            # print(dataset.name)
            # print(dataset.indexes)
            self.meta_data = dataset.meta
            for i in dataset.indexes:
                self.raw_layers.append(dataset.read(i))
        self.distnace_calc()
        self.print_layers()


    def print_layers(self):
       for i in self.raw_layers[7]:
            print(i,'\n')

    #
    #     for k in dataset.meta:
    #         print(k, dataset.meta[k])
    #     print(dataset.meta['crs'])
    #
    #
    # for k in dataset.meta['crs']:
    #     print(k, dataset.meta['crs'][k])
    # min_elevation = dataset.read(1).min()
    #
    # print(len(dataset.read(1)[0]))

    def make_fds(self):
        # create file...

        job_name = filename.split('/')[-1].split('.')[0]

        outputStr = "&HEAD  CHID='{}', Title='{}' / \n".format(job_name,self.title)
        outputStr += "\n&TIME T_END={} /\n".format(self.time)
        outputStr += "\n&DUMP WRITE_XYZ=.TRUE., DT_PL3D=0.1 /\n"
        outputStr += "\n&MESH IJK={0},{1},100,".format(self.meta_data['width'],self.meta_data['height'])
        outputStr += "XB=0,{},0,{},{},{}/ \n".format(self.width_m_per_px*(self.meta_data['width']+1),self.length_m_per_px*(self.meta_data['height']+1),self.min_elevation,self.sky_elevation)


            # add the 3d terrain
        outputStr += self.landscape()


        outputStr += "\n&VENT MB='XMIN' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='XMAX' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='YMIN' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='YMAX' SURF_ID='OPEN' / \n"
        outputStr += "&VENT MB='ZMAX' SURF_ID='OPEN' / \n"


        outputStr += "\n&TAIL /"   #End of File

        return outputStr


    def landscape(self):
        output = '\n'
        obj = '&OBST XB= {0},{1},{2},{3},0,{5} /\n'
        print("Length{} Width {}".format (len(self.raw_layers[0]),len(self.raw_layers[0][0])))
        for i in range(len(self.raw_layers[0])):

            for j in range(len(self.raw_layers[0][i])):

                output += obj.format(i*self.width_m_per_px,(i+1)*self.width_m_per_px,j*self.length_m_per_px,(j+1)*self.length_m_per_px,self.min_elevation,self.raw_layers[0][i][j])
        return output


# Using the Haversine Formula
    def distnace_calc(self):
        for i in self.meta_data:
            print (i,self.meta_data[i])
        R = 637.3 # radious of earth in KM
        lat_1 = math.radians(self.meta_data['crs']['lat_1'])
        lat_2 = math.radians(self.meta_data['crs']['lat_2'])
        # lon_0 = math.radians(self.meta_data['crs']['lon_0'])

        delta_lat = lat_2 - lat_1

        a = math.sin(delta_lat/2)**2 + math.cos(lat_1)*math.cos(lat_2)*math.sin(0)**2
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        distance = R * c *100
        # print("Distance in KM ", distance )
        distance=round(distance*1000)
        self.size_m=distance
        self.width_m_per_px = round(distance/ self.meta_data['width'])
        self.length_m_per_px = round(distance/ self.meta_data['height'])
        self.min_elevation = self.raw_layers[0].min()
        self.max_elevation = self.raw_layers[0].max()
        self.sky_elevation= math.ceil(self.max_elevation/1000)*1000
        # print(self.length_m_per_px, "Height")
        # print(self.width_m_per_px, "Width")
        # print(self.sky_elevation, "Sky Height")


if __name__ =="__main__":
    filename = "LoLo.tif"
    title = "This is the Title "  # Todo: sys.arg maybeh?

    test = geo2fds(filename,1.0,title)


    # temp=test.make_fds()
    # try:
    #     with open(filename.split('.')[0]+'.fds','w') as output_file:
    #         output_file.write(temp)
    # except IOError as e:
    #     print("Write Error\n", e)
    #


