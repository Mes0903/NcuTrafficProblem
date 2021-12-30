import requests as rq
import gzip
import os
from multiprocessing import Pool

wait_queue = []
domain = "https://tisvcloud.freeway.gov.tw"
parent_url = "/history/motc20/VD/2021122"

def get_request(path: str, day: int, hour: int, min: int, url: str):
    print(url)
    download_response = rq.get(url)
    print(download_response.status_code)
    
    if(download_response.status_code == 200):
        f_in = gzip.decompress(download_response.content).decode()
        with open(path + "/2021122" + str(day) + f"_{hour:02d}{min:02d}" + ".xml", 'w') as file:
            file.write(f_in)


if __name__ == '__main__':
    for day in range(9):
        path = "2021_122" + str(day)
        if not os.path.isdir(path):
            os.mkdir(path)

        for hour in range(24):
            for min in range(60):
                url = domain + parent_url + str(day) + "/VDLive_" + f"{hour:02d}{min:02d}" + ".xml.gz"
                wait_queue.append((path, day, hour, min, url))

    with Pool(20) as pool:
        pool.starmap(get_request, wait_queue)