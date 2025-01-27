import scrapy
import os
import requests
import json

class IdolscraperSpider(scrapy.Spider):
    name = "idolscraper"
    start_urls = ["URL"]

    def parse(self, response):
        # extracts the group name from the <title> tag and sanitize the name
        group_name = response.css("title::text").get().split(" |")[0]
        group_folder= group_name.replace("|", "").strip()

        os.makedirs(group_folder, exist_ok=True)

        # this variable is for the specific tags in the css that stores the members links. this must be adapted if used for a different website
        member_links = response.css("h3.pi-data-label.pi-secondary-font:contains('Current Members') + div.pi-data-value.pi-font a::attr(href)").getall()

        # loop through each member link
        for member_url in member_links:
            member_url = "URL" + member_url  # in this case, the links are stored as link stubs in the tags and need to be appended to the base URL
            yield response.follow(member_url, self.parse_member, meta={"group_path": group_folder})

    def parse_member(self, response):
        # extract the idol name from the <title> tag
        idol_name = response.css("title::text").get().split(" |")[0].replace(" ","_").strip()

        # makes a folder named after the respective member
        member_folder = idol_name.translate(str.maketrans("", "", ":*?\"<>|")) # sanitize folder name so as to not run into Windows issues
        member_path = os.path.join(response.meta["group_path"], member_folder)
        os.makedirs(member_path, exist_ok=True)

        # initialize dictionary to store scraped profile info, make first key the idol's name
        scraped_data = {"idol_name": idol_name}

        # finds the tag that the profile info is stored and extracts it into a dictionary
        profile_content = response.css("div.pi-item.pi-data.pi-item-spacing.pi-border-color")
        for div in profile_content:
            key = div.css("::attr(data-source)").get()
            value = div.css(".pi-data-value.pi-font::text").getall()
            value = " ".join(value).strip()
            if key and value:
                scraped_data[key] = value

        # extracts social media links, needs to account for naming of twitter/X
        sns_links = response.css("div.pi-data-value.pi-font a::attr(href)").getall()
        sns_links = [sns for sns in sns_links if sns.startswith(('https://twitter.com', 'https://x.com', 'https://www.instagram.com', 'https://www.tiktok.com'))]
        if sns_links:
            scraped_data["sns"] = sns_links

        # save the scraped data in a JSON file in the member's folder
        json_file_path = os.path.join(member_path, f"{idol_name}_profile.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)

        # Download the profile picture
        self.download_profile_picture(response, member_path, idol_name)

    def download_profile_picture(self, response, member_path, idol_name):
        # finds the profile picture based on the css tags
        img_url = response.css("meta[property='og:image']::attr(content)").get()
        if img_url:
            img_name = f"{idol_name}_profile_pic.jpg"
            img_path = os.path.join(member_path, img_name)
            with open(img_path, "wb") as img_file:
                img_file.write(requests.get(img_url).content)