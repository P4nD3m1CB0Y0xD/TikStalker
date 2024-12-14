import json
import argparse
import requests
from bs4 import BeautifulSoup as BSoup
import csv
import logging
import os

ESC = '\x1b'
RED = ESC + '[31m'
GREEN = ESC + '[32m'
RESET = ESC + '[0m'

logging.basicConfig(filename='tikstalker.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_tiktoker(username: str, user_agent=None, proxy=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.5748.222 Safari/537.36'
    }
    tiktok_url = 'https://www.tiktok.com/@'

    if user_agent:
        headers['User-Agent'] = user_agent

    proxies = {}
    if proxy:
        proxies = {'http': proxy, 'https': proxy}

    try:
        response = requests.get(tiktok_url + username, headers=headers, proxies=proxies)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve data for {username}. Error: {e}")
        print(f"{RED}Failed to retrieve data for {username}. Error: {e}{RESET}")
        return

    soup = BSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

    if script_tag:
        try:
            json_data = json.loads(script_tag.string)
            user_data = json_data['__DEFAULT_SCOPE__']['webapp.user-detail']
            save_user_data(username, user_data)
            parse_tiktoker_data(username, user_data)
        except json.JSONDecodeError as error:
            logging.error(f"Error parsing JSON for {username}: {error}")
            print(f"{RED}Error parsing JSON: {error}{RESET}")
    else:
        logging.error(f'No script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__" found for {username}.')
        print(f'{RED}No script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__" found.{RESET}')


def save_user_data(username, data):
    filename = f"{username}_tiktok_data.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{GREEN}User data saved to {filename}{RESET}")

def parse_tiktoker_data(username, field: dict):
    user_data = field["userInfo"]["user"]
    user_stats = field["userInfo"]["stats"]
    user_share_meta = field["shareMeta"]

    profile_pic_url = user_data.get("avatarLarger", "")

    print('\n' + '-' * 15 + ' User Information ' + '-' * 15)

    # Account Information
    print(f'{RED}Profile Picture URL:{GREEN} {profile_pic_url}')
    print(f'{RED}Account ID:{GREEN}       {user_data["id"]}')
    print(f'{RED}Unique ID:{GREEN}        {user_data["uniqueId"]}')
    print(f'{RED}Nickname:{GREEN}         {user_data["nickname"]}')
    signature = user_data["signature"].replace('\n', ' ')
    print(f'{RED}Bios:{GREEN}             {signature}')
    print(f'{RED}Private Account:{GREEN}  {user_data["privateAccount"]}')
    print(f'{RED}User Country:{GREEN}     {user_data["region"]}')
    print(f'{RED}Account Language:{GREEN} {user_data["language"]}')
    # Account Status
    print(f'{RED}\nTotal Followers:{GREEN}  {user_stats["followerCount"]}')
    print(f'{RED}Total Following:{GREEN}  {user_stats["followingCount"]}')
    print(f'{RED}Total Hearts:{GREEN}     {user_stats["heartCount"]}')
    print(f'{RED}Total Posts:{GREEN}      {user_stats["videoCount"]}')
    # Account Description
    print(f'{RED}\nTitle:{GREEN}            {user_share_meta["title"]}')
    print(f'{RED}Description:{GREEN}      {user_share_meta["desc"]}\n')

    # Recent Videos
    print('\n' + '-' * 15 + ' Recent Videos ' + '-' * 15)
    recent_videos = field.get("itemList", [])
    video_data = []
    if recent_videos:
        for idx, video in enumerate(recent_videos, 1):
            video_desc = video["desc"].replace('\n', ' ')
            video_url = f'https://www.tiktok.com/@{user_data["uniqueId"]}/video/{video["id"]}'
            video_stats = video["stats"]
            print(f'{RED}Video {idx}:{GREEN} {video_desc}')
            print(f'{RED}Video URL:{GREEN} {video_url}')
            print(f'{RED}Views:{GREEN} {video_stats["playCount"]}')
            print(f'{RED}Likes:{GREEN} {video_stats["diggCount"]}')
            print(f'{RED}Comments:{GREEN} {video_stats["commentCount"]}')
            print(f'{RED}Shares:{GREEN} {video_stats["shareCount"]}\n')

            video_data.append({
                "Description": video_desc,
                "URL": video_url,
                "Views": video_stats["playCount"],
                "Likes": video_stats["diggCount"],
                "Comments": video_stats["commentCount"],
                "Shares": video_stats["shareCount"]
            })
        save_videos_csv(username, video_data)
    else:
        print(f'{RED}No recent videos found.{RESET}')


def save_videos_csv(username, video_data):
    filename = f"{username}_videos.csv"
    keys = video_data[0].keys() if video_data else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(video_data)
    print(f"{GREEN}Video data saved to {filename}{RESET}")


def main():
    parser = argparse.ArgumentParser(description="TikStalker is a Python script developed to automate the process \
    of extracting public information from TikTok accounts.")
    parser.add_argument('-u', '--user', dest='target', required=True, help='The @nickname from your target')
    parser.add_argument('-a', '--user-agent', dest='uagent', required=False, help='Custom User-Agent <name>')
    parser.add_argument('-p', '--proxy', dest='proxy', required=False, help='Proxy server (e.g., http://proxyserver:port)')
    args = parser.parse_args()

    if args.target or args.uagent or args.proxy:
        get_tiktoker(args.target, args.uagent, args.proxy)


if __name__ == '__main__':
    main()
