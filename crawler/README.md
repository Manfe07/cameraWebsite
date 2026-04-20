# CameraCrawler

This is a python script, to crawl images from network cameras and creat a timelapse every night.

## Sample cameras.yaml
```yaml
- name: "Dummy" # name of camera
  url: "" # camera-image url
  interval: 5 # Capture intervall in minutes
  timelapse: True # create timelapse every night
  website: 
   picture: True # display camera on website
   timelapse: True # display timelapse on website
   
- name: "Dummy"
  url: ""
  interval: 5
  timelapse: True
  website:
   picture: True
   timelapse: True

```

## Sample docker-compose.yml
```yaml
version: '3.4'

services:
  cam-flask:    
    image: registry.mnl-fhrn.de/lsrg/camerawebsite:latest
    restart: unless-stopped

    volumes:
      - ./cam/logs:/logs:rw
      - ./cam/output:/static/output:ro
      - /etc/localtime:/etc/localtime:ro
    environment:
      - TZ="Europe/Berlin"
    
    command: gunicorn -w 1 
            -b :8000 app:app \
            --access-logfile ./logs/log.txt \
            --log-level info \
            --timeout 90 \
            --workers 25 \
            --worker-class gevent

    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.cam.rule=Host(`cam.domain.com`)"
      - "traefik.http.routers.cam.entrypoints=websecure"
      - "traefik.http.services.cam.loadbalancer.server.port=8000"
      - "traefik.http.routers.cam.service=cam"
      - "traefik.http.routers.cam.tls.certresolver=production"
    networks:
      - traefik_default

    
  cam-crawler:
    image: registry.mnl-fhrn.de/lsrg/cameracrawler:latest
    restart: unless-stopped

    volumes:
      - ./cam/timelapse:/archive:rw
      - ./cam/output:/output:rw
      - ./cam/config:/config:ro
      - /etc/localtime:/etc/localtime:ro
    command: python app.py

networks:
  traefik_default:
    external: true
```