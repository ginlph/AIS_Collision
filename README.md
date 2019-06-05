# AIS_Collision
Risk distribution of collision of ships along China's coast

预估方案:
    1.2016年全年366天，计算中国沿海船舶碰撞风险需要计算366次
        可采用MapReaduce、Spark、Hadoop等大数据处理框架进行并行计算！！！
    2.时间范围
        ("2016-10-01" <= time < "2016-10-02")
        按一天进行计算，时间间隔可为1s，那么一天为24 * 60 * 60 = 86400(共有86400个时刻，86400个网格范围)
    如: "2016-10-01 00:00:00", "2016-10-01 00:00:01" ... "2016-10-01 23:59:59", "2016-10-02 00:00:00"
    3.网格区域:
        [[120, 30], [125, 35]]
    4.网格粒度:
        0.5 * 0.5
    5.查找算法:
        二分查找BinarySearch(sequence, value)
        sequence: 顺序存储的序列
        value: 查找的值
        return:
            返回value的索引值
    finally:
        longitude: np.arange(120, 125, 0.5)
        latitude: np.arange(30, 35, 0.5)

数据存储方案:
    1.网格抽象化:
    class Grid:
        grid_delta = 0.5
        LON_LENGTH = len(longitude)
        def __init__(self, area_ID):
        # 根据传进来的网格编号area_ID, 可以直接定位该网格左下角的经纬度
        # 省了两层嵌套for循环
            self.area_ID = area_ID
            self.Left_lon = longitude[area_ID % Grid.LON_LENGTH]
            self.Left_lat = latitude[area_ID // Grid.LON_LENGTH]
            self.Right_lon = self.Left_lon + Grid.grid_delta
            self.Right_lat = self.Left_lat + Grid.grid_delta
            self.flag = 3
            if self.Left_lat == min(latitude) or self.Left_lat == max(latitude):
                self.flag = 2
                if self.Left_lon == min(longitude) or self.Left_lon == max(longitude):
                    self.flag = 1
            if self.Left_lon == min(longitude) or self.Left_lon == max(longitude):
                self.flag = 2
                if self.Left_lat == min(latitude) or self.Left_lat == max(latitude):
                    self.flag = 1
            self.need_ID = None
        
        def need_id(self):
            if self.flag == 3:  # 中部网格计算, flag=3
                id_1 = self.area_ID
                id_2 = self.area_ID + 1
                id_3 = self.area_ID + Grid.LON_LENGTH - 1
                id_4 = self.area_ID + Grid.LON_LENGTH
                id_5 = self.area_ID + Grid.LON_LENGTH + 1
                self.need_ID = [id_1, id_2, id_3, id_4, id_5]
            elif self.flag == 2: # 4种边界网格计算, flag=2
                if self.Left_lat == min(latitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + 1
                    id_3 = self.area_ID + Grid.LON_LENGTH - 1
                    id_4 = self.area_ID + Grid.LON_LENGTH
                    id_5 = self.area_ID + Grid.LON_LENGTH + 1
                    self.need_ID = [id_1, id_2, id_3, id_4, id_5]
                elif self.Left_lat == max(latitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + 1
                    self.need_ID = [id_1, id_2]
                elif self.Left_lon == min(longitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + 1
                    id_3 = self.area_ID + Grid.LON_LENGTH
                    id_4 = self.area_ID + Grid.LON_LENGTH + 1
                    self.need_ID = [id_1, id_2, id_3, id_4]
                elif self.Left_lon == max(longitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + Grid.LON_LENGTH - 1
                    id_3 = self.area_ID + Grid.LON_LENGTH
                    self.need_ID = [id_1, id_2, id_3]
            elif self.flag == 1: # 网格4个角落, flag=1
                if self.Left_lon == min(longitude) and self.Left_lat == min(latitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + 1
                    id_3 = self.area_ID + Grid.LON_LENGTH
                    id_4 = self.area_ID + Grid.LON_LENGTH + 1
                    self.need_ID = [id_1, id_2, id_3, id_4]
                elif self.Left_lon == max(longitude) and self.Left_lat == min(latitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + Grid.LON_LENGTH - 1
                    id_3 = self.area_ID + Grid.LON_LENGTH
                    self.need_ID = [id_1, id_2, id_3]
                elif self.Left_lon == min(longitude) and self.Left_lat == max(latitude):
                    id_1 = self.area_ID
                    id_2 = self.area_ID + 1
                    self.need_ID = [id_1, id_2]
                elif self.Left_lon == max(longitude) and self.Left_lat == max(latitude):
                    id_1 = self.area_ID
                    self.need_ID = [id_1]
            return self.need_ID
        (1)每一个Grid中，都有左下角经纬度Left: (lon, lat), 当然也可以有右上角经纬度Right: (lon, lat);
        (2)识别网格flag;
        (3)网格编号area_ID;可用作"网格名", 如grid(area_belong_ID)
        (4)每一个网格所需计算的其他网格编号need_ID
    
    2.存储网格区域:
    grid = [
        {datetime(2016, 10, 1, 0, 0, 0): [Vessel(0, args), Vessel(1, args), Vessel(2, args), ..., Vessel(99, args)]}
        {datetime(2016, 10, 1, 0, 0, 1): [Vessel(0, args), Vessel(1, args), Vessel(2, args), ..., Vessel(99, args)]}
        ......
        {datetime(2016, 10, 1, 23, 59, 59): [Vessel(0, args), Vessel(1, args), Vessel(2, args), ..., Vessel(99, args)]}
        {datetime(2016, 10, 2, 0, 0, 0): [Vessel(0, args), Vessel(1, args), Vessel(2, args), ..., Vessel(99, args)]}
    ]
    其中,该列表中共有86400个字典,dict().values()存储在该dict().keys()对应时刻下船舶AIS数据
    Vessel(area_ID, args): 是Grid网格类的子类,继承Grid的所有属性及方法
        area_ID: 船舶所在网格的编号
        args: 船舶AIS信息
                                |————MMSI
                                |————TIME
                        AIS ————|————LON
                                |————LAT
                                |————COG
                                |————SOG

    class Vessel(Grid):
        def __init__(self, area_ID, args):
            self.MMSI = args[0]
            self.TIME = args[1]
            self.LON = args[2]
            self.LAT = args[3]
            self.COG = args[4]
            self.SOG = args[5]
            Grid.__init__(self, area_ID)

    3.将AIS数据倒入至子网格
        (1) 在MongoDB数据库中, 查询满足时间范围("2016-10-01" <= time < "2016-10-02")、网格区域[[120, 30], [125, 35]]
    的船舶AIS数据
    db.collection.find({
        "TIME": {$gte: "2016-10-01", $lt: "2016-10-02"},
        "location": {
        $geoWithin: {
            type: "Polygon",
            coordinates: [[[120, 30], [125, 30], [125, 35], [120, 35], [120, 30]]]
        }
    }
})
        
        (2) 查询后数据暂时存储形式csv
    查询结果results:
    results = [{MMSI, TIME, LON, LAT, COG, SOG}, {}, ...., {}]
    import csv
    with open("2016-10-01.csv", "w") as f:
        datas = csv.writer(f)
        Header = ["MMSI", "TIME", "LON", "LAT", "COG", "SOG"]
        for result in results:
            datas.writerow([
                result["MMSI"],
                result["TIME"],
                result["location"]["coordinates"][0],
                result["location"]["coordinates"][1],
                result["COG"],
                result["SOG"]
        ])

    4.为每艘船的AIS点加入网格编号area_ID
        (1) 二分法BinarySearch
            def BinarySearch(sequence, value):
            """
            二分法BinarySearch
            [注] 序列sequence必须采用顺序存储结构，而且表中元素按关键字有序排列
            sequence: 目标序列
            value: 在序列中查找的值
            return: 查找value的索引值
            """
            begin = 0
            end = len(sequence) - 1
            while begin <= end:
                middle = (begin + end) // 2
                # middle = int(begin + (value - sequence[begin])/(sequence[end] - sequence[begin])*(end-begin))
                if list(sequence[middle].keys())[0] < value:
                    begin = middle + 1
                elif list(sequence[middle].keys())[0] > value:
                    end = middle - 1
                else:
                    return middle

        (2) 将AIS数据倒入"存储网格区域"
        Lon_Length = len(longitude)
        with open("2016-10-01.csv") as f:
            datas = csv.reader(f)
            next(datas)
            for data in datas:
                # 先根据经、纬度(data[2], data[3])确定子网格编号area_ID
                # 后根据时间(data[1])判断在哪个"网格区域"
                # BinarySearch([list], value)
                if int(data[2][4]) >= 5 or int(data[3][3]) >=5:
                    _lon = int(data[2][: 3]) + 0.5
                    _lat = int(data[3][: 2]) + 0.5
                else:
                    _lon = int(data[2][: 3])
                    _lat = int(data[3][: 2])
                # _lon, _lat 为每一个AIS所在网格左下角的经纬度
                # lon_remainder, lat_quotient 为_lon, _lat在longitude和latitude的索引值
                lon_remainder = int(*np.where(longitude == _lon))
                lat_quotient = int(*np.where(latitude == _lat))
                # area_ID = _lat在latitude中的索引 * longitude的长度 + _lon在longitude中的索引
                area_ID = lat_quotient * LON_LENGTH + lon_remainder
                grid[BinarySearch(grid, data[1])][data[1]].append(Vessel(area_ID, data))

    5.计算两船间的DCPA和TCPA
    def dcpa(Tar_Ship, Ref_Ship):
        """
        计算目标船与参考船之间的DCPA和DCPA
        Tar_Ship: 目标船
        Ref_Ship: 参考船
        return:  DCPA、TCPA
        """
        Tar_Lat, Tar_Lon = Tar_Ship.LAT, Tar_Ship.LON
        Tar_Cog, Tar_Sog = Tar_Ship.COG, Tar_Ship.SOG
        Ref_Lat, Ref_Lon = Ref_Ship.LAT, Ref_Ship.LON
        Ref_Cog, Ref_Sog = Ref_Ship.COG, Ref_Ship.SOG

        # 两船之间的距离distance
        distance = get_distance_hav(Tar_Lat, Tar_Lon, Ref_Lat, Ref_Lon)

        alpha = Tar_Cog - Ref_Cog
        if alpha > 180:
            alpha -= 360
        elif alpha < -180:
            alpha += 360

        # 两船之间的相对速度Relative_Speed
        Relative_Speed = sqrt(Tar_Sog**2 + Ref_Sog**2 - 2*Tar_Sog*Ref_Sog*cos(alpha / 180.0 * pi))

        Q = acos((Relative_Speed**2 + Tar_Sog**2 - Ref_Sog**2) / (2 * Relative_Speed * Tar_Sog)) * 180.0 / pi
        # 两船之间的相对航向Relative_Course
        if alpha > 0:
            Relative_Course = Tar_Cog + Q
        else:
            Relative_Course = Tar_Cog - Q

        # 相对舷角Bearing
        Bearing = bearing.initial_compass_bearing(Tar_Lat, Tar_Lon, Ref_Lat, Ref_Lon) - Relative_Course
        DCPA = distance * sin(Bearing * pi / 180.0)
        TCPA = distance* cos(Bearing * pi / 180.0) / Relative_Speed
        return DCPA, TCPA



数据计算方案:
    main.py
    网格范围
        longitude: np.arange(120, 125, 0.5)
        latitude: np.arange(30, 35, 0.5)
    
    遇到的问题:
        1.怎么做并行化计算？现有阶段只能算一天的数据，2016年分为366个子任务？
        2.使用异步？进程？线程？
        3.MapReaduce和Hadoop、Spark大数据处理框架是否对现有DCPA、TCPA计算有帮助？怎么使用？
        4.代码要写成分布式么？
        5.已有工作性能更强的工作站，可能要搭建基于“分片Sharding”的MongoDB数据库
        现实问题：
            工作站怎么使用？
    
    原始数据集SourceData:
    处理数据集DataProcess:
    应用数据集DataApplication:

    使用cartopy画风险分布点:
        思路:
        1. 
