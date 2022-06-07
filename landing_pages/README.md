

## Install
Installation is quite simple
```
docker run -d -p 5000:80 --restart always internetofwater/pygeoapi-geoconnex:latest
docker run -d --name watchtower -v /var/run/docker.sock:/var/run/docker.sock --restart always containrrr/watchtower -i 30 --cleanup
```
