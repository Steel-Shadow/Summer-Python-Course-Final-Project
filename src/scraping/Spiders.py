import os
import time
from typing import Iterable

import multiprocessing
import openpyxl

from .websites import icourses, bilibili, netease, cmooc, ke, haodaxue, imooc, mooc


# from .websites import bilibili, cmooc, ke, haodaxue, imooc, mooc


class Spiders:
    # 网页 -> 抓取函数
    web_scraping = {
        'icourses': icourses.scraping,
        'bilibili': bilibili.scraping,
        'netease': netease.scraping,
        'cmooc': cmooc.scraping,
        # 'coursera': coursera.scraping, # 不稳定，弃用
        'ke': ke.scraping,
        'haodaxue': haodaxue.scraping,
        'imooc': imooc.scraping,
        'mooc': mooc.scraping,
    }

    @staticmethod
    def err_call_back(err):
        print(f'多进程爬取出错啦~ error：{str(err)}')

    @staticmethod
    def task(shared_dict, web: str, keyword: str):
        sub_scraping = Spiders.web_scraping.get(web)
        shared_dict[(web, keyword)] = sub_scraping(keyword)

    @classmethod
    def close(cls):
        bilibili.driver_quit()
        cmooc.driver_quit()
        ke.driver_quit()
        haodaxue.driver_quit()
        imooc.driver_quit()
        mooc.driver_quit()
        icourses.driver_quit()
        netease.driver_quit()

    @classmethod
    def scraping(cls, keywords: Iterable[str]) -> dict:
        """
        请尽量少调用(把关键词放一块)，每次抓取都要重新打开、关闭浏览器
        :return: dict.key是tuple[网页名,关键词] dict.value是list[tuple[标题,链接]]
        """
        start_time = time.time()

        pool = multiprocessing.Pool(8)
        manager = multiprocessing.Manager()

        # 网页 -> 抓取信息 多进程共享
        shared_dict = manager.dict()

        for k in keywords:
            for web in cls.web_scraping:
                # 爬取任务加入进程池
                pool.apply_async(cls.task, (shared_dict, web, k), error_callback=cls.err_call_back)

        pool.close()
        pool.join()
        end_time_0 = time.time()
        print('没有关闭浏览器耗时 ' + str(end_time_0 - start_time))
        cls.close()
        end_time_1 = time.time()
        print('关闭浏览器耗时 ' + str(end_time_1 - start_time))
        return shared_dict


def main():
    """
    修改words为要爬取的关键词，运行完毕后生成 scraping.txt，文件呈树状结构
    scraping.txt结构解释：
    关键词前无空格，平台(共8个)前有1个空格，课程信息(课程名 链接)前有2个空格
    若 关键字 网页 爬取结果为空，则显示'  Empty'，前有2个空格
    """
    # with open(os.path.join(os.path.dirname(__file__), 'CS_KG.txt'), encoding='utf-8') as in_file:
    #     graph = in_file.readlines()

    # words = list()

    # for line in graph:
    #     words.append(line.strip())
    words = ['面向对象']

    start_time = time.time()
    res = Spiders.scraping(words)
    end_time = time.time()
    print(end_time - start_time)

    # 创建一个新的工作簿
    workbook = openpyxl.Workbook()

    # 选择默认的活动工作表
    sheet = workbook.active

    for row in range(1, len(words) + 1):
        # 第一列 关键词
        keyword = words[row - 1]
        sheet.cell(row=row, column=1, value=keyword)
        column = 1
        for w in Spiders.web_scraping:  # 网页
            courses = res.get((w, keyword))

            if not courses:
                continue

            for course in courses:  # 课程
                unit = ''
                for info in course:  # 课程各个信息
                    unit += info + ','
                column += 1
                sheet.cell(row, column, unit)

    # 保存工作簿
    workbook.save("scraping_offline.xlsx")

    # 关闭工作簿
    workbook.close()


if __name__ == '__main__':
    main()
