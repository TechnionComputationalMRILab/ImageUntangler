import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator, splprep,splev
from typing import List
from icecream import ic

ic.configureOutput(includeContext=True)


class PointsToPlaneVectors:
    def __init__(self, allPoints: List[np.array], imageData, height = 10, viewAngle = 0, Plot = False):
        self.Plot = Plot
        self.Height = height

        self.V = np.asarray(imageData.dicomArray)


        V_spacing = np.asarray(imageData.spacing)
        V_dim = np.asarray(imageData.dimensions)

        self.x = np.linspace(-V_dim[0] * V_spacing[0] / 2, (V_dim[0] ) * V_spacing[0]/2, V_dim[0])
        self.y = np.linspace(-V_dim[1] * V_spacing[1] / 2, (V_dim[1] ) * V_spacing[1]/2, V_dim[1])
        self.z = np.linspace(-V_dim[2] * V_spacing[2] / 2, (V_dim[2] ) * V_spacing[2]/2, V_dim[2])

        self.delta = V_spacing[0]

        self.Org_points = np.asarray(allPoints)
        allPoints = self.Org_points[:, 0:3] # should be replaceable by [:, :]
        x = np.squeeze(allPoints[:, 0])
        y = np.squeeze(allPoints[:, 1])
        z = np.squeeze(allPoints[:, 2])
        if self.Plot:
            self.plotPoints(x, y, z)

        linearVTKlist = self.bspline(allPoints, self.delta, degree=2)  # calculates 2nd degree spline function for all points
        # ic(linearVTKlist)
        self.FindVectors(linearVTKlist, viewAngle)
        self.getStraightMPRVector(self.x, self.y, self.z, self.V, linearVTKlist, viewAngle)

    def plotPoints(self, x, y, z):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, '-ob')
        plt.show()

    def LinearCenterLine(self, allPoints,delta):
        # allPoints = self.Org_points[:, 0:3]
        LinearVTKlist = np.zeros([1, 3])
        for i in range(1, allPoints.shape[0]):
            Vector = allPoints[i] - allPoints[i - 1]
            point = allPoints[i - 1]
            LinearVTKlist = np.append(LinearVTKlist, [point], axis=0)
            dist = np.linalg.norm(allPoints[i] - point)
            while dist > delta:
                point = point + (delta / np.linalg.norm(Vector)) * Vector
                LinearVTKlist = np.append(LinearVTKlist, [point], axis=0)
                dist = np.linalg.norm(allPoints[i] - point)
            allPoints[i] = point + (delta / np.linalg.norm(Vector)) * Vector
        LinearVTKlist = np.append(LinearVTKlist, [allPoints[i]], axis=0)
        LinearVTKlist = LinearVTKlist[1:]
        return LinearVTKlist

    # def LinearCenterLine2(self, allPoints, delta):
    #     LinearVTKlist = np.zeros([1, 3])
    #     for i in range(1, allPoints.shape[0]):

    def bspline(self, allPoints, delta, n=100, degree=3, ):
        """ Calculate n samples on a bspline

            cv :      Array ov control vertices
            n  :      Number of samples to return
            degree:   Curve degree
        """
        x = np.squeeze(allPoints[:, 0])
        y = np.squeeze(allPoints[:, 1])
        z = np.squeeze(allPoints[:, 2])
        dist =0
        for i in range(len(allPoints)-1):
            dist += np.linalg.norm(allPoints[i+1]-allPoints[i])
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
            ax.plot(allPoints[:, 0], allPoints[:, 1], allPoints[:, 2],'-ob')
            # ax.plot(xline, yline, zline, '-og')
            ax.plot(x_fine, y_fine, z_fine,'-*r')
            # ax.plot(L[:,0], L[:,1], L[:,2], '-*b')
            # ax.plot(np.squeeze(Linear[:, 0]),np.squeeze(Linear[:, 1]),np.squeeze(Linear[:, 2]))

            plt.show()

        return B

    def plotLines(self, xline, yline, zline):
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')
        ax2.plot3D(xline, yline, zline, 'gray')
        return ax2

    def FindVectors(self, allPoints, viewAngle, plot=False):
        Vector1_list = []
        Vector2_list = []
        xline = np.squeeze(allPoints[:, 0])
        yline = np.squeeze(allPoints[:, 1])
        zline = np.squeeze(allPoints[:, 2])
        if plot:
            current_fig = self.plotLines(xline, yline, zline)

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
            Vector1_list.append(Vector1)
            Vector2_list.append(Vector2)
            viewAngleRad = np.deg2rad(viewAngle)
            Vector_teta = Vector1 * np.cos(viewAngleRad) + Vector2 * np.sin(viewAngleRad)

            Dot1_2 = np.dot(Vector1, Vector2) if abs(np.dot(Vector1, Vector2))<=1 else np.sign(np.dot(Vector1, Vector2))
            Angle_1_2.append(np.arccos(Dot1_2))
            Dot1_teta = np.dot(Vector1, Vector_teta) if abs(np.dot(Vector1, Vector_teta))<=1 else np.sign(np.dot(Vector1, Vector_teta))
            Angle_1_teta.append(np.arccos(Dot1_teta))
            Dot2_teta = np.dot(Vector2, Vector_teta) if abs(np.dot(Vector2, Vector_teta))<=1 else np.sign(np.dot(Vector2, Vector_teta))
            Angle_2_teta.append(np.arccos(Dot2_teta))
            if plot:
                current_fig.plot3D([xline[i], xline[i] + Vector1[0]], [yline[i], yline[i] + Vector1[1]], [zline[i], zline[i] + Vector1[2]], color='g')
                current_fig.plot3D([xline[i], xline[i] + Vector2[0]], [yline[i], yline[i] + Vector2[1]], [zline[i], zline[i] + Vector2[2]], color='r')
                current_fig.plot3D([xline[i], xline[i] + Vector_teta[0]], [yline[i], yline[i] + Vector_teta[1]], [zline[i], zline[i] + Vector_teta[2]], color='b')

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



    def getStraightMPRVector(self, x, y, z, V, points, viewAngle):
        # Heigth in cm, Angle in deg
        Vector1 = self.Vector1_list
        Vector2 = self.Vector2_list
        org_points = self.Org_points
        Delta = self.delta
        Height = self.Height
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

        V = np.flip(V, 1)
        interpolatingFunction = RegularGridInterpolator((x, y, z), V, method='linear')
        MPR_indexs_np_reshape = np.reshape(MPR_indexs_np, (MPR_indexs_np.shape[0] * MPR_indexs_np.shape[1], 3))
        """
        ic(MPR_indexs_np_reshape.shape)

        for i, p in enumerate(MPR_indexs_np_reshape.T):

            ic(p)
        ic(x, y, z)
        """
        MPR_M = interpolatingFunction(MPR_indexs_np_reshape)
        self.MPR_M = np.reshape(MPR_M, (MPR_indexs_np.shape[0], MPR_indexs_np.shape[1]))

        self.MPR_indexs_np = MPR_indexs_np
