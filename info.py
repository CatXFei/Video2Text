from lxml import etree
from lxml import html
import requests

# get the script of the website and save it as a tree object
def get_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

# get the video link form the web script
def get_video_url(url):
    tree = get_tree(url)
    target_element = " ".join(tree.xpath('//script[contains(text(),"mp4")]/text()'))
    target_list = target_element.split('\n')
    link = target_list[4]
    # print(link)
    sub_link = "".join(link[link.index('/') + 2: len(link) - 2])
    # print(sub_link)
    real_link = sub_link.replace(sub_link[0 : sub_link.find('.')], 'mv')
    real_link = 'http://' + real_link
    # print(real_link)
    return real_link

#extract and create the video name with xpath
def get_video_name(url):
    tree = get_tree(url)
    name = "".join(tree.xpath('//meta[@name = "keywords"]/@content'))
    name += name + '.mp4'
    return name

#extract and create the audio name with xpath
def get_audio_name(url):
    tree = get_tree(url)
    name = "".join(tree.xpath('//meta[@name = "keywords"]/@content'))
    name += name + '.mp3'
    return name

