
# coding: utf-8

# In[2]:


import copy
import sys
sys.path.append('D:\Repo\sensoreval')
from filedriver import cmpfile
import json 
import shutil



# In[3]:


fPath = r"D:\石佳亮交接\to_csv\ped_009.cmp"
#fPath = r"D:\石佳亮交接\to_csv\car_006.cmp"


# In[4]:

WorkFile = cmpfile.CmpFile(fPath)

#输出数据帧总数
FIndx = cmpfile.DataTypeId.FrameIndex
FEnd = copy.deepcopy(WorkFile.ReadFrame(0,FIndx))
FrameNum = FEnd.DataBlock.FrameIdxNum

print(FrameNum)


# In[5]:


# 输出数据

dt = cmpfile.DataTypeId.Object
frame1 = copy.deepcopy(WorkFile.ReadFrame(0,dt))

for _ in frame1.DataBlock.Objects:
    print(_.Id,': ',_.Classification.name)


# In[6]:


for i in range(FrameNum):
    currentF = copy.deepcopy(WorkFile.ReadFrame(i,dt,'begin'))
    print("FrameIdx ", i)
    for _ in currentF.DataBlock.Objects:
        print('',_.Id,': ',_.Classification.name)


# In[7]:



# FrameInfo = {}
# huanchong = []

# for i in range(FrameNum):
#     currentF = copy.deepcopy(WorkFile.ReadFrame(i,dt,'begin'))
#     for _ in currentF.DataBlock.Objects:
#         huanchong.append({_.Id:_.Classification.name})
#     FrameInfo[i] = huanchong
#     FrameInfo[i].append({"Error":False})
#     huanchong = []


# In[8]:


FrameInfo = {}
huanchong = {}

for i in range(FrameNum):
    currentF = copy.deepcopy(WorkFile.ReadFrame(i,dt,'begin'))
    for _ in currentF.DataBlock.Objects:
        huanchong[_.Id]= _.Classification.name
#    huanchong['Error'] = False
    FrameInfo[i] = huanchong
    huanchong = {}

print(FrameInfo)


# In[9]:


for i,j in FrameInfo.items():
    print(i)
    for n,k in j.items():
        print('  ',n,' ',k)
    print()
    


# In[10]:


print(len(FrameInfo))


# In[11]:


# 写入 Json 文件

with open("DataOrigin.json", 'w') as f:
    json.dump(FrameInfo,f,indent = 4)


# In[12]:


def find_added_stillin_removed(current,last):
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

current = [1,2,3,4,5]
last = [0,3,4]
find_added_stillin_removed(current,last)


# In[18]:


huanchong = {}
tmp = {}
last_ids = []
rst = []

for _ in range(FrameNum):
    current_info = FrameInfo[_]
#    print(current_info)    # 打印出来
    
    current_ids = current_info.keys()
#    print(current_ids)
    
    added,stillin,removed = find_added_stillin_removed(current_ids,last_ids)
 #   print(added,stillin,removed)
    

    
    for i in added:
        huanchong[i] = [current_info[i]]
    for i in stillin:
        if current_info[i] not in huanchong[i]:
            huanchong[i].append(current_info[i])
    
    for i in removed:
        tmp = {i:huanchong[i]}
        rst.append(tmp)
        del huanchong[i]

    if _ == FrameNum - 1:
        for key, value in huanchong.items():
            rst.append({key:value})

    last_ids = current_ids
#print(huanchong)

print(rst)

