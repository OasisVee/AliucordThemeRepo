from operator import ge
from numpy import int32
from time import sleep
import json
import os
import shutil
aliucordpackagename = "com.aliucord/com.discord.app.AppActivity\$Main"
startcommand = " adb shell am start -n " + aliucordpackagename
stopcommand = "adb shell am force-stop com.aliucord"
screenshotCommand = "adb exec-out screencap -p > "
projectDir = r"C:\Users\manti\Desktop\projeler\themerScreenshoter"
escapeCommand = "adb shell input keyevent 4"
openSettingsPage = "adb shell input tap 937 2246"
getFile = r"adb pull sdcard/Aliucord/settings/Themer.json C:\Users\manti\Desktop\projeler\themerScreenshoter"
sendFile = r"adb push C:\Users\manti\Desktop\projeler\themerScreenshoter\Themer.json sdcard/Aliucord/settings/Themer.json"
sendCommand = r"adb push C:\Users\manti\Desktop\projeler\themerScreenshoter\themes\{guh} sdcard/Aliucord/themes/{guh}"


def getThemeName(themeFileName):
    theme = getTheme(themeFileName)
    if "manifest" in theme:
        return theme["manifest"]["name"]
    else:
        return theme["name"]


def getTheme(themeFileName: str):
    with open("themes/" + themeFileName, encoding="utf-8") as f:
        theme = json.load(f)
    return theme


def generateScreenShots(themeFileName: str):
    themeName = getThemeName(themeFileName)
    os.system(stopcommand)
    os.system(getFile)
    with open("Themer.json", "w") as f:
        f.write(json.dumps({themeName + '-enabled': True,
                "transparencyMode": 3 if isFullTransparent(themeFileName) else 0}, indent=4))
    os.system(sendFile)
    os.system(sendCommand.format(guh=themeFileName))
    os.system(startcommand)
    sleep(8)

    dirName = themeFileName.removesuffix(".json")
    try:
        os.mkdir(projectDir + "/screenshots/" + dirName)
    except:
        pass

    os.system(screenshotCommand + "screenshots/"+dirName+"/0.png")
    os.system(escapeCommand)
    os.system(screenshotCommand + "screenshots/"+dirName+"/1.png")
    os.system(openSettingsPage)
    sleep(1)
    os.system(screenshotCommand + "screenshots/"+dirName+"/2.png")


def validateFileName(fileName: str):
    return "".join([x if x.isalnum() else "_" for x in fileName])


def getUnscreenShottedThemes():
    themes = os.listdir("themes")
    themesToScreenshoted = []
    for theme in themes:
        if not ((os.path.isdir("screenshots/" + theme.removesuffix(".json"))) and
                len(os.listdir("screenshots/" + theme.removesuffix(".json"))) == 3):
            themesToScreenshoted.append(theme)
    return themesToScreenshoted


def isColorTransparent(color: str):
    color = str(color)
    if(color.isnumeric()):
        return (int(color) & 0xFF000000) != 0xFF000000
    return False


def isFullTransparent(them):
    theme = getTheme(them)
    if "simple_colors" in theme and ("background" in theme["simple_colors"] and isColorTransparent(theme["simple_colors"]["background"]) or ("background_secondary" in theme["simple_colors"] and isColorTransparent(theme["simple_colors"]["background_secondary"]))):
        return True
    if "colors" in them:
        for a in them["colors"]:

            if (a.startswith("primary_dark") and isColorTransparent(int32(them["colors"][a]))):
                return True
        return False


def generateThemeList():
    themeObjects = []

    for a in os.listdir("themes"):
        theme = getTheme(a)
        jsonObj = {}
        if "manifest" in theme:
            jsonObj = {"name": theme["manifest"]["name"], "author": theme["manifest"]["author"],
                       "version": theme["manifest"]["version"] if "version" in theme["manifest"] else "1.0"}
        else:
            jsonObj = {
                "name": theme["name"], "author": theme["author"], "version": theme["version"]}
        jsonObj["fileName"] = a

        themeObjects.append(jsonObj)
    with open("themeList.json", "w+", encoding="utf-8") as f:
        json.dump(themeObjects, f, indent=4)


def getAllThemes():
    return os.listdir("themes")


def deleteNormalThemeScreenshots():
    themes = []
    with open("themeList.json", "r+", encoding="utf-8") as f:
        themes = json.load(f)

    for theme in themes:
        if (theme["transparencyMode"] == 0):
            dirName = theme["fileName"].removesuffix(".json")
            print(dirName)
            try:
                shutil.rmtree(projectDir + "/screenshots/" + dirName)
                print("guhcess")
            except Exception as e:
                print(e)


def guh():
    themeObjects = []
    with open("themeList.json", "r+", encoding="utf-8") as f:
        themeObjects = json.load(f)

        for theme in themeObjects:
            themeName = theme["fileName"]
            if isFullTransparent(themeName):
                theme["transparencyMode"] = 3
            else:
                theme["transparencyMode"] = 0
            theme["screenshots"] = ["/screenshots/" +
                                    theme["fileName"] + "/"+str(i)+".png" for i in range(3)]
        open('themeList.json', 'w').close()

        f.write(json.dumps(themeObjects, indent=4))

for theme in getUnscreenShottedThemes():
    generateScreenShots(theme)

print(len(getUnscreenShottedThemes()))
# generateThemeList()
# guh()
