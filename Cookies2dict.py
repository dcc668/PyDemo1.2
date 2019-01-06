#!  /usr/bin/env python
#ecoding=utf-8
if __name__=='__main__':
    cookieStr = "MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1; mm_lang=zh_CN; webwxuvid=bd2a6d577d3e5a497c2ec36c562a3b111d81e1e0311d65fdad5d14ee8d4f2a49950af8eaa5aa8d7e85ded3f943c724b0; webwx_auth_ticket=CIsBEMbl7hIagAEi+BM6jGIGp/yTjZOwTvt2/gnw4SlAIsWTTWwddO0alA0dGKF7dWGBBpPzSxbx1HJSH6/Kl0rUuTlFBBCDuiXW1GoVnf20ZyuNxS3ASvLtsmoKxCwiQu8UZO9DZTbhX5drgz0NKPDetNImLv0oifb3xBy50RAT578qZ5KnrP4wMA==; login_frequency=1; last_wxuin=1874818113; wxloadtime=1512975906_expired; wxpluginkey=1512954002; wxuin=1874818113; wxsid=CBktnMZBq1zxZXHc; webwx_data_ticket=gSc62p27ViXvMe+wyJ9au+fB"
    cookies=dict(item.split('=')for item in cookieStr.split(';'))