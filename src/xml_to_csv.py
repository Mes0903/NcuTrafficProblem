import xml.etree.ElementTree as ET
from multiprocessing import Pool
from collections import defaultdict
import os

dictionary = defaultdict(list)

'''
@brief Write the content in the dictionary to the csv file.
@param key The key in the dictionary, which is the name of the sensor("VDID" in the xml)
@param value The data that connect by the sensor, the sensor connect one data per minute.
             It's a list of list, each element in the list is the data per minute, 
             which is one row in the csv file.
'''
def write_csv(key: str, value: list):
    FILENAME = "CSV_DATA/" + key + ".csv"    
    flag = not os.path.exists(FILENAME)    # if file doesn't exist, it need write label at first.
    
    with open(FILENAME, 'a') as file:
        if flag:
            __Lane_num = value[0].count('S')    # find the number of Lanes
            label = ",".join(["VDID", "Status", "DataCollectTime", "LinkIDL"]) + "," + ",".join(["LaneID", "LaneType", "OutSide_Speed", "Occupancy", *(["VehicleType", "Volume", "Speed"]*3)]*__Lane_num) + '\n'
            file.write(label)
            
        for row in value:
            file.write(",".join(map(str, row)) + '\n')    # write the csv file

'''
@brief Append the file_path to a small dictionary
@param file_path The file path that you want to transform
@return The samll dictionary, which will be merged to the `dictionary`
'''
def append_dic(file_path: str):
    
    s_dic = defaultdict(list)
    
    # open the file
    with open(f"{file_path}") as fp:
        __VDLiveList = ET.parse(fp).getroot()    # get the root Node of the xml tree
        __VDLives = __VDLiveList[3]    # get the root Node of the subtree VDLives
        
        # visit all Nodes in the subtree, __VDLive is the root of the subtree that we care about.
        # There are four childs nodes, three of them are single node with some value, the rest node
        # is the root of subtree, and it just have one child. You can check the image on the github.
        for __VDLive in __VDLives:
            [__VDID, __LINKFLOWS, __Status, __DataCollectTime] = __VDLive
    
            waiting_list = [__VDID.text, 
                            __Status.text,
                            __DataCollectTime.text]

            [__LinkID, __Lanes] = __LINKFLOWS[0]
            waiting_list.append(__LinkID.text)

            Lane_cnt = 0
            for __Lane in __Lanes:
                [__LaneID, __LaneType, __OutSide_Speed, __Occupancy, __Vehicles] = __Lane
                waiting_list.extend((__LaneID.text,
                                     __LaneType.text,
                                     __OutSide_Speed.text, 
                                     __Occupancy.text))
                
                for __Vehicle in __Vehicles:
                    [__VehicleType, __Volume, __Speed] = __Vehicle
                    waiting_list.extend((__VehicleType.text,
                                         __Volume.text,
                                         __Speed.text))
                    
            # add the attribute to dictionary
            s_dic[__VDID.text] = waiting_list    # s_dic.items() = [(__VIDI.text, [list]), (__VIDI.text, [list]), (__VIDI.text, [list]), ..., (__VIDI.text, [list])]
            
    return s_dic
                
if __name__ == '__main__':
    os.makedirs("CSV_DATA", exist_ok = True)    # check if the folder exists, if it doesn't exist, then create the folder
    for SENSOR_DATA in os.listdir("CSV_DATA"):
        os.remove(os.path.join("CSV_DATA", SENSOR_DATA))    # clear the folder
        
    with Pool(12) as pool:
        for day in range(9):
            for hour in range(24):
                file_list = []
                for min in range(60):
                    file_path = "2021_122" + str(day) + "/2021122" + str(day) + f"_{hour:02d}{min:02d}" + ".xml"
                    if(os.path.exists(file_path)):
                        file_list.append(file_path)    # append the file path to work queue

                print(f"day = {day:02d}, hour = {hour:03d}")

                # Append the xml file attribute into small dictionary,
                # it means data is list of dictionary, which return from `append_dic` function,
                # thus, data = [s_dic1, s_dic2, ... , s_dicn], the number is the order that pass in the function 
                print("appending small dictionary")
                data = pool.map(append_dic, file_list)    # data = [s_dic1, s_dic2, ..., s_dic3]

                print("merging to dictionary")
                for dic_ele in data:
                    for key, value in dic_ele.items():
                        dictionary[key].append(value)

                print("writing to csv file")
                pool.starmap(write_csv, dictionary.items())

                dictionary.clear()