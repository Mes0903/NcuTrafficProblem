import xml.etree.ElementTree as ET
import os

with open("src/VD_0000.xml", encoding="utf-8") as fp:
    __VDList = ET.parse(fp).getroot()    # get the root Node of the xml tree
    __VDs = __VDList[3]    # get the root Node of the subtree VDLives
    
    with open("VD_0000.csv", 'w') as csvfile:
        label = ["VDID", "SubAuthorityCode", "BiDirectional", "LinkID", "Bearing", "RoadDirection", "LaneNum", "ActualLaneNum", "VDType", "LocationType", "DetectionType", "PositionLon", "PositionLat", "RoadID", "RoadName", "RoadClass", "Start", "End", "LocationMile"]
        csvfile.write(",".join(label) + '\n')
        
        for __VD in __VDs:
            [__VDID, __SubAuthorityCode, __BiDirectional, __DETECTIONLINKS, __VDType,
             __LocationType, __DetectionType, __PositionLon, __PositionLat,
             __RoadID, __RoadName, __RoadClass, __RoadSection, __LocationMile] = __VD

            row = [__VDID.text, 
                   __SubAuthorityCode.text,
                   __BiDirectional.text]
            
            [__LinkID, __Bearing, __RoadDirection, __LaneNum, __ActualLanNum] = __DETECTIONLINKS[0]
            row.extend((__LinkID.text, __Bearing.text, __RoadDirection.text, __LaneNum.text, __ActualLanNum.text))
            
            row.extend((__VDType.text, 
                        __LocationType.text, __DetectionType.text, __PositionLon.text, __PositionLat.text,
                        __RoadID.text, __RoadName.text, __RoadClass.text))
            
            [__Start, __End] = __RoadSection
            
            row.extend((__Start.text, __End.text, __LocationMile.text))
            
            csvfile.write(",".join(row) + '\n')
            