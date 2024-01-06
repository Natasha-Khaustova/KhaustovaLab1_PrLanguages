import time
from bs4 import BeautifulSoup
import requests
import threading
from queue import Queue

titleList = Queue()
authorList = Queue()
annotationList = Queue()
newsAgregatorList = Queue()
visitedTitle = set()

def pars_sbnation():
    url = 'https://www.sbnation.com'
    while True:
        try:
            page = requests.get(url)
            pars = BeautifulSoup(page.text, "html.parser")
            infoPage = pars.findAll('div', class_='c-compact-river__entry')
            for selectInfo in infoPage:
                title = selectInfo.find('h2', class_='c-entry-box--compact__title')
                author = selectInfo.find('span', class_='c-byline__author-name')

                if title.text.strip() not in visitedTitle:
                    visitedTitle.add(title.text.strip())
                    newsAgregatorList.put("...................SBNATION news...................")

                    if title is not None:
                        titleList.put(title.text.strip())
                    if author is not None:
                        authorList.put(author.text.strip())
                    else: authorList.put("_")
                    annotationList.put("_")
        except Exception as e:
            print(f"An error occurred: {e}")
def pars_wordlinsport():
    url = 'https://worldinsport.com'
    while True:
        try:
            page = requests.get(url)
            pars = BeautifulSoup(page.text, "html.parser")
            infoPage = pars.findAll('article', class_='post')

            for selectInfo in infoPage:
                title = selectInfo.find('h2', class_='entry-title')
                author = selectInfo.find('span', class_='author-name')
                annotation = selectInfo.find('p', class_='')
                if title.text.strip() not in visitedTitle:
                    visitedTitle.add(title.text.strip())
                    newsAgregatorList.put("...................WORDLINSPORT news...................")

                    if title is not None:
                        titleList.put(title.text.strip())
                    if author is not None:
                        authorList.put(author.text.strip())
                    else: authorList.put("_")
                    if annotation is not None:
                        annotationList.put(annotation.text.strip())
        except Exception as e:
            print(f"An error occurred: {e}")

def pars_football365():
    url = 'https://www.football365.com/'
    while True:
        try:
            page = requests.get(url)
            pars = BeautifulSoup(page.text, "html.parser")
            infoPage = pars.findAll('div', class_='relative flex flex-col w-full news-card border border-page')

            for selectInfo in infoPage:
                title = selectInfo.find(class_=lambda x: x and x.startswith('px-3 xs:px-4'))
                author = selectInfo.find('a', class_='text-author')
                annotation = selectInfo.find('div', class_=lambda x: x and x.startswith('mb-2 px-3'))
                if title.text.strip() not in visitedTitle:
                    visitedTitle.add(title.text.strip())
                    newsAgregatorList.put("...................FOOTBALL365 news...................")

                    if title is not None:
                        titleList.put(title.text.strip())
                    if author is not None:
                        authorList.put(author.text.strip())
                    else: authorList.put("_")
                    if annotation is not None:
                        annotationList.put(annotation.text.strip())
        except Exception as e:
            print(f"An error occurred: {e}")


def pars_rusfootball():
    url = 'https://www.rusfootball.info/'
    while True:
        try:
            page = requests.get(url)
            pars = BeautifulSoup(page.text, "html.parser")
            infoPage = pars.findAll('article', class_=lambda x: x and x.startswith('short-story'))

            for selectInfo in infoPage:
                title = selectInfo.find('a')
                annotation = selectInfo.find('div', class_='short_description has_image')
                if title.text.strip() not in visitedTitle:
                    visitedTitle.add(title.text.strip())
                    newsAgregatorList.put("...................RUSFOOTBALL news...................")

                    if title is not None:
                        titleList.put(title.text.strip())
                    if annotation is not None:
                        annotationList.put(annotation.text.strip())
                    authorList.put("_")
        except Exception as e:
            print(f"An error occurred: {e}")

def pars_allhockey():
    url = 'https://allhockey.ru/'
    while True:
        try:
            page = requests.get(url)
            pars = BeautifulSoup(page.text, "html.parser")
            infoPage = pars.findAll('div', class_='ui card article-card')

            blocks = []

            for selectInfo in infoPage:
                blocks.append(selectInfo.find('div', class_='content'))

            for selectInfo in blocks:
                if selectInfo is not None:
                    title = selectInfo.find('a')
                    author = selectInfo.find('a', class_='author')
                    if title.text.strip() not in visitedTitle:
                        visitedTitle.add(title.text.strip())
                        newsAgregatorList.put("...................ALLHOCKEY news...................")

                        if title is not None:
                            titleList.put(title.text.strip())
                        if author is not None:
                            authorList.put(author.text.strip())
                        else: authorList.put("_")
                        annotationList.put("_")
        except Exception as e:
            print(f"An error occurred: {e}")


def main_thread():
    try:
        threadSbnation = threading.Thread(target=pars_sbnation)
        threadWordlinsport = threading.Thread(target=pars_wordlinsport)
        threadFootball365 = threading.Thread(target=pars_football365)
        threadRusFootball = threading.Thread(target=pars_rusfootball)
        threadAllHockey = threading.Thread(target=pars_allhockey)

        threadSbnation.start()
        threadWordlinsport.start()
        threadFootball365.start()
        threadRusFootball.start()
        threadAllHockey.start()

        while True:
            if not newsAgregatorList.empty():
                print(newsAgregatorList.get())

            if not titleList.empty():
                print(titleList.get())

            if not authorList.empty():
                print("by author ", authorList.get())

            if not annotationList.empty():
                print("annotation -> ", annotationList.get())


    except KeyboardInterrupt:
        print("\nProgram terminated by user.")


if __name__ == '__main__':
    main_thread()


