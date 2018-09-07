"""
 * Sensor Eval
 * add_omiga_csv.py
 * @author Jialiang Shi
 """

import numpy as np
import pandas as pd

def GetOuterOmiga(points):
    """
        获取物体视野夹角的中线位置的omiga角
        omiga角定义为x轴正方向为0，向上为正，向下为负，范围是(-pi,pi]

        Parameters
        ----------
        points : A list of list, each list is 2 float numbers
                四个角点的坐标,形式如下：
                [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]

        Returns
        -----
        omiga : float number
                物体视野夹角的中线位置的omiga角
        """
    angles = []
    for i,j in [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]:
        a,b = points[i],points[j]
        #print(a,b)
        adj1 = np.sqrt(a[0]**2+a[1]**2)
        adj2 = np.sqrt(b[0]**2+b[1]**2)
        opposite = np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
        #print(adj1,adj2,opposite)
        tmp = (adj1**2+adj2**2-opposite**2)/2/adj1/adj2
        #print(np.arccos(tmp)/np.pi*180)
        angles.append([[i,j],np.arccos(tmp)/np.pi*180])
    max_angle = angles[0][1]
    end_points = angles[0][0]
    for i,j in angles:
        #print('ij',i,j)
        if j>max_angle:
            max_angle = j
            end_points = i
        #print(points,max_angle)
    a,b = points[end_points[0]],points[end_points[1]]
    #print(a,b)
    x,y = (a[0]+b[0])/2,(a[1]+b[1])/2
    omiga = PositionToOmiga(x,y)
    return omiga

def PositionToOmiga(x,y):
    """
        已知物体中点坐标（无论何种形式获得），转化为omiga角

        Parameters
        ----------
        x,y : float numbers
                物体中点坐标

        Returns
        -----
        omiga : float number
                物体中点坐标对应的omiga角
        """
    if x==0 and y==0:
        return np.NAN
    if x==0 and y>0:
        return np.pi/2
    if x==0 and y<0:
        return -np.pi/2
    if x>0 and y==0:
        return 0
    if x<0 and y==0:
        return np.pi
    if x>0:
        return(np.arctan(y/x))
    if x<0 and y>0:
        return(np.pi+np.arctan(y/x))
    if x<0 and y<0:
        return(-np.pi+np.arctan(y/x))

def AddOmigaToCsv(inputPath,outputPath):
    """
        向csv文件中添加两种omiga角
            1. 物体视野夹角的中线位置的omiga角
            2. 物体中心点的omiga角

        Parameters
        ----------
        inputPath : string
                输入文件的路径

        outputPath : string
                输出文件的路径

        效果
        -----
        在outputPath位置新建一个csv文件，除了包含原始文件的数据，另包含两列omiga角信息
        """
    info = pd.read_csv(inputPath)

    outerOmiga = []
    for obj in info.iterrows():
        x0, y0, x1, y1, x2, y2, x3, y3 = obj[1][3:11]
        points = [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
        omiga = GetOuterOmiga(points)
        outerOmiga.append(omiga)
    print(len(info), len(outerOmiga))
    info['Outer_Omiga'] = outerOmiga

    centerOmiga = []
    for i in info.iterrows():
        x, y = i[1].Center_X, i[1].Center_Y
        omiga = PositionToOmiga(x, y)
        centerOmiga.append(omiga)
    info['Center_Omiga'] = centerOmiga

    info.to_csv(outputPath)