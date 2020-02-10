# 多种文档下载器
本工具适用于下载豆丁、道客巴巴、淘豆网、原创力、新浪爱问、金锄头网站的可以预览的文档。只要可以预览，就可以下载。下载下来是图片格式，然后会通过reportlab库，将图片转换成PDF。

本仓库为doc_downloader的网页版本，采用Flask框架搭建，并且用到了redis和celery。了解详细内容，可以访问[doc_downloader](https://github.com/rty813/doc_downloader)

本仓库对应的网页下载器网址为：[http://jdoufu.xyz](http://jdoufu.xyz)