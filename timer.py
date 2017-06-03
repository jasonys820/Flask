# -- coding: UTF-8 --

import time as t

class Mytimer():
    def __str__(self):
        return self.prompt

    __repr__ = __str__

    # start timer
    def start(self):
        self.start = t.localtime()
        print 'start timer..'

    # stop timer
    def stop(self):
        self.stop = t.localtime()
        self._calc()
        print 'stop timer..'

    # 计算时间
    def _calc(self):
        self.lasted = []
        self.prompt = '总共运行时间'
        for index in range(6):
            self.lasted.append(self.stop[index] - self.start[index])
            self.prompt += str(self.lasted[index])
        print self.prompt