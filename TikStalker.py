import json
import argparse
import requests
from bs4 import BeautifulSoup as BSoup

ESC = '\x1b'
RED = ESC + '[31m'
GREEN = ESC + '[32m'


def get_tiktoker(username: str, user_agent=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.5748.222 Safari/537.36'
    }
    tiktok_url = 'https://www.tiktok.com/@'

    if user_agent != 'None':
        headers = {
            'User-Agent': user_agent
        }

    response = requests.get(tiktok_url + username, headers=headers)
    # print(response.status_code)
    soup = BSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

    if script_tag:
        try:
            json_data = json.loads(script_tag.string)
            parse_tiktoker_data(json_data['__DEFAULT_SCOPE__']['webapp.user-detail'])
        except json.JSONDecodeError as error:
            print(f'Error parsing JSON: {error}')
    else:
        print('No script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__" found.')


def parse_tiktoker_data(field: dict):
    user_data = field["userInfo"]["user"]
    user_stats = field["userInfo"]["stats"]
    user_share_meta = field["shareMeta"]

    print('\n' + '-' * 15 + f' User Information ' + '-' * 15)

    # Account Information
    print(f'{RED}Account ID:{GREEN}       {user_data["id"]}')
    print(f'{RED}Unique ID:{GREEN}        {user_data["uniqueId"]}')
    print(f'{RED}Nickname:{GREEN}         {user_data["nickname"]}')
    print(f'{RED}Bios:{GREEN}             {user_data["signature"].replace('\n', ' ')}')
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


def main():
    parser = argparse.ArgumentParser(description="TikStalker is a Python script is developed to automate the process \
    of extracting public information from TikTok accounts.")
    parser.add_argument('-u', '--user', dest='target', required=True, help='The @nickname from your target')
    parser.add_argument('-a', '--user-agent', dest='uagent', required=False, help='Custom User-Agent <name>')
    args = parser.parse_args()

    if args.target or args.uagent:
        get_tiktoker(args.target, args.uagent)
    # else:
    #     print('No user.')


if __name__ == '__main__':
    main()
