from typing import Iterable

from websites import icourses, bilibili, netease, cmooc, coursera, haodaxue, imooc, mooc
import multiprocessing


class Spiders:
    # 网页 -> 抓取函数
    websites_scraping = {
        'icourses': icourses.scraping,
        'bilibili': bilibili.scraping,
        'netease ': netease.scraping,
        'cmooc': cmooc.scraping,
        'coursera': coursera.scraping,
        'haodaxue': haodaxue.scraping,
        'imooc': imooc.scraping,
        'mooc': mooc.scraping,
    }

    @staticmethod
    def err_call_back(err):
        print(f'多进程爬取出错啦~ error：{str(err)}')

    @classmethod
    def scraping(cls, keyword_collections: Iterable[str]):
        """
        请尽量少调用(把待搜索的关键词放一块)，每次抓取都要重新 打开/关闭 浏览器

        已使用多进程优化
        """
        pool = multiprocessing.Pool(8)
        for web in cls.websites_scraping:
            scraping = cls.websites_scraping.get(web)
            pool.apply_async(scraping, (keyword_collections,), error_callback=cls.err_call_back)
            # scraping(keyword_collections)

        pool.close()
        pool.join()


if __name__ == '__main__':
    Spiders.scraping(('python',))
