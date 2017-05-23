# -*- coding: utf-8 -*-
"""
    Context存储了回测设定与历史数据, 别的类都对其进行了引用, 方便别的类读取设定与数据.
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import data


#==============================================================================
class Context(object):
    """全局变量.

    存储了程序设定与历史数据.

    Attributes:
        path: 工作目录.
        start: 回测开始日期.
        end: 回测结束日期.
        m: 分组回测数量.
        bench: 比较基准.
        fee: 佣金.
        calendar: 日历数据.
        basic: 基本信息.
        bar: 行情数据.
        month: 月度数据.
        ttm: TTM财务数据.
        quarter: 季度财务数据.
        index: 指数数据.
        stocks: 股票池.
        dates: 回测交易日历.
        nv_portfolio: 分组组合累计净值.
        nv_hedge: 分组对冲累计净值.

    Methods:
        load_data: 载入数据.
    """

    def __init__(self, path, start, end, m, bench, fee):
        self.path = path
        self.start = start
        self.end = end
        self.m = m
        self.bench = bench
        self.fee = fee

    def load(self):
        """载入历史数据.

        包括日历数据、基本信息、行情数据、月度数据、TTM财务数据、季度财务数据和指数数据.
        载入数据后再生成股票池、交易日历.

        Args:
            None.

        Returns:
            历史数据.

        Raises:
            None.
        """
        # 日历数据
        self.calendar = data.Calendar(self.path)
        self.calendar.load()
        self.calendar.get_period_date(self.start, self.end)
        # 基本信息
        self.basic = data.Basic(self.path)
        self.basic.load()
        # 行情数据
        self.bar = data.Bar(self.path)
        self.bar.load()
        # 月度数据
        self.month = data.Month(self.path)
        self.month.load()
        # TTM财务数据
        self.ttm = data.Ttm(self.path)
        self.ttm.load()
        # 单季度财务数据
        self.quarter = data.Quarter(self.path)
        self.quarter.load()
        # 指数数据
        self.index = data.Index(self.path)
        self.index.load()
        # 股票池
        self.stocks = self.bar.close.columns
        # 回测交易日历
        self.dates = self.calendar.all_dates
        # 回测历史统计
        self.portfolio_nv_his = pd.DataFrame(index=self.dates,
                                             columns=np.arange(1, self.m + 1, 1))
        self.hedge_nv_his = pd.DataFrame(index=self.dates,
                                         columns=np.arange(1, self.m + 1, 1))

    def update(self, portfolio, n):
        """一组回测完成后更新分组组合累计净值与分组对冲累计净值.

        Args:
            portfolio: 组合持仓.
            n: 第n组回测.

        Returns:
            更新分组组合累计净值与分组对冲累计净值.

        Raises:
            None.
        """
        self.portfolio_nv_his[n] = portfolio.nv_his
        self.hedge_nv_his[n] = portfolio.hedge_nv_his

    def plot(self):
        """全部回测完成后画图.

        Args:
            None.

        Returns:
            分组组合累计净值与分组对冲累计净值图.

        Raises:
            None.
        """
        #======================================================================
        plt.figure()
        fig = self.portfolio_nv_his.plot(grid=True, legend=False, figsize=(9, 6),
                                         title='portfolio_nv_his').get_figure()
        fig.savefig(self.path + '\\output\\portfolio_nv.png',
                    dpi=100, bbox_inches='tight')
        #======================================================================
        plt.figure()
        fig = self.hedge_nv_his.plot(grid=True, legend=False, figsize=(9, 6),
                                     title='hedge_nv_his').get_figure()
        fig.savefig(self.path + '\\output\\hedge_nv.png',
                    dpi=100, bbox_inches='tight')

    def save(self):
        """全部回测完成后保存数据.

        Args:
            None.

        Returns:
            保存分组组合累计净值与分组对冲累计净值.

        Raises:
            None.
        """
        self.portfolio_nv_his.to_csv(self.path + '\\output\\portfolio_nv.csv')
        self.hedge_nv_his.to_csv(self.path + '\\output\\hedge_nv.csv')






