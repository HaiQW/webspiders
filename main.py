__requires__ = 'Scrapy==0.24.4'
from pkg_resources import load_entry_point

if __name__ == '__main__':
    argv = ["scrapy", "crawl", "weibo", "-a", "name=15557106533", "-a", "password=wenghaiqin", "-a", "uid=3856926178"]
    load_entry_point('Scrapy==0.24.4', 'console_scripts', 'scrapy')(argv)

