#_*_ecoding:utf8_*_

#demo1
url=input("input url:")     #user/say
urls=url.split("/")
user=__import__(urls[0]);
say=getattr(user,urls[1]);
say()

#demo2

