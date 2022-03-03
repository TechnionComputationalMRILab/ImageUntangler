import numpy as np
from scipy.interpolate import RegularGridInterpolator, splprep, splev
from typing import List

from MRICenterline.DisplayPanel.Model.ImageProperties import ImageProperties


class PointsToPlaneVectors:
    def __init__(self, all_points: List[np.array], image_data: ImageProperties,
                 height: int = 10, angle_degrees: int = 0):
        self.height = height
        self.angle = angle_degrees
        self.points = np.asarray(all_points)
        self.image_data = np.asarray(image_data.nparray)

        spacing = image_data.spacing
        dim = image_data.size
        self.x = np.linspace(-dim[0] * spacing[0] / 2, (dim[0]) * spacing[0] / 2, dim[0])
        self.y = np.linspace(-dim[1] * spacing[1] / 2, (dim[1]) * spacing[1] / 2, dim[1])
        self.z = np.linspace(-dim[2] * spacing[2] / 2, (dim[2]) * spacing[2] / 2, dim[2])

        self.delta = spacing[0]

        print("c")
        # calculates 2nd degree spline function for all points
        linearVTKlist = self.bspline()
        print("c")
        self.FindVectors(linearVTKlist, angle_degrees)
        print("c")
        self.getStraightMPRVector(self.x, self.y, self.z, self.image_data, linearVTKlist, angle_degrees)
        print("c")

    # def LinearCenterLine(self, allPoints,delta):
    #     LinearVTKlist = np.zeros([1, 3])
    #     for i in range(1, allPoints.shape[0]):
    #         Vector = allPoints[i] - allPoints[i - 1]
    #         point = allPoints[i - 1]
    #         LinearVTKlist = np.append(LinearVTKlist, [point], axis=0)
    #         dist = np.linalg.norm(allPoints[i] - point)
    #         while dist > delta:
    #             point = point + (delta / np.linalg.norm(Vector)) * Vector
    #             LinearVTKlist = np.append(LinearVTKlist, [point], axis=0)
    #             dist = np.linalg.norm(allPoints[i] - point)
    #         allPoints[i] = point + (delta / np.linalg.norm(Vector)) * Vector
    #     LinearVTKlist = np.append(LinearVTKlist, [allPoints[i]], axis=0)
    #     LinearVTKlist = LinearVTKlist[1:]
    #     return LinearVTKlist

    def bspline(self):
        x = np.squeeze(self.points[:, 0])
        y = np.squeeze(self.points[:, 1])
        z = np.squeeze(self.points[:, 2])
        dist = 0
        for i in range(len(self.points)-1):
            dist += np.linalg.norm(self.points[i+1]-self.points[i])
        n = np.int(round(dist/self.delta))

        tck, u = splprep([x, y, z], s=2)

        u_fine = np.linspace(0, 1, n)
        x_fine, y_fine, z_fine = splev(u_fine, tck)
        B = np.array([x_fine, y_fine, z_fine])
        B = B.T

        return B

    def FindVectors(self, allPoints, viewAngle):
        Vector1_list = []
        Vector2_list = []
        xline = np.squeeze(allPoints[:, 0])
        yline = np.squeeze(allPoints[:, 1])
        zline = np.squeeze(allPoints[:, 2])

        Angle_1_2 = []
        Angle_1_teta = []
        Angle_2_teta = []

        for i in range(0, zline.size-1):
            NormalDirection = np.array([xline[i + 1] - xline[i], yline[i + 1] - yline[i], zline[i + 1] - zline[i]])
            Vector1 = np.array([-NormalDirection[1], NormalDirection[0], 0])
            Vector2 = np.cross(Vector1, NormalDirection)

            # Normalize vectors:
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

        #Add vectors to arrays
        self.Vector1_list = np.asarray(Vector1_list)
        self.Vector2_list = np.asarray(Vector2_list)

    def getStraightMPRVector(self, x, y, z, V, points, viewAngle):
        # Heigth in cm, Angle in deg

        Vector1 = self.Vector1_list
        Vector2 = self.Vector2_list
        org_points = self.points
        Delta = self.delta
        Height = self.height
        viewAngleRad = np.deg2rad(viewAngle)
        size_x = len(Vector1)

        Vector_teta = Vector1 * np.cos(viewAngleRad) + Vector2 * np.sin(viewAngleRad)
        self.Pointz_zslice = np.squeeze(org_points[:, :])

        Num = Height // Delta
        Heigth = Num * Delta
        MPR_indexs = []
        for i in range(0, size_x):
            Center_point = points[i]
            Column_Vector = Vector_teta[i]
            Column_Vector_norm = Vector_teta[i]/np.linalg.norm(Column_Vector)

            point_start = Center_point - (Heigth/2)*Column_Vector_norm

            Column_MPR_x = np.arange(0, Num + 1) * Delta * Column_Vector_norm[0] + point_start[0]
            Column_MPR_y = np.arange(0, Num + 1) * Delta * Column_Vector_norm[1] + point_start[1]
            Column_MPR_z = np.arange(0, Num + 1) * Delta * Column_Vector_norm[2] + point_start[2]
            Column_MPR = np.stack((Column_MPR_x, Column_MPR_y, Column_MPR_z)).T
            size_y = Column_MPR.shape[0]
            MPR_indexs.append(Column_MPR)

        MPR_indexs_np = np.asarray(MPR_indexs)

        V = np.flip(V, 1)
        interpolatingFunction = RegularGridInterpolator((x, y, z), V, method='linear')
        MPR_indexs_np_reshape = np.reshape(MPR_indexs_np, (MPR_indexs_np.shape[0] * MPR_indexs_np.shape[1], 3))

        MPR_M = interpolatingFunction(MPR_indexs_np_reshape)
        self.MPR_M = np.reshape(MPR_M, (MPR_indexs_np.shape[0], MPR_indexs_np.shape[1]))
        self.MPR_indexs_np = MPR_indexs_np
