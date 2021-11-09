import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'alonhadat',
            '-o',
            '../resources/alo_nha_dat.csv',
        ]
    )
except SystemExit:
    pass
