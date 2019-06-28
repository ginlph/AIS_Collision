# AIS_Collision
***Yangtze river estuary collision risk distribution***

<img src="https://raw.githubusercontent.com/ginlph/AIS_Collision/master/RiskOfCollisionPicture/2016-10-01/Distribution_of_collision_risk_in_Yangtze_river_estuary(2016-10-01).png" width="75%">

---

***Geojson data for the channel of Yangtze River(Polygon)***

[The channel of Yangtze River(Polygon)](https://github.com/ginlph/AIS_Collision/blob/master/DataProcess/channel_geojson/map.geojson)

### Code Structure
* **_Time**
    * *ParseTime.py* `"%Y-%m-%d %H:%M:%S" -> datetime(year, month, day, hour, minute, second)`
    * *TimeStamp.py* `date_range(start, step, end)`
* **Area**
    * *Grid.py* `class Grid`
        * area_id: grid index(网格编号)
        * gridlon_: `np.arange(120, 126, 0.5)` (网格经度范围)
        * gridlat_: `np.arange(30, 36, 0.5)` (网格纬度范围)
        * griddelta: `0.5` (网格间隔)
        
    * *Vessel.py* `class Vessel(Grid)`
        * args: 
            *               |————MMSI
                            |————TIME
                    AIS ————|————LON
                            |————LAT
                            |————COG
                            |————SOG
        * area_id: same as Grid.area_id
        * gridlon_: same as Grid.gridlon_
        * gridlat_: same as Grid.gridlat_
        * griddelta_: same as Grid.delta_
        
* **CPA**
    * *DCPA_TCPA.py* 
        * distance method: distance between tar_ship and ref_ship(目标船与参考船之间的距离)
        * mid_point method: the half-way point along a great circle path between the two vessels(目标船与参考船之间中点地理位置)
        * bearing method: initial bearing(方位)
        <img src="http://www.movable-type.co.uk/scripts/baghdad-to-osaka.jpg">
        
        * cpa method: return DCPA, TCPA(计算两船在同一AIS时刻下的DCPA和TCPA)
        
* **DataProcess**
    * *channel_geojson* Geojson data for the channel of Yangtze River(Polygon)
    * *Meta_Data* Meta_Data queried from the mongodb database(csv format)
    * *Final_Data_Result* The final result!(csv format)
    * *SourceData.py* 
        * Store the grid and list of ships in the grid(创建网格，将AIS数据按TIME存入grid中)
    * *FinalData.py*
        * Call the method in **CPA.DCPA_TCPA**, return the final result
        (调用CPA.DCPA_TCPA中有关方法，计算最终结果)
    * *data_process.py*
        *  store result in the **Final_Data_Result** folder
        (计算结果存入Final_Data_Result文件夹)
      
* **ShipDataInsert**
    * Insert the AIS data into the mongodb database

* **ShipDataQuery**
    * Query the AIS data from the mongodb database and store it in "../../DataProcess/Meta_Data"

* **main.py**
    * use `cartopy module` to draw Yangtze river estuary collision risk distribution

### 未完待续...
***Author: LPH，TIME: 2019年06月28日 下午15:15***
 
***Address 上海海事大学(Shanghai maritime university)***

***Email 664104221@qq.com***