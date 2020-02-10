import fire
import os
import douding
import doc88
import book118 
import taodocs
import jinchutou
import ishare

def download(url, callback):
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    if not os.path.exists('./output'):
        os.mkdir('./output')

    if 'doc88' in url:
        # 道客巴巴
        return doc88.download(url, callback)
    elif 'book118' in url:
        # 原创力
        return book118.download(url, callback)
    elif 'taodocs' in url:
        # 淘豆网
        return taodocs.download(url, callback)
    elif 'docin' in url:
        # 豆丁
        return douding.download(url, callback)
    elif 'jinchutou' in url:
        # 金锄头
        return jinchutou.download(url, callback)
    elif 'ishare' in url:
        return ishare.download(url, callback)
    else:
        return False, "不支持"

if __name__ == "__main__":
    fire.Fire(main)
    # "https://www.doc88.com/p-6099938057537.html"
