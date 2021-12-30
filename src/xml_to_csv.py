import xml.etree.ElementTree as ET
import csv
from multiprocessing import Pool

wait_queue = []

'''
@brief Transform xml file to csv file
@param file_path The file path that you want to transform
'''
def xml_to_csv(file_path: str):
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
            
            [__LinkID, __LANES] = __LINKFLOWS[0]
            waiting_list.append(__LinkID.text)
            
            [__LaneID, __LaneType, __OutSide_Speed, __Occupancy, __Vehicles] = __LANES[0]
            waiting_list.extend((__LaneID.text,
                                 __LaneType.text,
                                 __OutSide_Speed.text, 
                                 __Occupancy.text))
            
            for __Vehicle in __Vehicles:
                [__VehicleType, __Volume, __Speed] = __Vehicle
                waiting_list.extend((__VehicleType.text,
                                     __Volume.text,
                                     __Speed.text))
            
            # write down the contents into the csv file.
            with open(f"CSV_DATA/{__VDID.text}.csv", "w", newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                if(file_path == "2021_1220/20211220_0000.xml"):    # if it is the first file, it needs the label.
                    csv_writer.writerow(["VDID", "Status", "DataCollectTime", "LinkIDL", "LaneID", "LaneType", "OutSide_Speed", "Occupancy", "VehicleType", "Volume", "Speed", "VehicleType", "Volume", "Speed", "VehicleType", "Volume", "Speed"])

                csv_writer.writerow(waiting_list)
                
if __name__ == '__main__':
    
    for day in range(9):
        for hour in range(24):
            for min in range(60):
                if(hour!=23 and min!= 59):
                    file_path = "2021_122" + str(day) + "/2021122" + str(day) + f"_{hour:02d}{min:02d}" + ".xml"
                    #wait_queue.append((file_path))
                    xml_to_csv(file_path)
    
    #with Pool(20) as pool:
    #    pool.starmap(xml_to_csv, wait_queue)