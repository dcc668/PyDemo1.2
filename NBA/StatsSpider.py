#!  /usr/bin/env python
#ecoding=utf-8
import  requests,time
import traceback
import json,random
from NBA.utils.ecoding_utils import EncodingUtils

class Spider():
    def __init__(self):
        self.ips=[]
        with open('ips/ips.txt','r',encoding='utf-8') as file:
            lines=file.readlines()
            for line in lines:
                self.ips.append(line.strip())
        print('>>>>>>>>>>>>>>>>>>>>>>>>>ips>>>>>>>>>>>>>>>>>>>>>>>>>'+str(self.ips))
    def get_proxy(self):
        website='http://'+random.choice(self.ips)
        return {
            'http':website,
        }
    def download_page(self,main_url,headers,retry_count=4):
        html=''
        retry=0
        while(retry<retry_count):
            try:
                print('Request:'+main_url)
                if retry==0:
                    response=requests.get(main_url,headers=headers,timeout=15)
                    if 200==response.status_code:
                        return EncodingUtils.getStrNotKnowEcoding(response.content)
                print("第："+str(retry)+" 次尝试请求")
                response=requests.get(main_url,headers=headers,proxies=self.get_proxy(),timeout=15)
                if 200==response.status_code:
                    return response.text
                else:
                    print('请求失败，返回码：'+str(response.status_code))
                    retry=retry+1
            except Exception as e:
                traceback.print_exc()
                retry=retry+1
                time.sleep(1)
            time.sleep(1)
        return html

if __name__=="__main__":
    spider=Spider()
    #赛季，球队，球员统计信息（http://stats.nba.com/teams/  界面,分析抓包 /js/data/ptsd/stats_ptsd.js）
    print('-----------------------获取统计信息----------------------')
    stats_url="http://stats.nba.com/js/data/ptsd/stats_ptsd.js"
    stats_headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://stats.nba.com/teams/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_ga=GA1.2.948953079.1521877673; ug=5ab602a80cda7c0a3c0101093300d02e; __gads=ID=a25f753a23986b4f:T=1521877682:S=ALNI_MaueWiR5SpgNoJf2Cvhty2cEs7cgw; s_fid=62873FC7BFF06232-36D3F04B762090A3; s_vi=[CS]v1|2D5B01808530E486-4000030860002A97[CE]; check=true; s_cc=true; ugs=1; _gid=GA1.2.1411142238.1522467246; ak_bmsc=DC5975E5369CAA9B3C07253A0CD0837E1720144D2E7800007320BF5AB81EE538~plCYuljtl4HlD5FmrCofG2vC8D1Yw01VF1BZ7RqGGeuq+qwYb6M4151RgXtk74gqR+kD6wSYZ7UAgNCnArhiG8fzhRdcR6gb+vMLt7cJjOtXk0UTZwTSlUcyG860xtgDo1GOIictd0KeSUFITOkCVa7RwCfvIIY8h2O3wD0UgfyHp6O4MQY6/6Gxvz78NApkhVlcf6KZO153cF2qu8zv38MZPUtc5sAYY3XpFWNm+r6qg=; s_sq=%5B%5BB%5D%5D; bm_sv=E9D8E9996843CB2A0CF5AFECFE9A348B~BklCRYU2QP79L86YbWj6xWthqj/WfPy8tlCKnz7nUUra3/SlfYg2EVsKXTvgh7YlljUP2/PcrYxgQ/lP+SlXfcptIMB2qaJQ9rpC6XaFHBiNEicwHU7y63VNv1wO0XdOUkwcL2RqASvagGJ+MYBPuQ==; _gat=1; mbox=PC#7e1af7207b244561823a002500b1292b.24_11#1585122479|session#c50c5baf930b4d76816c75171e4b42cf#1522479979',
    }
    rtn_json=spider.download_page(stats_url,stats_headers)
    json_str=rtn_json.split(" = ")[1].split(';')[0]
    print('return:'+json_str)
    json_obj=json.loads(json_str)
    print('teams_count:'+str(json_obj["teams_count"]))
    print('seasons_count:'+str(json_obj["seasons_count"]))
    #提取球队Id
    teams=json_obj["data"]["teams"]
    team_ids=[team[0] for team in teams]
    print(str(len(team_ids)))
    '''统计信息返回格式如下'''
    # var stats_ptsd = {
    #     "generated": "2018-03-31T02:00:03-04:00",
    #     "seasons_count": 54,
    #     "teams_count": 66,
    #     "players_count": 4280,
    #     "data": {
    #         "seasons": [
    #             ["leagueMatchups", "00", 2017, 2, 2017, []],
    #             ["schedule", "00", 2017, 2, 2016, [
    #                 ["hidePrev", true, "Y"],
    #                 ["initialMonth", false, "12"]
    #             ]],
    #             ["summerleague", "00", 2017, 2, 2016, [
    #                 ["month", true, "7"],
    #                 ["isActive", true, "15"],
    #                 ["hasDaily", true, "15"]
    #             ]],
    #             ["draftboard", "00", 2017, 2, 2017, [
    #                 ["isActive", true, ""],
    #                 ["isLive", false, ""]
    #             ]],
    #             ["DraftCombineLanding", "00", 2017, 2, 2014, []],
    #             ["standings", "00", 2017, 2, 1970, []],
    #             ["trackingStats", "00", 2017, 2, 2013, []],
    #             ["transactions", "00", 2017, 2, 2015, []],
    #             ["playtypeStats", "00", 2017, 2, 2015, []],
    #             ["teamVsPlayerStats", "00", 2017, 2, 2001, []],
    #             ["playerVsPlayerStats", "00", 2017, 2, 2001, []],
    #             ["teamTracking", "00", 2017, 2, 2013, []],
    #             ["teamStats", "00", 2017, 2, 1996, []],
    #             ["teamRoster", "00", 2017, 2, 1951, []],
    #             ["teamPlayer", "00", 2017, 2, 1996, []],
    #             ["teamOnOffCourt", "00", 2017, 2, 1996, []],
    #             ["teamLineups", "00", 2017, 2, 2007, []],
    #             ["teamGameLogs", "00", 2017, 2, 1996, []],
    #             ["teamProfile", "00", 2017, 2, 1951, []],
    #             ["playoffBracket", "00", 2016, 4, 2014, []],
    #             ["playerUpcomingGames", "00", 2017, 2, 2015, []],
    #             ["playerTracking", "00", 2017, 2, 2013, []],
    #             ["playerStats", "00", 2017, 2, 1996, []],
    #             ["playerFantasy", "00", 2017, 2, 2014, []],
    #             ["playerGamelogs", "00", 2017, 2, 1996, []],
    #             ["playerProfile", "00", 2017, 2, 1951, []],
    #             ["playerList", "00", 2017, 2, 1996, []],
    #             ["leagueGameHustle", "00", 2017, 2, 2015, []],
    #             ["leagueTeamHustle", "00", 2017, 2, 2015, []],
    #             ["leaguePlayerHustle", "00", 2017, 2, 2015, []],
    #             ["leagueHustleLeaders", "00", 2017, 2, 2015, []],
    #             ["leagueDefensiveLeaders", "00", 2017, 2, 2015, []],
    #             ["leadersAllTime", "00", 2017, 2, 1951, []],
    #             ["leadersCurrent", "00", 2017, 2, 1946, []],
    #             ["leaderTiles", "00", 2016, 2, 1996, []],
    #             ["homepageLeaders", "00", 2017, 2, 1996, []],
    #             ["leagueTrackingStats", "00", 2017, 2, 2013, []],
    #             ["leagueTeamStats", "00", 2017, 2, 1996, []],
    #             ["leaguePlayerStats", "00", 2017, 2, 1996, []],
    #             ["leagueLineups", "00", 2017, 2, 2007, []],
    #             ["leagueGameLogs", "00", 2017, 2, 1946, []],
    #             ["DraftHistory", "00", 2017, 2, 1947, []],
    #             ["DraftCombineSpotUp", "00", 2017, 2, 2014, []],
    #             ["DraftCombineNonstationary", "00", 2017, 2, 2014, []],
    #             ["DraftCombineSummary", "00", 2017, 2, 2000, []],
    #             ["DraftCombineAnthro", "00", 2017, 2, 2000, []],
    #             ["DraftCombineAgility", "00", 2017, 2, 2000, []],
    #             ["boxscorePlayByPlay", "00", 2017, 2, 1996, []],
    #             ["boxscoreTracking", "00", 2017, 2, 2014, []],
    #             ["boxscoreCharts", "00", 2017, 2, 2015, []],
    #             ["leagueAllstar", "00", 2015, 3, 1996, []],
    #             ["allstar", "00", 2015, 3, 1996, []],
    #             ["allstarRoster", "00", 2015, 3, 1950, []],
    #             ["site", "00", 2017, 2, 1996, [
    #                 ["isHustleMenuActive", true, ""],
    #                 ["showHomepageLinks", true, ""],
    #                 ["showDailyLeaders", true, ""]
    #             ]]
    #         ],
    #         "teams": [
    #             ["15016", "MEL", "united", "Melbourned", "United", 0, 0, 1, 2017, 1, ["#dd3333", "#1e73be"]],
    #             ["12329", "SDS", "sharks", "Shanghai", "Sharks", 0, 0, 1, 2017, 1, ["#dd3333", "#1e73be"]],
    #             ["15018", "GUANGZHOU", "GUA", "Guangzhou", "Long-Lions", 0, 0, 1, 2017, 1, []],
    #             。。。
    #         ],
    #         "players": [
    #             [76001, "Abdelnaby, Alaa", 0, 1990, 1994, 0, "Y"],
    #             [76002, "Abdul-Aziz, Zaid", 0, 1968, 1977, 0, "Y"],
    #             [76003, "Abdul-Jabbar, Kareem", 0, 1969, 1988, 0, "Y"],
    #             。。。
    #         ]
    #     }
    # };



    '''球队详细信息（http://stats.nba.com/team/1610612741/  界面,分析抓包 /stats/teamdetails）'''
    print('-----------------------获取球队详细信息----------------------')
    team_hearders={
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Referer': 'http://stats.nba.com/team/1610612744/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    for team_id in team_ids:
        team_url="http://stats.nba.com/stats/teamdetails?teamID="+str(team_id)
        rtn_json=spider.download_page(team_url,team_hearders)
        print('return:'+rtn_json)
        json_obj=json.loads(rtn_json)
        print('name:'+str(json_obj["resultSets"][0]['name']))

        '''球队详细信息 返回格式如下'''
        # {
        #     "resource":"teamdetails",
        #     "parameters":{
        #         "TeamID":1610612744
        #     },
        #     "resultSets":[
        #         {
        #             "name":"TeamBackground",
        #             "headers":[
        #                 "TEAM_ID",
        #                 "ABBREVIATION",
        #                 "NICKNAME",
        #                 "YEARFOUNDED",
        #                 "CITY",
        #                 "ARENA",
        #                 "ARENACAPACITY",
        #                 "OWNER",
        #                 "GENERALMANAGER",
        #                 "HEADCOACH",
        #                 "DLEAGUEAFFILIATION"
        #             ],
        #             "rowSet":[
        #                 [
        #                     1610612744,
        #                     "GSW",
        #                     "Warriors",
        #                     1946,
        #                     "Golden State",
        #                     "Oracle Arena",
        #                     "19596",
        #                     "Joe Lacob",
        #                     "Bob Myers",
        #                     "Steve Kerr",
        #                     "Santa Cruz Warriors"
        #                 ]
        #             ]
        #         },
        #         。。。


        '''球队中的球员花名册（第1个数组）'''
        '''球队中的教练（第2个数组）'''
        print('-----------------------获取球队中的球员花名册和教练信息---------------------')
        # LeagueID: 00
        # Season: 2017-18    17年到18年
        # TeamID: 1610612741
        # "/stats/commonteamroster"
        seasons=['2017-18','2016-17',]
        players_headers={
                'Accept': 'application/json, text/plain, */*',
                'x-nba-stats-token': 'true',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
                'x-nba-stats-origin': 'stats',
                'Referer': 'http://stats.nba.com/team/1610612744/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        for season in seasons:
            players_url="http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season="+season+"&TeamID="+team_id
            rtn_json=spider.download_page(players_url,players_headers)
            print('return:'+rtn_json)
            json_obj=json.loads(rtn_json)
            print('球员信息:'+str(json_obj["resultSets"][0]['rowSet'][0]))
            print('教练信息:'+str(json_obj["resultSets"][0]['rowSet'][1]))

            '''球员花名册 返回格式如下'''
            # {
            #     "resource":"commonteamroster",
            #     "parameters":{
            #         "TeamID":1610612744,
            #         "LeagueID":"00",
            #         "Season":"2011-12"
            #     },
            #     "resultSets":[
            #         {
            #             "name":"CommonTeamRoster",
            #             "headers":[
            #                 "TeamID",
            #                 "SEASON",
            #                 "LeagueID",
            #                 "PLAYER",
            #                 "NUM",
            #                 "POSITION",
            #                 "HEIGHT",
            #                 "WEIGHT",
            #                 "BIRTH_DATE",
            #                 "AGE",
            #                 "EXP",
            #                 "SCHOOL",
            #                 "PLAYER_ID"
            #             ],
            #             "rowSet":[
            #                 [
            #                     1610612744,
            #                     "2011",
            #                     "00",
            #                     "Dorell Wright",
            #                     "1",
            #                     "F",
            #                     "6-9",
            #                     "205",
            #                     "DEC 02, 1985",
            #                     26.0,
            #                     "7",
            #                     "South Kent Prep (CT)",
            #                     2748
            #                 ],
            #                 [
            #                     1610612744,
            #                     "2011",
            #                     "00",
            #                     "Nate Robinson",
            #                     "2",
            #                     "G",
            #                     "5-9",
            #                     "180",
            #                     "MAY 31, 1984",
            #                     28.0,
            #                     "6",
            #                     "Washington",
            #                     101126
            #                 ],

            '''教练 返回格式如下'''
            # {
            #     "resource":"commonteamroster",
            #     "parameters":{
            #         "TeamID":1610612744,
            #         "LeagueID":"00",
            #         "Season":"2011-12"
            #     },
            #     "resultSets":[
            #         {},
            #         {
            #             "name":"Coaches",
            #             "headers":[
            #                 "TEAM_ID",
            #                 "SEASON",
            #                 "COACH_ID",
            #                 "FIRST_NAME",
            #                 "LAST_NAME",
            #                 "COACH_NAME",
            #                 "COACH_CODE",
            #                 "IS_ASSISTANT",
            #                 "COACH_TYPE",
            #                 "SCHOOL",
            #                 "SORT_SEQUENCE"
            #             ],
            #             "rowSet":[
            #                 [
            #                     1610612744,
            #                     "2011",
            #                     "JAC331857",
            #                     "Mark",
            #                     "Jackson",
            #                     "Mark Jackson",
            #                     "mark_jackson",
            #                     1.0,
            #                     "Head Coach",
            #                     "College - St. John's (N.Y.)",
            #                     null
            #                 ],
            break;#测试（只获取一个赛季的球员和教练信息）

        break;#测试（只获取一个球队信息）