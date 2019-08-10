# PixivDownloader
Pixiv And Pixivision Illustrations Downloader.<br>
 
* 项目主要用于 Pixiv站和Pixivision的插画特辑信息爬取和图片下载<br>
      	支持以下下载方式：<br>
          1.  Pixivision插画特辑列表页全部爬取<br>
          2.  Pixivision插画特辑详情页全部爬取<br>
          3.  通过Pixiv插画url下载<br>
          4.  通过Pixiv插画ID下载<br>
          5.  通过关键字搜索下载<br>
           6.  排行榜下载<br>
          7.  通过插画ID下载关联作品<br>

启动图形界面下载工具:(支持下载方式1-6)<br>
使用方式：1.直接启动，输入Pixiv用户名和密码(如果有配置会自动填充)，验证通过直接进入下载界面。2.配置ACCESS_TOKEN和PIXIV_COOKIES(每次使用用户名和密码登录时控制台会输出)，验证通过后(时间可能略长),直接进入下载界面。
~~~
python launcher_gui.py
~~~
<img src="readmeFile/gui.png" alt="GUI" width="400" height="430"/>

运行Pixivision全站插画爬虫:<br>
&nbsp;&nbsp;&nbsp;&nbsp;全站爬取完毕后，如果Pixivsion有更新，可以修改配置文件中的PAGE_NUM为更新的页数，比如Pixivsion有2页更新未爬取，修改PAGE_NUM=2,全站插画爬虫则会爬取前2页的所有特辑
~~~
python launcher_pixivision.py
~~~
运行Pixivision插画特辑补全脚本：<br>
&nbsp;&nbsp;&nbsp;&nbsp;用于检查从Pixivision下载的特辑是否完全下载完毕，文件是否完整，并补全下载。(注意：这里的补全并不是下载Pixivison的更新的内容)
~~~
python launcher_check_completion.py
~~~
Pixiv Api代码参考了[pixivpy](https://github.com/upbit/pixivpy "pixivpy")<br>
运行需求：python2.7(3以上版本暂未测试) 必要扩展库：future,requests(用于网页爬取,api请求),BeautifulSoup(用于网页html数据解析)<br>
非必要扩展库：<br>
&nbsp;requests[socks] 提供socks5代理支持
~~~
pip install 'requests[socks]'
~~~
&nbsp;twisted 如果需要运行launcher_pixivision.py,使用twisted线程池管理下载可以获取更快下载速度。<br>
&nbsp;Pillow  可检查Pixivision下载的插画文件是否完整。<br><br>

UPDATE:<br>
2017.05.11  新增项目目录外的配置文件config.ini,避免更新代码后原配置被覆盖<br>
2017.05.24  添加了一个简单的图形界面下载工具<br>
2017.06.20  完善图像界面下载工具,支持通过关键字搜索下载插画<br>
2017.07.06  由于Pixiv Api更新,原本拉取插画详情的接口需要登录才能使用,直接使用控制台命令下载时,Pixiv账号和密码设置变为必填项<br>
2017.07.16  Pixivision专辑页支持多图下载，所有下载图片默认为原图画质<br>
2017.07.27  Pixivision补全脚本,新增检查文件完整性：需要修改配置：CHECK_IMAGE_VERIFY=True 并安装 Pillow 生效<br>
2017.08.03  图形界面下载工具需要登录或配置Token和Cookie才能启动下载界面<br>
2017.08.31  优化图形界面下载工具的搜索下载，同时使用网页搜索爬虫和API搜索搜集下载数据<br>
2017.09.02  图形界面下载工具新增排行榜下载<br>
2017.09.22  Pixiv因DNS污染，部分地区无法直接访问。需要修改DNS或hosts文件才能正常使用。hosts文件修改:复制[pixiv_host](readmeFile/pixiv_host.txt)内容到hosts中<br>
2018.04.18  新增通过插画ID下载关联作品<br>
2018.09.03  旧hosts文件已失效，修改pixiv_host。新增windows环境下项目启动流程[windows](readmeFile/windows.md)<br>
2018.10.22  pixiv已经完全被墙，提供代理配置支持(详见pixiv_config配置项：USE_PROXY和PROXIES)<br>
2019.08.10  新增Pixiv Web Page Ranking 下载，支持下载Pixiv网页版排行榜<br>
2019.08.11  目前发现模拟登录网页版需要进行机器人验证，暂未解决，目前解决方式为直接网页登录后，复制浏览器的cookie，配置在RAW_PIXIV_COOKIES配置项上，可以绕开登录验证<br>


