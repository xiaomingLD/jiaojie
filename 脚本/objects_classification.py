"""
 * Sensor Eval
 * objects_classification.py
 * @author Jialiang Shi
 """
import json

def FindAddedStillinRemoved(current, last):
    """
            根据上一帧的物体id集合，和下一帧的物体id集合，找出新添加的id，仍然存在id，和消失的id

            Parameters
            ----------
            current：list of int
                    当前帧的id集合
            last：list of int
                    上一帧的id集合

            Returns
            -----
            added：list of int
                    新添加的id
            stillin：list of int
                    仍然存在id
            removed：list of int
                    消失的id
            """
    added = []
    stillin = []
    removed = []
    for i in current:
        if i in last:
            stillin.append(i)
        else:
            added.append(i)
    for i in last:
        if i not in current:
            removed.append(i)
    return added,stillin,removed

def DumpJson(info, outName):
    """
        提取 csv 文件中所有物体曾出现的分类，并输出为 JSON 文件

        Parameters
        ----------
        info：Pandas DataFrame
                cmp转化来的csv文件，经过pandas读取
        outName：string
                希望输出的文件路径

        """
    cache = {}
    lastIds = []
    rst = []

    for _ in range(len(info)):
        frame = info[info.FrameIdx == _]

        currentInfo = {}
        for obj in frame.iterrows():
            objIdx, objId, className = obj[1].ObjIdx, obj[1].Obj_Id, obj[1].Class_Name
            currentInfo[objId] = className
        currentIds = currentInfo.keys()
        # print('last\n',lastIds)
        # print('current\n',currentIds)
        added, stillin, removed = FindAddedStillinRemoved(currentIds, lastIds)
        # print('added',added)
        # print('stillin',stillin)
        # print('removed',removed,'\n')
        lastIds = currentIds

        # 新出现的物体，在缓冲区新建一个对象
        for i in added:
            cache[i] = [currentInfo[i]]
        # 上一帧同样存在的物体，在缓冲区索引到，并添加有可能新出现的类
        for i in stillin:
            if currentInfo[i] not in cache[i]:
                cache[i].append(currentInfo[i])
                # print('updated',i,currentInfo[i])
        # 对于上一帧存在，这一帧消失的物体，把缓冲区的结果tmp直接移动到最终结果列表rst中
        for i in removed:
            tmp = {i: cache[i]}
            del cache[i]
            rst.append(tmp)
            # print('move to rst',tmp)
        # print('\ncache',cache)
        # print('rst',rst,'\n====================================================')
    rst = {'Obj_Classification': rst}

    with open(outName, 'w') as outfile:
        json.dump(rst, outfile)
