# PixivisionDownloader
 Pixivision Illustrations Crawler And Downloader.<br>
 [Pixivision](http://www.pixivision.net/)原pixiv Spotlight，以特辑的形式展示Pixiv经典作品（包括 插画、漫画、小说等），支持日语、英语、中文（繁体·简体），共4种语言<br>
 
* 项目主要用于 Pixivision的插画特辑信息爬取和图片下载<br>
	支持图片质量：普通图和原图|大图下载<br>
      	支持以下下载方式：<br>
          1.  Pixivision插画特辑列表页<br>
          2.  Pixivision插画特辑详情页<br>
          3.  Pixiv插画url<br>
          4.  Pixiv插画ID<br>
 
* 核心配置文件__pixiv_config.py__<br>
     1. 修改__CRAWLER_HEADER__中__Accept-Language__，获取4中不同语言的特辑描述。<br>
     2. 修改__IMAGE_SVAE_BASEPATH__，指定图片存储位置。<br>
     3. 修改__IMAGE_QUALITY__，指定下载的图片质量。<br>
     4. 修改__USE_FILTER__，True：启动RedisFilter，自动过滤重复下载的特辑。False:重复下载特辑会覆盖原文件。<br>

运行：
~~~
python  launcher.py 
~~~
启动Pixivision全站插画爬虫(需配置Pixivision总页数pixiv_config.PAGE_NUM):
~~~
python launcher_plus.py
~~~
启动关联下载，通过Pixiv插画id下载关联作品,需自定义关联深度，每次向下关联可获取20-30副插画，因为越向下关联性越差，质量也会变低，因此关联深度不能设置太大。
~~~
python launcher_related.py
~~~
PS:因网络问题，下载失败很难避免。运行完毕后，若有提示下载失败的插画，可以通过查看download_error.log文件获取下载失败的插画详情。运行launcher.py 使用url或ID下载。<br>
实现思路：参考我的博客文章[shawblog.me](https://shawblog.me/blog/112.html)
