import os
import json
from socket import getnameinfo
from itsdangerous import json
import requests


def validateFileName(fileName: str):
    return "".join([x if x.isalnum() else "_" for x in fileName])


def downloadTheme(urla: str):
    url = urla.replace("\n", "")
    text = requests.get(url).text
    try:
        theme = json.loads(text)
        if "manifest" in theme:
            themename = theme["manifest"]["name"].replace("\n", "")
        else:
            themename = theme["name"].replace("\n", "")
        with open("themes/" + validateFileName(themename) + ".json", "w+", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(e)
        print(text)


def getAllThemes():
    with open("guh.json", "r") as f:
        themes = json.loads(f.read())
    return themes


def getTheme(themeFileName: str):
    if not ".json" in themeFileName:
        themeFileName += ".json"

    with open("themes/" + themeFileName, encoding="utf-8") as f:
        theme = json.load(f)
    return theme


def getNewThemes():
    newThemes = []
    themes = os.listdir("themes")
    themeNames = []
    with open("themeList.json", "r+", encoding="utf-8") as f:
        themeObjects = json.load(f)
        for theme in themeObjects:
            themeNames.append(theme["fileName"])
    for theme in themes:
        if theme.removesuffix(".json") not in themeNames:
            newThemes.append(theme)
    return newThemes


def downloadAllThemes():
    themes = getAllThemes()
    for a in themes:
        downloadTheme(a)


# downloadAllThemes()
# addNewThemesToJson()
