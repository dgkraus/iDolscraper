# Idolscraper

A Scrapy-based tool to scrape and organize Japanese idol group member profiles.

## Description
This project scrapes individual idol profiles from public pages of official websites or wikis, organizes the data neatly in folders by group and member, and saves everything in JSON format for easy database integration.

The exact URL is intentionally left out to avoid overloading the website, but adjusting the script for each website's design should be rather simple.

## Installation And Usage

install scrapy via "python -m pip install scrapy", navigate to the file "idolscraper/spiders/idolscraper.py", and simply run the command "scrapy crawl idolscraper". Folders with scraped data will be saved in the same folder as the script.

## Example Output

{
    "idol_name": "Tsukiashi Amane",
    "caption": "Promoting   (March 2024)",
    "nickname": "Amachan (あまちゃん)",
    "birthdate": "October 26, 1999 (age 25)",
    "birthplace": ",  ,",
    "bloodtype": "B",
    "zodiac": "Scorpio",
    "height": "153 cm",
    "genre": "J-Pop",
    "occupation": "Idol",
    "active": "2016-present",
    "agency": "( )",
    "formergroup": "(Team TII)",
    "generation": "4th ( )",
    "join": "July 12, 2016 ( ) Founding Member ( )",
    "graduate": "March 30, 2020 ( )",
    "sns": [
        "https://www.instagram.com/am1026_official/",
        "https://www.tiktok.com/@am1026_official"
    ]
}