# -*- coding:UTF-8 -*-

# 导入模块
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re


def getDetail(hrefList):
    detailPage = []
    for image in hrefList:
        image = "https://pic.netbian.com/" + image["href"]
        detailPage.append(image)
    return detailPage


def getImage(detailPage, jpgExpression):
    allImageList = []
    allNameList = []
    for detail in detailPage:
        detailUrl = urlopen(detail)
        bsObjDetail = BeautifulSoup(detailUrl, features="lxml")  # BeautifulSoup对象
        imageList = bsObjDetail.findAll("img", {"src": re.compile(jpgExpression)})
        for i in imageList:
            try:
                allNameList.append(i["title"])
                allImageList.append("https://pic.netbian.com" + i["src"])
            except KeyError:
                pass
    return [allImageList, allNameList]


def getHref(url, hrefExpression):
    listPage = urlopen(url)
    bsObj = BeautifulSoup(listPage, features="lxml")  # BeautifulSoup对象
    hrefList = bsObj.findAll("a", {"href": re.compile(hrefExpression)})  # 得到壁纸具体页面
    return hrefList


def getPageNum(url):
    listPage = urlopen(url)
    bsObj = BeautifulSoup(listPage, features="lxml")  # BeautifulSoup对象
    expression = url[23:]
    expression = expression.replace("index", "index.*")
    hrefList = bsObj.findAll("a", {"href": re.compile(expression)})
    href = hrefList[-2].text
    return href


def download(address, path, headers):
    img = requests.get(address, headers=headers).content
    with open(path, "wb") as f:
        f.write(img)
