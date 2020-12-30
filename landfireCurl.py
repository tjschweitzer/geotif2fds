import os, sys, shutil
from geo2fds import geo2fds
from datetime import date





class backend:
    def __init__(self,saveName,lat,long,version="LF140", resolution=30,size=5):
        today = date.today()
        d2 = today.strftime("%Y-%m-%d-")

        self.title=d2+saveName.split('.')[0]
        self.filedir="image/"+saveName
        command = "curl -s -k \"https://aws.wfas.net/geoserver/ows?service=WPS&version=1.0.0&request=execute&identifier=gs:LandscapeExport&DataInputs=Longitude={};Latitude={};Version={};Resolution={};Extent={}&RawDataOutput=output\" -o {}"
        e = os.system(command.format(long,lat,version,resolution,size,self.filedir))
        print(e)
        print("Curl Complete")

    def makeGeo(self,time=1):
        fdsFile = geo2fds(self.filedir,time,4,self.title)


        temp=fdsFile.make_fds(hrrpua=2500)
        self.filename = self.filedir.split("/")[-1]
        if not os.path.isdir('fds'):
            os.mkdir ('fds')
        path = os.path.join('fds',self.filename.split('.')[0]+'.fds')
        try:
            with open(path,'w') as output_file:
                output_file.write(temp)
        except IOError as e:
            print("Write Error\n", e)

    def fdsRun(self):
        filename=self.filename.split('.')[0]
        path = os.path.join("..", "fds")
        path = os.path.join("..", path)
        filename = os.path.join(path,filename)
        fdscommand = "mpiexec -np 1  fds {}.fds"

        #creates data folder if it doesnt exist, move to data folder
        if not os.path.isdir('data'):
            os.mkdir('data')
        os.chdir('data')


        if not os.path.isdir(self.title):
            os.mkdir (self.title)
        else:
            print("Directory already exists some files may be over written")

        os.chdir(self.title)
        os.system(fdscommand.format(filename))
        print(os.getcwd())
        os.chdir('..')

        shutil.make_archive(self.title+"-compress",'zip',self.title)
        # os.system("smokeview {}".format(self.filename.split('.')[0]+".smv"))
        return self.title+"compress.zip"

if __name__ == "__main__":
    #test data
    if len(sys.argv) == 1:
        lat,long =   46.72521515952037, -114.53272969666871
        filename="lolo-curl.tif"
    elif len(sys.argv) == 4:
        lat,long = float(sys.argv[1]),float(sys.argv[2])
        filename = sys.argv[3]+".tif"
    else:
        print("Please input 3 parameters latitude, longitude, and510 desired filename ")
    app = backend(filename,lat,long)
    app.makeGeo()
    app.fdsRun()