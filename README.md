# Traffic Data Analysis - Turning Movement Counts

Traffic Data Analysis - Turning Movement Counts

## Context 

![](images/traffic%20data%20portal.png)

When a traffic data provider lacks API access, the task became to find a way to automate the processing of the data as shown in the online cloud portal.  Based on the vendor's structure, each project represents a **purchase order PO** and each study represents an intersection that was studied on either tuesday, wednesday or thursday between the hours of 6AM - 7PM. This is known as a 13-hr turning movement count study, typically used to gather data for signal warrant studies. 

The following main pieces are extracted from the study:
- total traffic volume 
- turning movements (entry/exit directions)
- vehicle classification
- video recording of the entire movement count 
- peak hour factor (AM, MIDDAY, PM)

##### Images from vendor's cloud report
![](images/traffic%20could%20maps.png)
![](turning%20movement%20count%20chart.png)
![](turning%20movement%20count.png)
![](video%20and%20peak%20hour%20factors.png)

## Objectives 

> Aggregating the different sources of traffic data, along with government provided sources creates a background to compare against data coming from subscription services. 

##### Step 1: Download all CSV's related to the current projects 
Because the vendor allowed downloading by project (collection of studies), the bigger task became bringing all the studies out to a root folder, totaling almost 500 csv files. 

|Project|Volume|Year|Quarter|Longitude|Latitude|
|---|---|---|---|---|---|
|1|2-1058 - Harris County - Open PO#36384|956294.0|2021|3|29.997896|-95.797362|
|2|2-4686 - Harris County - PO 2022-45695|1049938.0|2022|2|30.103385|-95.499133|
|3|2-6404 - Harris County - PO-May 2022 Pt 2|1156824.0|2022|2|30.11023|-95.512759|
|4|2-7900 - Harris Co. Oct. Open PO|1222130.0|2022|4|29.941478|-95.762904|
|5|Harris County - Open PO 2020|766079.0|2020|3|29.853378|-95.683233|

![[average volume tracked per year.png]]

#### Step 2 Process into Dataframe

Provided instructions within the script, the objective follows: 
1. Import file paths and csv 
2. Read all csv with panda
3. validate dataframes
4. transform each dataframe, summary and raw data 
5. concatenate into a single dataframe
6. group by to appropriate transformations to load into GIS

link to script

![](images/Preview%20of%20studies%20in%20GIS.png)

#### Step 3: Process into GIS 

*WIP - match against junction code, aggregate with other sources* 

#### Step 4: Load into PowerBI/external platforms

*WIP -*

