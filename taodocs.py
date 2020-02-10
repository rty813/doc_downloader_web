from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, JavascriptException, StaleElementReferenceException

import base64
import time
import sys
import os
from tqdm import trange
from img2pdf import conpdf
import urllib.request
import shutil


def download(url, callback):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('log-level=3')
    driver = webdriver.Chrome(chrome_options=option)

    title = "output"
    try:
        driver.set_page_load_timeout(15)
        driver.get(url)
        title = driver.title[:-8]
    except:
        return False, "下载失败，超时"

    print(f'淘豆网: 《{title}》')
    if os.path.exists(f'./output/{title}.pdf'):
        return True, title
    time.sleep(5)

    while True:
        try:
            driver.execute_script("window.scrollBy(0,10000)")
            time.sleep(1)
            # 展开全部
            elem_cont_button = driver.find_element_by_class_name(
                "banner-more-btn")
            elem_cont_button = elem_cont_button.find_element_by_tag_name(
                'span')
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", elem_cont_button)
            actions = ActionChains(driver)
            actions.move_to_element(elem_cont_button).perform()
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", elem_cont_button)
            # break
        except NoSuchElementException:
            break
        except StaleElementReferenceException:
            break
        except JavascriptException:
            continue

    try:
        # 获取页数
        num_of_pages = driver.find_element_by_id(
            'docPage').get_attribute('innerHTML')
        num_of_pages = int(num_of_pages)

        if os.path.exists(f'./temp/{title}'):
            shutil.rmtree(f'./temp/{title}')
        os.makedirs(f'./temp/{title}')

        for pages in trange(num_of_pages):
            callback(pages, num_of_pages, "正在下载：%s" % title)
            try:
                time.sleep(0.5)
                element = driver.find_element_by_id(f"page{pages + 1}")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                time.sleep(0.5)
                imgElement = element.find_element_by_tag_name('img')
                imgUrl = imgElement.get_attribute('src')
                response = urllib.request.urlopen(imgUrl)
                html = response.read()
                with open(f'./temp/{title}/{pages}.jpg', 'wb') as f:
                    f.write(html)
            except Exception as e:
                print('下载中断，信息：\n%r' % e)
                break
        driver.quit()
        print('下载完毕，正在转码')
        callback(99, 100, "正在转码")
        conpdf(f'output/{title}.pdf', f'temp/{title}', '.jpg')
        return True, title
    except Exception as e:
        return False, e

if __name__ == "__main__":
    download('https://www.taodocs.com/p-292564682.html')
