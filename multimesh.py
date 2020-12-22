import math
class multiMesh:

    def __init__(self):
        print("Inputs:")
        self.IJK = input("single mesh equivalent IJK,\n\t exp: 221,221,241\n IJK = ").split(',')
        self.XB = input("single mesh equivalent XB,\n\t  exp: -1,1,-1.5,1.5,-1.5,-3\n XB = ").split(',')
        self.MBLKS = input("mesh block arrangment,\n\t      exp: 5,5,5 \n Mesh Blocks = ").split(',')

        self.IJK = [int(x) for x in self.IJK]
        self.XB = [int(x) for x in self.XB]
        self.MBLKS = [int(x) for x in self.MBLKS]

    def __init__(self,XB,IJK,MBLKS):
        self.XB=XB
        self.IJK=IJK
        self.MBLKS=MBLKS



    def inputCheck(self):
        assert len(self.IJK) == 3
        assert len(self.XB) == 6
        assert len(self.MBLKS) == 3

        for i in range(3):
            if self.IJK[i]<1:
                print("IJK values need to be positive")
                quit()
            if self.MBLKS[i]<1:
                print("Mesh Block values need to be positive")
                quit()
            if self.XB[i*2]>self.XB[i*2+1]:
                print("XB values need to be increasing IE: x2 needs to be bigger then x1")
                quit()

    def meshGen(self):
        self.inputCheck()
        MULT_obj = "&MULT ID=\"m1\",DX={}, DY={}, DZ={}, I_UPPER={}, J_UPPER={}, K_UPPER={} /"
        MESH_obj = "&MESH IJK={}, {}, {}, XB={}, {}, {}, {}, {}, {}, MULT_ID=\"m1\" / {} Mesh "
        # delta x value
        D_X = (self.XB[1]-self.XB[0])/self.MBLKS[0]
        D_Y = (self.XB[3]-self.XB[2])/self.MBLKS[1]
        D_Z = (self.XB[5]-self.XB[4])/self.MBLKS[2]

        # IJK Upper values
        I_U, J_U, K_U = [x - 1 for x in self.MBLKS]

        I = math.ceil(self.IJK[0]/self.MBLKS[0])
        J = math.ceil(self.IJK[1]/self.MBLKS[1])
        K = math.ceil(self.IJK[2]/self.MBLKS[2])

        X_0 = self.XB[0]
        X_1 = X_0 + D_X
        Y_0 = self.XB[2]
        Y_1 = Y_0 + D_Y
        Z_0 = self.XB[4]
        Z_1 = Z_0 + D_Z
        num_mesh = self.MBLKS[0]*self.MBLKS[1]*self.MBLKS[2]

        MULT = MULT_obj.format(D_X,D_Y,D_Z,I_U,J_U,K_U)
        MESH = MESH_obj.format(I,J,K,X_0,X_1 ,Y_0,Y_1, Z_0,Z_1, num_mesh)
        return MULT,MESH


if __name__ =='__main__':
    temp = multiMesh()
    mult , mesh = temp.meshGen()
    print(mult)
    print(mesh)