# -*- coding:UTF-8 -*-

import getImage as gI
import time
from fake_user_agent.main import user_agent
import linecache

# 获取url
settingPath = "settings.txt"
url = linecache.getline(settingPath, 1).strip()  # 读取settings.txt第一行
path = linecache.getline(settingPath, 2).strip()  # 读取settings.txt第二行
# 获取页面数目
numList = [""]
pageNum = gI.getPageNum(url=url.format(numList[0]))
for i in range(2, int(pageNum)+1):
    numList.append("_" + str(i))
# 获取页面的正则表达式
hrefExpression = "\/tupian\/.*\.html"
jpgExpression = "\/uploads\/allimg\/.*\.jpg"


def main(url_, path):
    for i in numList:
        try:
            url = url_.format(i)
            print("\n已获取链接 " + str(url))
            hrefList = gI.getHref(url=url, hrefExpression=hrefExpression)
            detailPage = gI.getDetail(hrefList)
            allList = gI.getImage(detailPage, jpgExpression=jpgExpression)
            allImageList = allList[0]
            allNameList = allList[1]
            for li in allImageList:
                headers = {"user-agent": user_agent()}  # 设置假的请求头
                path_ = path + allNameList[allImageList.index(li)] + ".jpg"  # 得到存储地址
                gI.download(address=li, path=path_, headers=headers)  # 写入文件
                print("已下载：\t" + str(path_.split("\\")[-1]))
        except:
            print("抱歉，我们遭遇了未知错误")


if __name__ == "__main__":
    raw = input("按下Enter开始爬虫")
    startTime = time.time()  # 程序开始时间
    main(url_=url, path=path)
    endTime = time.time()  # 爬虫完成时间
    print("\n爬虫所用时间：" + str(round(endTime - startTime, 1)) + "秒")
    raw_ = input("按下Enter退出")
