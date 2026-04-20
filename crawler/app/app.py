from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
import os
from pathlib import Path
import shutil
from PIL import Image
import requests
import atexit
import yaml
import timelaps

os.environ['TZ'] = "Europe/Berlin"
time.tzset()

sched = BackgroundScheduler(daemonic=True)

with open("config/cameras.yaml", "r") as yamlfile:
    yaml = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("camera config read successful")
#print(yaml)

def compress(src,dst):
    
    filepath = os.path.join(os.getcwd(), src)

    image = Image.open(filepath)
    
    image = image.resize((image.width // 2, image.height // 2), Image.LANCZOS)

    image.save(src,
                 "JPEG",
                 optimize = True,
                 quality = 90)

    shutil.copyfile(src, dst)

    return



def crawl_image(url, name):
    ct = datetime.datetime.now()
    
    file_path = "archive/" + name + "/" + ct.strftime("%Y%m%d")
    file_name = name + "_" + ct.strftime("%Y%m%d_%H%M%S") + ".jpg"

    staticPath = "output"

    print('Started Image Downloaded: ',url)
    Path(file_path).mkdir(parents=True, exist_ok=True)
    Path(staticPath).mkdir(parents=True, exist_ok=True)

    # Download image
    try:
        res = requests.get(url, stream = True, auth=('admin', 'hackerspace'))
        if res.status_code == 200:
            with open(os.path.join(file_path,file_name),'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',os.path.join(file_path,file_name))
            compress(os.path.join(file_path,file_name), staticPath + "/" + name + ".jpg")

            original_size = os.path.getsize(os.path.join(file_path,file_name))
            compressed_size = os.path.getsize(staticPath + "/" + name + ".jpg")

            print("Original Size: ", original_size)
            print("Compressed Size: ", compressed_size)
            print("New image at:-", ct)
            print()

        else:
            print("URL - Error:", url)
            return -1
    except Exception as e:
        print(e)

   

def createTimelapsYesterday(name):
    yesterday = datetime.datetime.now()- datetime.timedelta(days=1)
    timelaps.createTimelaps(name=name,date=yesterday.strftime("%Y%m%d"))


def addJob(name, url, minutes):
    sched.start()
    
    #create backgroundTask for each camera
    for camera in yaml:
        sched.add_job(crawl_image,'interval',[camera["url"], camera["name"]],minutes=camera["interval"],max_instances=1, id=camera["name"] + " - crawler")
        crawl_image(camera["url"], camera["name"])
        if camera["timelapse"]:
            sched.add_job(createTimelapsYesterday,'cron',[camera["name"]], hour='01',max_instances=1, id=camera["name"] + " - timelapse")
            createTimelapsYesterday(camera["name"])

    #atexit.register(lambda: scheduler.shutdown())
    print(camera["name"], "--- was added with", camera["interval"], "minutes interval")


def initCrawler():
    atexit.register(stopCrawler)
    url_kantine = "http://192.168.187.80/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=smart&password=DwyU8AfK2p2PKT"
    addJob("kantine", url_kantine, 5)


def stopCrawler():
    sched.shutdown(wait=True)

if __name__ == '__main__':
    initCrawler()
    while(True):
        time.sleep(1)
        pass


