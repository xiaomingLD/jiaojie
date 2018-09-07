"""
 * Sensor Eval
 * to_csv_test.py
 * @author Jialiang Shi
 """
from filedriver.to_csv import InitCsv,ExtractFrame
import copy
from filedriver.cmpfile import CmpFile,DataTypeId



# Head 需要与filedriver.to_csv.extract_frame中 35-70 行 对应
head = ('FrameIdx',
            'TimeStamp',
            'ObjIdx',
            'Obj_Id',
            'BdBox_0X',
            'BdBox_0Y',
            'BdBox_1X',
            'BdBox_1Y',
            'BdBox_2X',
            'BdBox_2Y',
            'BdBox_3X',
            'BdBox_3Y',
            'Center_X',
            'Center_Y',
            'Class_Name',
            'Velocity_X',
            'Velocity_Y',
            )

outputName = 'objects_info.csv'
fPath = "../../testfile/cmpfile/Online"

InitCsv(head, outputName)
cmpFile = CmpFile(fPath)
frameNum = cmpFile.TotalFrameNum

for i in range(frameNum):
    ExtractFrame(i, cmpFile, outputName)

