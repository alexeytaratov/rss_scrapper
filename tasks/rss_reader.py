# You shouldn't change  name of function or their arguments
# but you can change content of the initial functions.
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import sys
from bs4 import BeautifulSoup
import json as lib_json
import pycodestyle


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,   # это я сам закомментил
) -> List[str]:
    # Your code goes here
    bytes_xml = bytes(xml, encoding='utf-8')
    # Этот код (КОТОРЫЙ НИЖЕ) запишет извлекаемый XML-контент в переменную soup.
    soup = BeautifulSoup(bytes_xml, features='xml')
    articles_head = soup.find('channel')
    articles = soup.findAll('item')   # Выбираем всё содержимое тегов item и записываем articles.
    # print(f"Количество новостей в ленте всего: {len(articles)}\n")

    if json is True:
        result = {}
        if articles_head.find('title') is not None:
            result['title'] = articles_head.find('title').text
        if articles_head.find('link') is not None:
            result['link'] = articles_head.find('link').text
        if articles_head.find('lastBuildDate') is not None:
            result['lastBuildDate'] = articles_head.find('lastBuildDate').text
        if articles_head.find('pubDate') is not None:
            result['pubDate'] = articles_head.find('pubDate').text
        if articles_head.find('language') is not None:
            result['language'] = articles_head.find('language').text
        if articles_head.find('category') is not None:
            result['category'] = articles_head.find('category').text
        if articles_head.find('managinEditor') is not None:
            result['managinEditor'] = articles_head.find('managinEditor').text
        if articles_head.find('description') is not None:
            result['description'] = articles_head.find('description').text
        if articles_head.find('item') is not None:
            result['items'] = []

        endIndex = 0
        if (limit is not None) and (len(articles) >= limit) and (limit > 0):  # and (json == True)
            endIndex = limit
        elif (limit is None) or (len(articles) < limit):  # and (json == True)
            endIndex = len(articles)
        for a in range(endIndex):
            item = {}
            if articles[a].find('title') is not None:
                item.update({'title': articles[a].find('title').text})
            if articles[a].find('author') is not None:
                item.update({'author': articles[a].find('author').text})
            if articles[a].find('pubDate') is not None:
                item.update({'pubDate': articles[a].find('pubDate').text})
            if articles[a].find('link') is not None:
                item.update({'link': articles[a].find('link').text})
            if articles[a].find('category') is not None:
                item.update({'category': articles[a].find('category').text})
            if articles[a].find('description') is not None:
                item.update({'description': articles[a].find('description').text})
            result['items'].append(item)
        resultJson = lib_json.dumps(result, indent=2, ensure_ascii=False)
        res_json_list = resultJson.split('\n')
        return res_json_list

    else:
        # Собрать все строки вместо принта в массив строк и вернуть его
        result = []
        if articles_head.find('title') is not None:
            result.append(f"Feed: {articles_head.find('title').text}")
        if articles_head.find('link') is not None:
            result.append(f"Link: {articles_head.find('link').text}")
        if articles_head.find('lastBuildDate') is not None:
            result.append(f"Last Build Date: {articles_head.find('lastBuildDate').text}")
        if articles_head.find('pubDate') is not None:
            result.append(f"Publish Date: {articles_head.find('pubDate').text}")
        if articles_head.find('language') is not None:
            result.append(f"Language: {articles_head.find('language').text}")
        if articles_head.find('category') is not None:
            result.append(f"Categories: {articles_head.find('category').text}")
        if articles_head.find('managinEditor') is not None:
            result.append(f"Editor: {articles_head.find('managinEditor').text}")
        if articles_head.find('description') is not None:
            result.append(f"Description: {articles_head.find('description').text}")

        endIndex = 0
        if (limit is not None) and (len(articles) >= limit) and (limit > 0):
            endIndex = limit
        elif (limit is None) or (len(articles) < limit):
            endIndex = len(articles)
        for i in range(endIndex):
            result.append('')
            if articles[i].find('title') is not None:
                result.append(f"Title: {articles[i].find('title').text}")
            if articles[i].find('author') is not None:
                result.append(f"Author: {articles[i].find('author').text}")
            if articles[i].find('pubDate') is not None:
                result.append(f"Published: {articles[i].find('pubDate').text}")
            if articles[i].find('link') is not None:
                result.append(f"Link: {articles[i].find('link').text}")
            if articles[i].find('category') is not None:
                result.append(f"Categories: {articles[i].find('category').text}")
            if articles[i].find('description') is not None:
                result.append('')
                result.append(articles[i].find('description').text)
        return result


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )
    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
