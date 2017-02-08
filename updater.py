import urllib2
from urllib2 import HTTPError, URLError
import re

cfg_file = 'dnsexit.conf'
ip_file = 'dnsexit-ip.txt'


def get_ip(servers):
    p = re.compile('\D*(\d+\.\d+\.\d+\.\d+).*')
    for server in servers:
        url='http://' + server
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req)
            content = res.read()
            a = p.findall(content)
            if len(a) <= 0:
                print "Return message format error.... Fail to grep the IP address from " + url
                print "response " + content
            else:
                ip = a[0]
                print url + " says your IP address is: " + ip
                return ip

        except HTTPError as e:
             print 'Error calling ' + url+ ' Error code: '+ e.code
        except URLError as e:
             print 'Error calling '+ url+ ' Error reason: '+ e.reason
    return None


def is_ip_changed(ip):
    fip = open(ip_file, 'r')
    old_ip = fip.read()
    fip.close()
    return old_ip != ip


def send_new_ip(cfg, ip):
    url = cfg['url']
    posturl = "%s?login=%s&password=%s&host=%s&myip=%s" % (url,cfg['login'],cfg['password'],cfg['host'],ip)

    print posturl
    req = urllib2.Request(posturl)
    try:
        res = urllib2.urlopen(req)
        content = res.read()
        print "Response from " + url +" : " + content
        p = re.compile('(\d+)=')
        a = p.findall(content)
        if len(a) <= 0:
                print "Return message format error.... " + content
        else:
            return int(a[0])

    except HTTPError as e:
         print 'Error calling ' + url+ ' Error code: '+ e.code
    except URLError as e:
         print 'Error calling '+ url+ ' Error reason: '+ e.reason


f = open(cfg_file, 'r')
lines = f.readlines();
f.close()

lines = map(lambda x: x.strip().split("="), lines)
cfg = {l[0]:l[1] for l in lines}
proxyservs = cfg['proxyservs'].split(";")

ip = get_ip(proxyservs)

if not is_ip_changed(ip):
   print "IP  didn't change since last update"
else:
    ret = send_new_ip(cfg, ip)
    if ret == 0:
        print "Success!"
        fip = open(ip_file, 'w')
        fip.write(ip)
        fip.close()
        print "IP cached in " + ip_file
    else:
        print "ERROR :("





