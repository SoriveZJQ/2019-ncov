# 2019-ncov
python仿真程序

初始化：  
1️⃣：创建一个二维数组_people，count行2列，代表count个人的位置坐标(x、y轴)。  
2️⃣：创建两个数组：_status和_timer，分别表示某人的状态和上次状态改变的时间(天)。  
3️⃣：其中，_status取值为：0-易感染者，1-感染者，2-康复者，3-潜伏者，4-死亡者，5-隔离者  
4️⃣：其他基本设定：潜伏期7天，感染者传染的概率0.5，潜伏者传染的概率0.25，自愈概率0.01，隔离治疗康复概率0.7，感染者的死亡率0.1，隔离后的死亡率0.02，隔离启动时间40天，床位100张，安全距离2.0。

思路：  
1️⃣：使用正态分布模型随机生成count个人的初始位置，初始_status为0，初始_timer为0。  
2️⃣：设定初始感染人数，随机挑选易感染者变为感染者。  
3️⃣：随机生成移动距离和移动意愿(某个人是否移动)，然后和上一次位置进行叠加。  
4️⃣：感染者和潜伏者皆会按照各自的传染概率来感染安全距离以内的若干个易感染者，将其变为潜伏者。  
5️⃣：每一天的状态改变：若某人为感染者，则有几率自愈或死亡；若某人为潜伏者，则过了潜伏期就会变为感染者；若某人为隔离者，则有几率康复或死亡。  
6️⃣：当开启隔离时，若床位有剩余，则把感染者变为隔离者。  
7️⃣：每一天都打印出每个人的位置及状态(除去死亡者和隔离者)。

防疫措施：  
1️⃣：戴口罩，即降低感染率。  
2️⃣：社交距离，即降低安全距离。  
3️⃣：隔离。  

结果：  
1️⃣：初始数据下的结果  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure1_1.png)    
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure1_2.png)  
2️⃣：戴口罩，把感染者和潜伏者的传染概率都减半  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure2_1.png)      
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure2_2.png)  
3️⃣：社交距离，把安全距离从2.0降低为1.5  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure3_1.png)  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure3_2.png)  
4️⃣：隔离，40天的启动期，100张床位  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure4_1.png)  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure4_2.png)  
5️⃣：隔离，20天的启动期，100张床位  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure5_1.png)  
![](https://github.com/SoriveZJQ/2019-ncov/blob/main/Figure5_1.png)
