import urllib
import urllib2

url = 'http://cs302.pythonanywhere.com/report?'
values = {'username' : 'rdso323',
          'password' : '8F61A0B4911467540CD6DF03E59E40D041323BC8BEB1A3744E22BF4E7458B869',
          'location' : '2',
          'ip' : '10.0.2.15',
          'port' : '10007',
          'enc' : '0'}

try:
    data = urllib.urlencode(values)
    respdata = urllib2.urlopen(url+data).read()
    print(respdata)

except Exception as e:
    print(str(e))

    # data = data.encode('utf-8')
    # req = urllib2.Request(url,data)
    # resp = urllib2.urlopen(req)
    # respData = resp.read()