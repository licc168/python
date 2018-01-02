# -*- coding:utf8 -*-
import sys
import requests
import re
import json
 
#搜索获取音乐列表
def get_music_info(url):
    response = requests.get(url)
    return parse_music_info(response.text)
#解析音乐列表
def parse_music_info(html):
    html = re.sub(r'^jQuery.+lists\"\:', "", html)
    html = re.sub(r'\,\"chinesecount.+',"",html)

    for item in json.loads(html):

        yield [item['FileName'],item['AlbumID'],item['AlbumName'],item['Duration'],item['FileHash']]
#跳转到每个歌曲的详细页面
def get_play_url(hash_id,album_id):
    url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash='+hash_id+'&album_id='+album_id+'&_=1505738969338'
    response = requests.get(url)
    return parse_play_url(response.text)
#解析歌曲的播放地址
def parse_play_url(html):
    pattern = re.compile('"play_url":"(.*?)"')
    result = re.findall(pattern, html)
    if result:
        return result[0].replace('\\','')
#程序入口
def main(keyword):
    url = 'http://songsearch.kugou.com/song_search_v2?callback=jQuery112405213552049562944_1505739248953&keyword='+keyword+'&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter'
    # html = get_music_info(url)
    for item in get_music_info(url):
        play_url = get_play_url(item[4],item[1])
        second = int(item[3])%60
        second = str(second) if second > 10 else '0'+str(second)
        print ('歌名：'+str(item[0]),'专辑：'+ str(item[2]),'时长：'+str(int(item[3])/60)+':'+second,play_url)
 
if __name__ == '__main__':
    main('慢慢')