import os, sys, shutil
from geo2fds import geo2fds
from datetime import date





class backend:
    def __init__(self, saveName, lat, long, version="LF140", resolution=30,size=5,fire_points=[]):

        self.checkConus(lat,long)
        self.fire_points = fire_points

        # builds unique(ish) folder name system
        today = date.today()
        d2 = today.strftime("%Y-%m-%d-")
        self.title = d2+saveName.split('.')[0]

        if not os.path.isdir('data'):
            os.mkdir('data')
        os.chdir('data')

        if not os.path.isdir(self.title):
            os.mkdir (self.title)
        else:
            print("Directory already exists some files may be over written")
        os.chdir(self.title)

        #checks if image folder exists
        if not os.path.isdir('image'):
            os.mkdir ('image')

        self.filedir=os.path.join('image',saveName)

        # builds and runs curl command
        command = "curl -s -k \"https://aws.wfas.net/geoserver/ows?service=WPS&version=1.0.0&request=execute&identifier=gs:LandscapeExport&DataInputs=Longitude={};Latitude={};Version={};Resolution={};Extent={}&RawDataOutput=output\" -o {}"
        e = os.system(command.format(long,lat,version,resolution,size,self.filedir))

    # Checks values for latitude and longitude
    # https://en.wikipedia.org/wiki/List_of_extreme_points_of_the_United_States
    def checkConus(self,lat,long):
        top = 49.3457868  # north lat
        left = -124.7844079  # west long
        right = -66.9513812  # east long
        bottom = 24.7433195  # south lat

        #  Todo:fix lat and long comparison
        if top < float(lat) < bottom:
            quit()
        if right < float(long) < left:
            quit()


    def makeGeo(self,time=1):
        fdsFile = geo2fds(self.filedir,time,self.title,fire_points=self.fire_points)
        temp=fdsFile.make_fds(hrrpua=2500)
        self.filename = self.title+".fds"

        if not os.path.isdir('fds'):
            os.mkdir ('fds')
        path = os.path.join('fds',self.filename)
        try:
            with open(path,'w') as output_file:
                output_file.write(temp)
        except IOError as e:
            print("Write Error\n", e)


    # filename ~ path to fds file
    # fdscommand ~ basic mpi fds command
    #       Todo: Update -np 1 with number of meshes once mushes can be changed if needed
    # Returns name of compressed file
    def fdsRun(self):

        filename = os.path.join("fds",self.filename)
        fdscommand = "mpiexec -np 1  fds {}"

        #creates data folder if it doesnt exist, move to data folder
        # if not os.path.isdir('data'):
        #     os.mkdir('data')
        # os.chdir('data')
        # if not os.path.isdir(self.title):
        #     os.mkdir (self.title)
        # else:
        #     print("Directory already exists some files may be over written")

        # Changes to folder and runs fds command

        os.system(fdscommand.format(filename))

        # moves down one layer then compresses fds files.
        os.chdir('..')
        shutil.make_archive(self.title+"-compress",'zip',self.title)


        return self.title+"-compress.zip"

if __name__ == "__main__":
    #test data
    if len(sys.argv) == 1:
        lat,long =   46.72521515952037, -114.53272969666871
        filename="lolo-curl.tif"
    elif len(sys.argv) == 4:
        lat,long = float(sys.argv[1]),float(sys.argv[2])
        filename = sys.argv[3]+".tif"
    else:
        print("Please input 3 parameters latitude, longitude, and desired filename ")
    app = backend(filename,lat,long,fire_points=[[500,500],[600,600]])

    app.makeGeo()
    # app.fdsRun()

