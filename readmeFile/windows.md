1.下载安装python2.7环境(安装时需要选择Add python.exe to Path,默认是不勾选的)。并安装相关依赖,直接在cmd执行以下命令：
```
pip install  requests
pip install  future
pip install  BeautifulSoup
#下为非必需安装-作用详见readme
pip install twisted
pip install Pillow
```
2.下载项目源码，使用git下载或直接Download Zip
```
git clone https://github.com/imn5100/pixivDownloader.git
```
3.找到源码根目录,复制config.ini到向外一层文件夹。设置自己的配置(也可以直接修改pixiv_config.py中的配置)。

4.打开cmd，跳转(cd)到源码根目录,运行：
```
python launcher_gui.py
```
5.第一次运行后需要输入账号密码，登录成功后控制台会输出Refresh Token和cookie信息。将其填写到配置文件中，就不用每次都输出账号密码了。

控制台输出
```
ACCESS TOKEN R8d7lRnRxT6PCnWwSAQj7gn6AWes8pGzP8lGgzSpxz0
ACCESS Refresh Token i0I0ZxJvgRXVaqJXdws01ojeP1buc_w5NgThFHZL6mI
Login Success getCookies:{'device_token': 'cd00981cb187dac4912ca4b06b0c9fb8', 'p_ab_id': '6', 'PHPSESSID': '26621395_a2b37599dbdcb225b35b22008760b153', 'p_ab_id_2': '3'}
```
配置文件(Token有效期太短，通常只配置Refresh_Token和Cookie就够了,Cookie和Refresh Token是长期有效的)
```
REFRESH_TOKEN=i0I0ZxJvgRXVaqJXdws01ojeP1buc_w5NgThFHZL6mI
PIXIV_COOKIES = {'device_token': 'cd00981cb187dac4912ca4b06b0c9fb8', 'p_ab_id': '6', 'PHPSESSID': '26621395_a2b37599dbdcb225b35b22008760b153', 'p_ab_id_2': '3'}
```
6.如果登录时，控制台出现连接超时或连接拒绝，尝试修改hosts(详见readme)
