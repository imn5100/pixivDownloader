# PixivisionDownloader
 Pixivision Illustrations Crawler And Downloader.<br>
 [Pixivision](http://www.pixivision.net/)原pixiv Spotlight，以特辑的形式展示Pixiv经典作品（包括 插画、漫画、小说等），支持日语、英语、中文（繁体·简体），共4种语言<br>
 
* 项目主要用于 Pixivision的插画特辑信息爬取和图片下载<br>
	支持图片质量：普通图和原图|大图下载<br>
      	支持以下下载方式：<br>
          Pixivision插画特辑列表页<br>
          Pixivision插画特辑详情页<br>
          Pixiv插画url<br>
          Pixiv插画ID<br>
 
* 核心配置文件__pixiv_config.py__<br>
     修改__CRAWLER_HEADER__中__Accept-Language__，获取4中不同语言的特辑描述。<br>
     修改__IMAGE_SVAE_BASEPATH__，指定图片存储位置。<br>
     修改__IMAGE_QUALITY__，指定下载的图片质量。<br>
~~~
python launcher.py
~~~
