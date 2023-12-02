"""
Vanguard Zero Image Downloader
Version: 1.0
Date: 24 November 2023
"""


import os
import random
import time
import requests


def download_images(url_list, image_namelist, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for i, url in enumerate(url_list):
        time.sleep(random.randint(2,4))
        try:
            response = requests.get(url)
            response.raise_for_status()

            image_filename = os.path.join(output_folder, image_namelist[i])

            with open(image_filename, 'wb') as image_file:
                image_file.write(response.content)

            print(f"Downloaded {image_filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")


if __name__ == "__main__":
    path = 'https://s3-ap-northeast-1.amazonaws.com/vgzero.bushimo.jp/wp-content/images/cardlist/gacha/'
    folder_name = 'g-box-14_ryuoukakusei'
    set_name = 'g-box-14_ryuoukakusei/'
    # set_name = 'g-box_fc01/'
    card_id = 'BTG7452'
    first_id = 1
    last_id = 17

    image_urls = []
    image_names = []

    for card in range(first_id, last_id + 1):
        if card < 10:
            image_urls.append(path + set_name + card_id + '00' + str(card) + '.png')
            image_names.append(card_id + '00' + str(card) + '.png')
        elif card < 100:
            image_urls.append(path + set_name + card_id + '0' + str(card) + '.png')
            image_names.append(card_id + '0' + str(card) + '.png')
        else:
            image_urls.append(path + set_name + card_id + str(card) + '.png')
            image_names.append(card_id + str(card) + '.png')

    # for i, link in enumerate(image_urls):
    #     print(image_names[i])
    #     print(link)

    download_images(image_urls, image_names, folder_name)
