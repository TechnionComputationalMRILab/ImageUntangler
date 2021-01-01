import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator, BSpline, Rbf, interp2d, griddata,splprep,splev
import vtk
from vtk.util import numpy_support

class PointsToPlansVectors():
    def __init__(self, viewerLogic, ListOfPoints, ViewMode, Height = 10, viewAngle = 0,Plot = 0):
        self.Plot = Plot
        self.Height = Height
        self.viewAngle = viewAngle

        if ViewMode == 'Coronal':
            V = np.asarray(viewerLogic.CoronalArrayDicom)

            ##
            self.V = V
            ##
            V_origin = np.asarray(viewerLogic.CoronalVTKOrigin)
            V_spacing = np.asarray(viewerLogic.CoronalVTKSpacing)
            V_dim = np.asarray(viewerLogic.CoronalDimensions)

            # self.x = np.arange(V_origin[0],V_origin[0]+V_dim[0]*V_spacing[0], V_spacing[0])
            # self.y = np.arange(V_origin[1],V_origin[1]+V_dim[1]*V_spacing[1], V_spacing[1])
            # self.z = np.arange(V_origin[2], V_origin[2] + V_dim[2] * V_spacing[2], V_spacing[2])
            # self.x = np.arange(-V_dim[0] * V_spacing[0] / 2, V_dim[0] * V_spacing[0] / 2, V_spacing[0])
            # self.y = np.arange(-V_dim[1] * V_spacing[1] / 2, V_dim[1] * V_spacing[1] / 2, V_spacing[1])
            # self.z = np.arange(-V_dim[2] * V_spacing[2] / 2, V_dim[2] * V_spacing[2] / 2, V_spacing[2])
            # self.x = np.linspace(V_origin[0], V_origin[0] + (V_dim[0] - 1) * V_spacing[0], V_dim[0])
            # self.y = np.linspace(V_origin[1], V_origin[1] + (V_dim[1] - 1) * V_spacing[1], V_dim[1])
            # self.z = np.linspace(V_origin[2], V_origin[2] + (V_dim[2] - 1) * V_spacing[2], V_dim[2])
            self.x = np.linspace(-V_dim[0] * V_spacing[0] / 2, (V_dim[0] ) * V_spacing[0]/2, V_dim[0])
            self.y = np.linspace(-V_dim[1] * V_spacing[1] / 2, (V_dim[1] ) * V_spacing[1]/2, V_dim[1])
            self.z = np.linspace(-V_dim[2] * V_spacing[2] / 2, (V_dim[2] ) * V_spacing[2]/2, V_dim[2])
            # self.x = np.linspace(-(V_dim[0]-1) * V_spacing[0] / 2, (V_dim[0]-1 ) * V_spacing[0]/2, V_dim[0])
            # self.y = np.linspace(-(V_dim[1]-1) * V_spacing[1] / 2, (V_dim[1]-1 ) * V_spacing[1]/2, V_dim[1])
            # self.z = np.linspace(-(V_dim[2]-1) * V_spacing[2] / 2, (V_dim[2]-1 ) * V_spacing[2]/2, V_dim[2])
            # if
        #my_interpolating_function = interpulation3d(x, y, z, V)
        self.delta = V_spacing[0]

        Pts = np.asarray(ListOfPoints)
        self.Org_points = Pts
        ListOfPoints = self.Org_points[:, 0:3]
        # self.LinearVTKlist = self.LinearCenterLine(ListOfPoints)
        Linear = self.LinearCenterLine(ListOfPoints, self.delta*2)
        x = np.squeeze(ListOfPoints[:, 0])
        y = np.squeeze(ListOfPoints[:, 1])
        z = np.squeeze(ListOfPoints[:, 2])
        if self.Plot:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(x, y, z,'-ob')

            plt.show()

        # f = interp2d(x, y, z, kind='cubic')
        # rbfi = Rbf(x, y, z,'cubic')
        # zi = rbfi(np.squeeze(Linear[:, 0]), np.squeeze(Linear[:, 1]))
        # self.LinearVTKlist = np.array(np.squeeze(Linear[:, 0]),np.squeeze(Linear[:, 1]),zi)
        # self.LinearVTKlist = f(np.squeeze(Linear[:, 0]),np.squeeze(Linear[:, 1]))
        self.LinearVTKlist = self.bspline(ListOfPoints,self.delta,degree=2)
        # self.LinearVTKlist = self.LinearCenterLine(ListOfPoints,self.delta)
        self.FindVectors()
        self.getStraightMPRVector(self.x, self.y, self.z, V)

    def LinearCenterLine(self, ListOfPoints,delta):
        # ListOfPoints = self.Org_points[:, 0:3]
        LinearVTKlist = np.zeros([1, 3])
        for i in range(1, ListOfPoints.shape[0]):
            Vector = ListOfPoints[i] - ListOfPoints[i - 1]
            point = ListOfPoints[i - 1]
            LinearVTKlist = np.append(LinearVTKlist, [point], axis=0)
            dist = np.linalg.norm(ListOfPoints[i] - point)
            while dist > delta:
                point = point + (delta / np.linalg.norm(Vector)) * Vector
                LinearVTKlist = np.append(LinearVTKlist, [point], axis=0)
                dist = np.linalg.norm(ListOfPoints[i] - point)
            ListOfPoints[i] = point + (delta / np.linalg.norm(Vector)) * Vector
        LinearVTKlist = np.append(LinearVTKlist, [ListOfPoints[i]], axis=0)
        LinearVTKlist = LinearVTKlist[1:]
        return LinearVTKlist
        # self.LinearVTKlist = LinearVTKlist

    # def LinearCenterLine2(self, ListOfPoints, delta):
    #     LinearVTKlist = np.zeros([1, 3])
    #     for i in range(1, ListOfPoints.shape[0]):

    def bspline(self, ListOfPoints, delta, n=100, degree=3, ):
        """ Calculate n samples on a bspline

            cv :      Array ov control vertices
            n  :      Number of samples to return
            degree:   Curve degree
        """
        x = np.squeeze(ListOfPoints[:, 0])
        y = np.squeeze(ListOfPoints[:, 1])
        z = np.squeeze(ListOfPoints[:, 2])
        dist =0
        for i in range(len(ListOfPoints)-1):
            dist += np.linalg.norm(ListOfPoints[i+1]-ListOfPoints[i])
        n = np.int(round(dist/delta))

        tck, u = splprep([x, y, z], s=2)
        x_knots, y_knots, z_knots = splev(tck[0], tck)
        u_fine = np.linspace(0, 1, n)
        x_fine, y_fine, z_fine = splev(u_fine, tck)
        B = np.array([x_fine, y_fine, z_fine])
        B = B.T

        if self.Plot:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(ListOfPoints[:, 0], ListOfPoints[:, 1], ListOfPoints[:, 2],'-ob')
            # ax.plot(xline, yline, zline, '-og')
            ax.plot(x_fine, y_fine, z_fine,'-*r')
            # ax.plot(L[:,0], L[:,1], L[:,2], '-*b')
            # ax.plot(np.squeeze(Linear[:, 0]),np.squeeze(Linear[:, 1]),np.squeeze(Linear[:, 2]))

            plt.show()

        return B
    def FindVectors(self):
        ListOfPoints = self.LinearVTKlist
        Vector1_list = []
        Vector2_list = []
        xline = np.squeeze(ListOfPoints[:, 0])
        yline = np.squeeze(ListOfPoints[:, 1])
        zline = np.squeeze(ListOfPoints[:, 2])
        if self.Plot:
            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            # ax.plot3D(xline, yline, zline, '-og')
            # # ax.scatter(xline, yline, zline)

            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111, projection='3d')
            ax2.plot3D(xline, yline, zline, 'gray')

        Angle_1_2 = []
        Angle_1_teta = []
        Angle_2_teta = []
        for i in range(0, zline.size-1):
            NormalDirection = np.array([xline[i + 1] - xline[i], yline[i + 1] - yline[i], zline[i + 1] - zline[i]])
            Vector1 = np.array([-NormalDirection[1], NormalDirection[0], 0])
            Vector2 = np.cross(Vector1, NormalDirection)
            # Normolize vectors:
            Vector1 = Vector1/np.linalg.norm(Vector1)
            Vector2 = Vector2 / np.linalg.norm(Vector2)
            NormalDirection = NormalDirection/np.linalg.norm(NormalDirection)
            Vector1_list.append(Vector1)
            Vector2_list.append(Vector2)
            viewAngle = self.viewAngle
            viewAngleRad = np.deg2rad(viewAngle)
            Vector_teta = Vector1 * np.cos(viewAngleRad) + Vector2 * np.sin(viewAngleRad)

            Dot1_2 = np.dot(Vector1, Vector2) if abs(np.dot(Vector1, Vector2))<=1 else np.sign(np.dot(Vector1, Vector2))
            Angle_1_2.append(np.arccos(Dot1_2))
            Dot1_teta = np.dot(Vector1, Vector_teta) if abs(np.dot(Vector1, Vector_teta))<=1 else np.sign(np.dot(Vector1, Vector_teta))
            Angle_1_teta.append(np.arccos(Dot1_teta))
            Dot2_teta = np.dot(Vector2, Vector_teta) if abs(np.dot(Vector2, Vector_teta))<=1 else np.sign(np.dot(Vector2, Vector_teta))
            Angle_2_teta.append(np.arccos(Dot2_teta))
            if self.Plot:
                # #ax.quiver(xline[i], yline[i], zline[i], NormalDirection[0], NormalDirection[1], NormalDirection[2] , normalize=True, colors='b')
                # ax.quiver(xline[i], yline[i], zline[i], Vector1[0], Vector1[1], Vector1[2],  colors='g',length=0.5, normalize=True)
                # ax.quiver(xline[i], yline[i], zline[i], Vector2[0], Vector2[1], Vector2[2],colors='r',length=0.01, normalize=True)
                # ax.quiver(xline[i], yline[i], zline[i], Vector_teta[0], Vector_teta[1], Vector_teta[2],colors='b',length=0.01, normalize=True)

                ax2.plot3D([xline[i], xline[i] + Vector1[0]], [yline[i], yline[i] + Vector1[1]], [zline[i], zline[i] + Vector1[2]], color='g')
                ax2.plot3D([xline[i], xline[i] + Vector2[0]], [yline[i], yline[i] + Vector2[1]], [zline[i], zline[i] + Vector2[2]], color='r')
                ax2.plot3D([xline[i], xline[i] + Vector_teta[0]], [yline[i], yline[i] + Vector_teta[1]], [zline[i], zline[i] + Vector_teta[2]], color='b')

        Angle_1_2= np.asarray(np.rad2deg(Angle_1_2))
        Angle_1_teta = np.asarray(np.rad2deg(Angle_1_teta))
        Angle_2_teta = np.asarray(np.rad2deg(Angle_2_teta))
        if self.Plot:
            # plt.gca().set_aspect('equal', adjustable='box')
            plt.show()

            fig, ax = plt.subplots()
            ax.plot(Angle_1_2, label = "Vector1_Vector2")
            ax.plot(Angle_1_teta, label = "Vector1_VectorTheta")
            ax.plot(Angle_2_teta, label = "VectorTheta_Vector2")
            ax.legend()
            plt.show()
        #Add vectors to arrays


        self.Vector1_list = np.asarray(Vector1_list)
        self.Vector2_list = np.asarray(Vector2_list)

    def interpulation3d(self,x, y, z, V):
        my_interpolating_function = RegularGridInterpolator((x, y, z), V, method='linear')
        return my_interpolating_function

    def getStraightMPRVector(self, x, y, z, V):
        # Heigth in cm, Angle in deg
        Vector1 = self.Vector1_list
        Vector2 = self.Vector2_list
        points = self.LinearVTKlist
        org_points = self.Org_points
        Delta = self.delta
        Height = self.Height
        viewAngle = self.viewAngle
        viewAngleRad = np.deg2rad(viewAngle)
        size_y = np.int16(np.round(Height / Delta))+1
        size_x = len(Vector1)
        Vector_teta = Vector1 * np.cos(viewAngleRad) + Vector2 * np.sin(viewAngleRad)
        # temp:
        Ponits_x = np.squeeze(org_points[:, 0])
        Ponits_y = np.squeeze(org_points[:, 1])
        Ponits_z = np.squeeze(org_points[:, 2])
        Pointz_zslice = np.squeeze(org_points[:, 3])

        self.Pointz_zslice = Pointz_zslice

        Num = Height // Delta
        Heigth = Num * Delta
        MPR_indexs = []
        for i in range(0, size_x):
            Center_point = points[i]
            Column_Vector = Vector_teta[i]
            Column_Vector_norm = Vector_teta[i]/np.linalg.norm(Column_Vector)

            point_start = Center_point - (Heigth/2)*Column_Vector_norm
            point_stop = Center_point + (Heigth/2)*Column_Vector_norm

            [Column_MPR_old,step] = np.linspace(point_start, point_stop, num=np.int16(Num), retstep =True)
            Column_MPR_x = np.arange(0, Num + 1) * Delta * Column_Vector_norm[0] + point_start[0]
            Column_MPR_y = np.arange(0, Num + 1) * Delta * Column_Vector_norm[1] + point_start[1]
            Column_MPR_z = np.arange(0, Num + 1) * Delta * Column_Vector_norm[2] + point_start[2]
            Column_MPR = np.stack((Column_MPR_x, Column_MPR_y, Column_MPR_z)).T
            size_y = Column_MPR.shape[0]
            MPR_indexs.append(Column_MPR)



        MPR_indexs_np = np.asarray(MPR_indexs)
        print(MPR_indexs_np[0:4,0:4,:])
        Line_x = np.squeeze(MPR_indexs_np[:, :, 0]).reshape(size_x * size_y)
        Line_y = np.squeeze(MPR_indexs_np[:, :, 1]).reshape(size_x * size_y)
        Line_z = np.squeeze(MPR_indexs_np[:, :, 2]).reshape(size_x * size_y)



        if self.Plot:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            z_list= np.sort(np.unique(np.round(Ponits_z,2)))
            for j in z_list:
                I = (np.abs(z - j)).argmin()
                X, Y = np.meshgrid(x, y)
                plan = np.squeeze(np.transpose(V[:, :, I]))
                ax.contourf(X, Y, plan, zdir='z', offset=z[I])

            ax.scatter(Line_x, Line_y, Line_z, c='b')
            ax.plot(Line_x,Line_y,Line_z,c='gray')
            ax.scatter(points[:,0], points[:,1], points[:,2],c='g')
            ax.scatter(Ponits_x,Ponits_y,Ponits_z, c='b')
            # ax.set_zlim(z_list[0] , z_list[-1] )
            plt.show()

            I = (np.abs(z - z_list[0])).argmin()
            plan2 =np.squeeze(np.transpose(V[:, :, I]))
            fig, ax1 = plt.subplots()
            # ax1.imshow(plan2, origin='upper', extent=[x.min(), x.max(), y.min(), y.max()])
            ax1.imshow(plan2,origin='upper', extent=[x.min(), x.max(), y.min(), y.max()])
            ax1.scatter(Line_x, Line_y, c='b')
            ax1.scatter(points[:,0], points[:,1], c='g')
            ax1.scatter(Ponits_x, Ponits_y, c='r')
            plt.show()

        X_dis = []
        Y_dis = []
        for i in range(MPR_indexs_np.shape[0] - 1):
            x_i = []
            y_i = []
            for j in range(MPR_indexs_np.shape[1] - 1):
                D_j = np.linalg.norm(MPR_indexs_np[i, j, :] - MPR_indexs_np[i, j + 1, :])
                x_i.append(D_j)
                D_i = np.linalg.norm(MPR_indexs_np[i, j, :] - MPR_indexs_np[i + 1, j, :])
                y_i.append(D_i)
            X_dis.append(x_i)
            Y_dis.append(y_i)
        X_dis = np.asarray(X_dis)
        Y_dis = np.asarray(Y_dis)

        V = np.flip(V, 1)
        my_interpolating_function = self.interpulation3d(x, y, z, V)
        MPR_indexs_np_reshape = np.reshape(MPR_indexs_np, (MPR_indexs_np.shape[0] * MPR_indexs_np.shape[1], 3))
        MPR_M = my_interpolating_function(MPR_indexs_np_reshape)
        print(MPR_M.shape)
        self.MPR_M = np.reshape(MPR_M, (MPR_indexs_np.shape[0], MPR_indexs_np.shape[1]))
        print(MPR_M.shape)

        # self.MPR_M = my_interpolating_function(MPR_indexs_np)
        self.MPR_indexs_np = MPR_indexs_np
        # extent = np.linalg.norm
        if self.Plot:
            fig, ax = plt.subplots()
            #ax.imshow(MPR_M,origin='upper')
            ax.imshow(self.MPR_M)
            plt.gca().invert_yaxis()
            #plt.scatter(Ponits_x,Ponits_y)
            plt.show()
        print("")
        #MPR_M_vtk = numpy_support.numpy_to_vtk(num_array=MPR_M, deep=True, array_type=vtk.VTK_FLOAT)

    def PlotSelectedPointsForDis(self, Piots_pos):
        plan2 = np.transpose(self.V[:, :, min(self.Pointz_zslice).astype(int)])
        fig, ax1 = plt.subplots()
        ax1.imshow(plan2, origin='upper', extent=[self.x.min(), self.x.max(), self.y.min(), self.y.max()])
        ax1.scatter(Piots_pos[:,0],Piots_pos[:,1])
        # ax1.scatter(Line_x, Line_y, c='b')
        # ax1.scatter(points[:, 0], points[:, 1], c='g')
        # ax1.scatter(Ponits_x, Ponits_y, c='r')
        plt.show()