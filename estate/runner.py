import os
from scrapy.cmdline import execute
from argparse import ArgumentParser

os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = ArgumentParser()
parser.add_argument("--scrape", "-s", dest="scrape", default='alonhadat')
parser.add_argument("--output", "-o", dest="output", default='../resources/test.csv')

args = parser.parse_args()


try:
    execute(
        [
            'scrapy',
            'crawl',
            args.scrape,
            '-o',
            args.output,
        ]
    )
except SystemExit:
    pass
