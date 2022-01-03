import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'batdongsan',
            '-o',
            '../resources/data/web1.csv',
        ]
    )
except SystemExit:
    pass
