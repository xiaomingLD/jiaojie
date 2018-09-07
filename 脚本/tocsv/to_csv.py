"""
 * Sensor Eval
 * to_csv.py
 * @author Jialiang Shi
 """
import copy
from filedriver.cmpfile import CmpFile,DataTypeId

def InitCsv(head, fname):
    """
    Initiate csv table head
    :param head: table head to use
    :param fname: the output name of the csv table
    :return: None
    """
    l = len(head)
    with open(fname, 'w') as csvfile:
        csvfile.write((('%s,'*l)[:-1]+'\n')% head)

def ExtractFrame(idx,cmpFile,fname):
    """
    Extract useful features from a frame, and append to the csv table.
    :param idx: the frame idx
    :param cmpFile: cmpFile to use
    :param fname: the output name of the csv table
    :return: None
    """
    frame = copy.deepcopy(cmpFile.ReadFrame(idx, DataTypeId.Object, 'begin'))
    timeStamp = frame.GetFrameHeader().TimeStamp.ToUnixStamp()
    frameIdx = frame.GetFrameHeader().FrameIdx
    objList = frame.GetDataBlock().Objects
    objNum = len(objList)
    # 需要与所需属性的header对应
    for i in range(objNum):
        obj = objList[i]
        obj_idx = i
        obj_id = obj.Id
        BdBox_0X = obj.BoundingBox[0].ToVector()[0]
        BdBox_0Y = obj.BoundingBox[0].ToVector()[1]
        BdBox_1X = obj.BoundingBox[1].ToVector()[0]
        BdBox_1Y = obj.BoundingBox[1].ToVector()[1]
        BdBox_2X = obj.BoundingBox[2].ToVector()[0]
        BdBox_2Y = obj.BoundingBox[2].ToVector()[1]
        BdBox_3X = obj.BoundingBox[3].ToVector()[0]
        BdBox_3Y = obj.BoundingBox[3].ToVector()[1]
        center_X = obj.Center.ToVector()[0]
        center_Y = obj.Center.ToVector()[1]
        className = obj.Classification.name
        velocity_X = obj.Velocity.ToVector()[0]
        velocity_Y = obj.Velocity.ToVector()[1]

        info = (frameIdx,
                timeStamp,
                obj_idx,
                obj_id,
                BdBox_0X,
                BdBox_0Y,
                BdBox_1X,
                BdBox_1Y,
                BdBox_2X,
                BdBox_2Y,
                BdBox_3X,
                BdBox_3Y,
                center_X,
                center_Y,
                className,
                velocity_X,
                velocity_Y,
                )
        info_str = tuple([str(i) for i in info])
        with open(fname, 'a') as csvfile:
            csvfile.write((('%s,' * len(info))[:-1] + '\n') % info_str)