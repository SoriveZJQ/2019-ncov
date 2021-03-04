import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class People(object):
    def __init__(self, count=1000, first_infected_count=3):
        self.count = count
        self.first_infected_count = first_infected_count
        self.data = []
        self.sepCount = 0  # 隔离人数

        self.init()

    def init(self):
        self._people = np.random.normal(0, 100, (self.count, 2))
        self.reset()

    def reset(self):
        self._round = 0
        self._status = np.array([0] * self.count)
        self._timer = np.array([0] * self.count)
        self.random_people_state(self.first_infected_count, 1)

    def random_people_state(self, num, state=1):
        """随机挑选人设置状态
        """
        assert self.count > num
        # TODO：极端情况下会出现无限循环
        n = 0
        while n < num:
            i = np.random.randint(0, self.count)
            if self._status[i] == state:
                continue
            else:
                self.set_state(i, state)
                n += 1

    def set_state(self, i, state):
        self._status[i] = state
        # 记录状态改变的时间
        self._timer[i] = self._round

    def random_movement(self, width=1):
        """随机生成移动距离

        :param width: 控制距离范围
        :return:
        """
        return np.random.normal(0, width, (self.count, 2))

    def random_switch(self, x=0.):
        """随机生成开关，0 - 关，1 - 开

        x 大致取值范围 -1.99 - 1.99；
        对应正态分布的概率， 取值 0 的时候对应概率是 50%
        :param x: 控制开关比例
        :return:
        """
        normal = np.random.normal(0, 1, self.count)
        switch = np.where(normal < x, 1, 0)
        return switch

    @property
    def healthy(self):
        return self._people[self._status == 0]

    @property
    def infected(self):
        return self._people[self._status == 1]

    @property
    def confirmed(self):
        return self._people[self._status == 2]

    @property
    def exposed(self):
        return self._people[self._status == 3]

    @property
    def died(self):
        return self._people[self._status == 4]

    @property
    def separated(self):
        return self._people[self._status == 5]

    def move(self, width=1, x=.0):
        movement = self.random_movement(width=width)
        # 限定特定状态的人员移动
        switch = self.random_switch(x=x)
        # movement[(self._status == 0) | switch == 0] = 0
        movement[switch == 0] = 0
        self._people = self._people + movement  # x、y轴各自移动

    def change_state(self, x1=0.6, x2=0.01, x3=0.1, x4=0.7, x5=0.02):  # 潜伏者、感染者，x1-潜伏者变为感染者，x2-自愈，x3-感染死亡，x4-治疗，x5-隔离死亡
        for i in range(self.count):
            if self._status[i] == 0 | self._status[i] == 2 | self._status[i] == 4:
                continue
            if self._status[i] == 1:  # 感染者
                if np.random.rand(1)[0] <= x2:
                    self._status[i] = 2
                    self._timer[i] = self._round
                elif np.random.rand(1)[0] <= x3:
                    self._status[i] = 4  # 死亡
                    self._timer[i] = self._round
            if self._status[i] == 3:  # 潜伏者
                if self._round - self._timer[i] >= 7:  # 潜伏期为7天
                    self._status[i] = 1  # 变为感染者
                    self._timer[i] = self._round
                # else:
                #     if np.random.rand(1)[0] <= x1:
                #         self._status[i] = 1  # 变为感染者
                #         self._timer[i] = self._round

            if self._status[i] == 5:  # 隔离者
                if np.random.rand(1)[0] <= x4:  # 康复
                    self._status[i] = 2
                    self._timer[i] = self._round
                    self.sepCount -= 1
                elif np.random.rand(1)[0] <= x5:
                    self._status[i] = 4
                    self._timer[i] = self._round
                    self.sepCount -= 1

    def separate(self, day=20, beds=300):
        if self._round < day:
            return
        cnt1 = len(self._status[self._status == 1])  # 感染者人数
        cnt2 = beds - self.sepCount  # 剩余床位
        cnt = min(cnt1, cnt2)
        self.sepCount += cnt
        k = 0
        for i in range(self.count):
            if self._status[i] == 1:
                self._status[i] = 5
                self._timer[i] = self._round
                k += 1
            if k > cnt:
                break

    def affect(self):
        self.infect_possible_infected(x=0.5, safe_distance=2.0)
        self.infect_possible_exposed(x=0.25, safe_distance=2.0)

    def infect_possible_infected(self, x=0.05, safe_distance=2.0):  # x-感染率
        """按概率感染接近的健康人"""
        for inf in self.infected:
            dm = (self._people - inf) ** 2
            # d = dm.sum(axis=1) ** 0.5
            d = dm.sum(axis=1) ** 0.5
            sorted_index = d.argsort()   # 将d中的元素从小到大排列，提取其对应的index(索引)
            for i in sorted_index:
                if d[i] >= safe_distance:
                    break  # 超出范围，不用管了
                if self._status[i] > 0:
                    continue
                if np.random.rand(1)[0] > x:
                    continue
                self._status[i] = 3  # 感染为潜伏者
                # 记录状态改变的时间
                self._timer[i] = self._round

    def infect_possible_exposed(self, x=0.05, safe_distance=2.0):
        """按概率感染接近的健康人"""
        for inf in self.exposed:
            dm = (self._people - inf) ** 2
            # d = dm.sum(axis=1) ** 0.5
            d = dm.sum(axis=1) ** 0.5
            sorted_index = d.argsort()   # 将d中的元素从小到大排列，提取其对应的index(索引)
            for i in sorted_index:
                if d[i] >= safe_distance:
                    break  # 超出范围，不用管了
                if self._status[i] > 0:
                    continue
                if np.random.rand(1)[0] > x:
                    continue
                self._status[i] = 3  # 感染为潜伏者
                # 记录状态改变的时间
                self._timer[i] = self._round

    def over(self):
        return len(self.healthy) == 0

    def report(self):
        plt.clf()
        # plt.grid(False)
        p1 = plt.scatter(self.healthy[:, 0], self.healthy[:, 1], s=1, c='green')
        p2 = plt.scatter(self.infected[:, 0], self.infected[:, 1], s=1, c='red')
        p3 = plt.scatter(self.confirmed[:, 0], self.confirmed[:, 1], s=1, c='blue')
        p4 = plt.scatter(self.exposed[:, 0], self.exposed[:, 1], s=1, c='yellow')
        # plt.scatter(self.separated[:, 0], self.separated[:, 1], s=1, c='black')

        plt.legend([p1, p2, p3, p4], ['healthy', 'infected', 'confirmed', 'exposed'], loc='upper right', scatterpoints=1)
        t = "Round: %s, Healthy: %s, Infected: %s, Confirmed: %s, Exposed: %s, Separated: %s, Died: %s" % \
            (self._round, len(self.healthy), len(self.infected), len(self.confirmed), len(self.exposed), len(self.separated), len(self.died))
        # plt.text(-400, 400, t, ha='left', wrap=True)
        plt.title(t)
        plt.xlim((-400, 400))
        plt.ylim((-400, 400))
        self.data.append([self._round, len(self.healthy), len(self.infected), len(self.confirmed), len(self.exposed), len(self.died)])


    def result(self):
        self.data = np.array(self.data)
        plt.figure()
        plt.plot(self.data[:, 0], self.data[:, 1], '-g', label='Healthy')
        plt.plot(self.data[:, 0], self.data[:, 2], '-r', label='Infected')
        plt.plot(self.data[:, 0], self.data[:, 3], '-b', label='Confirmed')
        plt.plot(self.data[:, 0], self.data[:, 4], '-y', label='Exposed')
        plt.plot(self.data[:, 0], self.data[:, 5], '-k', label='Died')
        plt.xlabel('Round')
        plt.ylabel('Number')
        plt.legend()
        plt.show()
        plt.pause(100000)

    def update(self):
        """每一次迭代更新"""
        self.affect()
        self.change_state()
        # self.separate(40, 100)
        self.move(3, 1.99)
        self._round += 1
        self.report()


if __name__ == '__main__':
    np.random.seed(1)
    # fig = plt.figure(figsize=(15, 15), dpi=85)
    plt.ion()
    p = People(5000, 10)
    for i in range(100):
        p.update()
        # p.report()
        plt.pause(.001)
    p.result()
    plt.pause(100000)




##### 参考自：https://www.cnblogs.com/davyyy/p/12307441.html #####
