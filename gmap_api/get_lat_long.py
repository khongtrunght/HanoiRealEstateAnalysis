from datetime import datetime
import json
import numpy as np
import pandas as pd
import time
import asyncio
import logging
import argparse
import aiohttp
import attr

LOGGER_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=LOGGER_FORMAT, datefmt="[%H:%M:%S]")
log = logging.getLogger()
log.setLevel(logging.INFO)


API_KEY = "QQUQPZqYkIiEniTsfYkg9X_fm7m3iAsPNVgXu8glsCQ"
FILE_PATH = "resources/data/alo_nha_dat.csv"
SAVE_PATH = "resources/data/alo_nha_dat_lat_long.csv"
request_link = "https://geocode.search.hereapi.com/v1/geocode?q={}&apiKey={}"


def main(FILE_PATH, SAVE_PATH, API_KEY="QQUQPZqYkIiEniTsfYkg9X_fm7m3iAsPNVgXu8glsCQ"):
    if FILE_PATH[-4:] == "xlsx":
        batdongsan_df = pd.read_excel(FILE_PATH)
    elif FILE_PATH[-3:] == "csv":
        batdongsan_df = pd.read_csv(FILE_PATH)
    batdongsan_df = batdongsan_df.assign(lat=0.0, lng=0.0)

    @attr.s
    class Fetch:
        limit = attr.ib()  # batch
        rate = attr.ib(default=5, converter=int)  # speed

        async def make_request_new(self, url, idx):

            async with self.limit:
                async with aiohttp.ClientSession() as session:
                    async with session.request(method="GET", url=url) as response:
                        js = await response.json()
                        try:
                            loc = js["items"][0]["position"]
                            log.info(f"Location {loc} thanh cong")
                        except:
                            log.error(f"url {url} fail")
                            # return {'data': '',}
                        await asyncio.sleep(self.rate)
            return (idx, js)

    async def rate_limit_class(urls, rate, limit):
        limit = asyncio.Semaphore(limit)

        f = Fetch(
            rate=rate,
            limit=limit,
        )

        tasks = []

        for url in urls:
            tasks.append(f.make_request_new(url=url[1], idx=url[0]))

        results = await asyncio.gather(*tasks)

        for json in results:
            if json[1]:
                try:
                    batdongsan_df.loc[json[0], "lat"] = json[1]["items"][0]["position"][
                        "lat"
                    ]
                    batdongsan_df.loc[json[0], "lng"] = json[1]["items"][0]["position"][
                        "lng"
                    ]
                    log.info(f"{json[0]} thanh cong")
                except:
                    log.error(f"json loi {json}")

    request_links = (
        (i, request_link.format(batdongsan_df["address"][i], API_KEY))
        for i in range(batdongsan_df.shape[0])
    )  # batdongsan_df.shape[0]

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(rate_limit_class(urls=request_links, rate=1.1, limit=5))

    if SAVE_PATH[-3:] == "csv":
        batdongsan_df.to_csv(SAVE_PATH, index=False)
    elif SAVE_PATH[-4:] == "xlsx":
        batdongsan_df.to_excel(SAVE_PATH, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", dest="input", default=FILE_PATH)
    parser.add_argument("--output", "-o", dest="output", default=SAVE_PATH)
    args = parser.parse_args()
    main(args.input, args.output)
