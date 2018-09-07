"""
 * Sensor Eval
 * single_frame_test.py
 * @author Jialiang Shi
 """

import copy
from filedriver.cmpfile import CmpFile,DataTypeId

# 读取单帧cmp文件 查看数据存储格式
fPath = "../../testfile/cmpfile/Online"
cmpFile = CmpFile(fPath)
frame = copy.deepcopy(cmpFile.ReadFrame(1, DataTypeId.Object, 'begin'))