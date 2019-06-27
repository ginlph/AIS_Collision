#First test:
##Enviroment: MacOS, 16 GB Memory, 8-core
##ScriptPath: 'FinalData.py'
##method: sort and group by
##decorator: No
##Write to csv file: No
##Cost Time: 1h 34min 10s


#Second test: 2019/06/17
##Enviroment: MacOS, 16 GB Memory, 8-core
##ScriptPath: 'AIS_Collision/DataProcess/data_process.py'
##method: SourceData.source_data + FinalData.calculation
##Write to csv file: yes
##SourceData Directory: 'AIS_Collision/DataProcess/Meta_Data'
##FinalData Directory: 'AIS_Collision/DataProcess/Final_Data_Result'
##The Length of original file —— final_data.csv: 80029
##The Length of final file —— finall_data-10-01.csv: 80089
##Cost Time: 1444.872s


#Second test: 2019/06/17
##Enviroment: DELL T7610, 16 GB Memory, 12-core
##ScriptPath: 'AIS_Collision/DataProcess/data_process.py'
##method: SourceData.source_data + FinalData.calculation
##Write to csv file: yes
##SourceData Directory: 'AIS_Collision/DataProcess/Meta_Data'
##FinalData Directory: 'AIS_Collision/DataProcess/Final_Data_Result'
##The Length of original final_data.csv: 80029
##The Length of original final_data.csv: 80089
##Cost Time: 1845.163s