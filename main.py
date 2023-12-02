"""
Vanguard Zero Image Downloader
Version: 2.2
Date: 1 December 2023
"""
from playwright.sync_api import sync_playwright
import requests
import os
import random
import re
import time


# MAX_SCROLLS = 100
SCROLL_DELAY = 2000
page_link = 'https://vgzero.bushimo.jp/cardlist/cardsearch/?expansion=GACHA014'


def scroll_down_to_load_content(page):
    # Version 2.1 used this loop to scroll a fixed number of times before exiting to the outer loop in main()
    # prev_height = -1
    # scroll_count = 0
    # while scroll_count < MAX_SCROLLS:
    #     page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    #     page.wait_for_timeout(SCROLL_DELAY)
    #     new_height = page.evaluate("document.body.scrollHeight")
    #     if new_height == prev_height:
    #         break
    #     prev_height = new_height
    #     scroll_count += 1
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(SCROLL_DELAY)


def extract_card_urls(page):
    urls = page.evaluate('''() => {
        const cards = document.querySelectorAll('a > div');
        const links = [];
        cards.forEach(card => {
            links.push(card.getAttribute('style'));
        });
        return links;
    }''')
    return urls


def clean_urls(raw_list):
    # The Regex pattern searches for 1 or more characters in between single quotes
    # Search for the pattern, return Matches, get the content of the Matches with group() for all urls in the list
    pattern = r"'(.+)'"
    cleaned_urls = [re.search(pattern, url).group().strip("'") for url in raw_list]
    return cleaned_urls


def get_folder_name(url_list):
    folder_name_pattern = r"(?:clan|gacha|haihu|sonota)\/(.+)\/"
    return re.search(folder_name_pattern, url_list[0]).group(0)


def download_images(url_list, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for i, url in enumerate(url_list):
        time.sleep(random.randint(2, 4))
        try:
            response = requests.get(url)
            response.raise_for_status()

            image_name = get_image_name(url)
            image_filename = os.path.join(output_folder, image_name)
            image_filename = image_filename.replace("/", "\\")

            with open(image_filename, 'wb') as image_file:
                image_file.write(response.content)

            print(f"({i+1}) Downloaded {image_filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading ({i+1}) {url}: {e}")


def get_image_name(url):
    image_name_pattern = r"((BT|FV|NP|PR|VM).+\.png)"
    return re.search(image_name_pattern, url).group(0)


def get_element_count():
    css_selector = 'div.result_list#cardlist-container > div.wrap'
    return target_page.eval_on_selector(css_selector, 'element => element.childElementCount')


if __name__ == '__main__':
    cleaned_links = []
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)

        # Open the webpage
        target_page = browser.new_page()
        target_page.goto(page_link, timeout=0)

        element_count = 0
        card_count = int(target_page.locator('p.num span').inner_text())
        while element_count < card_count:
            scroll_down_to_load_content(target_page)
            element_count = get_element_count()

        card_links = extract_card_urls(target_page)

        cleaned_links = clean_urls(card_links)

        browser.close()

    folder_name = get_folder_name(cleaned_links)
    download_images(cleaned_links, folder_name)
