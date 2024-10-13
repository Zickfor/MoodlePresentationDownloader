import os
import os.path
import re
import base64
import shutil
import toml

import img2pdf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def img_converter_to_pdf(dirname):
    imgs = []
    for fname in os.listdir(dirname):
        if not fname.endswith(".jpg"):
            continue
        path = os.path.join(dirname, fname)
        if os.path.isdir(path):
            continue
        imgs.append(path)
    with open(f"{dirname}.pdf", "wb") as f:
        f.write(img2pdf.convert(imgs))


def download_presentation(pres_id, moodle_url):
    driver.get(moodle_url + "mod/page/view.php?id=" + pres_id)
    WebDriverWait(driver, 10)
    title = driver.find_element(By.TAG_NAME, "h1")
    new_title = re.sub(r'[^\w]', ' ', title.text)
    if not os.path.exists(pres_id):
        os.mkdir(pres_id)
    while True:
        page = driver.find_element(By.CLASS_NAME, "info")
        current_page, last_page = re.split(r" / ", page.text)
        print(f"{current_page} / {last_page}")
        viewport = driver.find_element(By.CLASS_NAME, "viewport")
        base64_img = viewport.get_property("style")["background-image"][27:-2]
        with open(f"{pres_id}/{current_page.zfill(3)}.jpg", "wb") as file:
            file.write(base64.b64decode(base64_img))
            file.close()
        if current_page == last_page:
            break
        next_button = driver.find_elements(By.TAG_NAME, "svg")
        next_button[1].click()
    img_converter_to_pdf(pres_id)
    shutil.rmtree(pres_id)


if __name__ == "__main__":
    if not os.path.exists("config.toml"):
        print("It seems to be a first start... So, please, edit config.toml file.")
        example_config = {
            "auth": {
                "username": "Your username here...",
                "password": "Your password here...",
                "moodle_url": "https://example.com/"
            },
            "ids": [
                "109554",
                "109569",
                "147600"
            ]
        }
        with open("config.toml", "w") as f:
            toml.dump(example_config, f)
            f.close()
        exit(0)
    else:
        with open("config.toml", "r") as f:
            config = toml.load(f)
            f.close()

    driver = webdriver.Firefox()
    driver.get(config["auth"]["moodle_url"])

    uname = driver.find_element(By.NAME, "username")
    uname.send_keys(config["auth"]["username"])
    pword = driver.find_element(By.NAME, "password")
    pword.send_keys(config["auth"]["password"])
    login = driver.find_element(By.ID, "loginbtn")
    login.click()

    WebDriverWait(driver, 10)

    for pres in config["ids"]:
        print(pres)
        download_presentation(pres, config["auth"]["moodle_url"])

    driver.quit()
