import markdown
import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict


def convert_md_to_html(path_to_file: str) -> None:
    """
    The function converts the *.md file to *.html
    and creates a new file with the extension *.html
    in the same directory
    :param path_to_file: path to file *.md
    :return: None
    """
    with open(path_to_file, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    with open('README.html', 'w') as f:
        f.write(html)


def get_urls_list(file_path: str) -> list:
    """
    The function extracts all links from the *.html file
    :param file_path: path to *.html file
    :return: list of links
    """
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

        urls_list = list()
        for link in soup.find_all('a'):
            urls_list.append(link.get('href'))

    return urls_list


def checking_link_availability(urls_list: list) -> dict:
    """
    The function checks the status code of all links.
    The result is saved to the dictionary by the key 'status_code'.
    Exceptions are saved by the 'exception' key
    :param urls_list: list of links
    :return: dictionary in the format {status_code: {i: url}}
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    check_result = defaultdict(dict)

    for i, url in enumerate(urls_list):
        print(i)
        print(url)
        try:
            page = requests.get(url, headers=headers)
            status_code = page.status_code
            check_result[status_code][i] = url

        except Exception:
            status_code = 'exception'
            check_result[status_code][i] = url
            pass

    return check_result


def convert_checking_result_to_json(datas: dict) -> None:
    """
    Converts the dictionary to json format, saves it to the same directory.
    :param datas: dictionary
    :return: None
    """
    convert_to_json = json.dumps(datas, indent=4)
    with open('checking_result.json', 'w') as f:
        f.write(convert_to_json)


convert_md_to_html('README.md')
urls_list = get_urls_list('README.html')
checking_result = checking_link_availability(urls_list)
convert_checking_result_to_json(checking_result)
