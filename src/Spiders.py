from typing import Iterable, Dict, Any

from websites import icourses, bilibili, netease, cmooc, coursera, haodaxue, imooc, mooc
import multiprocessing


class Spiders:
    # 网页 -> 抓取函数
    web_scraping = {
        'icourses': icourses.scraping,
        'bilibili': bilibili.scraping,
        'netease': netease.scraping,
        'cmooc': cmooc.scraping,
        'coursera': coursera.scraping,
        'haodaxue': haodaxue.scraping,
        'imooc': imooc.scraping,
        'mooc': mooc.scraping,
    }

    @staticmethod
    def err_call_back(err):
        print(f'多进程爬取出错啦~ error：{str(err)}')

    @staticmethod
    def task(shared_dict, web: str, keywords: Iterable[str]):
        scraping = Spiders.web_scraping.get(web)
        gen_scraping = scraping(keywords)

        # yield迭代返回 每次返回单个 keyword 的爬取结果
        iter_keywords = iter(keywords)
        for iter_scraping in gen_scraping:
            shared_dict[(web, next(iter_keywords))] = iter_scraping

    @classmethod
    def scraping(cls, keywords: Iterable[str]) -> dict:
        """
        请尽量少调用(把关键词放一块)，每次抓取都要重新打开、关闭浏览器
        :return: dict.key是tuple[网页名,关键词] dict.value是list[tuple[标题,链接]]
        """
        pool = multiprocessing.Pool()
        manager = multiprocessing.Manager()

        # 网页 -> 抓取信息 多进程共享
        shared_dict = manager.dict()

        for web in cls.web_scraping:
            # 爬取任务加入进程池
            pool.apply_async(cls.task, (shared_dict, web, keywords), error_callback=cls.err_call_back)

        pool.close()
        pool.join()
        return shared_dict


if __name__ == '__main__':
    '''
    修改words为要爬取的关键词，运行完毕后生成 scraping.txt，文件呈树状结构
    scraping.txt结构解释：
    关键词前无空格，平台(共8个)前有1个空格，课程信息(课程名 链接)前有2个空格
    若 关键字 网页 爬取结果为空，则显示'  Empty'，前有2个空格 
    '''
    words = ('计算机组成', '面向对象', '操作系统')
    res = Spiders.scraping(words)

    with open('scraping.txt', 'w', encoding='utf-8') as out_file:
        for k in words:  # 关键词
            out_file.write(f'{k}\n')
            for w in Spiders.web_scraping:  # 网页
                out_file.write(f' {w}\n')
                courses = res.get((w, k))

                if not courses:
                    out_file.write('  Empty\n')

                for course in courses:  # 课程
                    for info in course:  # 课程各个信息
                        out_file.write(f'  {info}')
                    out_file.write('\n')
