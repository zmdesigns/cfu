"""
checkForUpdates.py
    Checks for updates to webpages
"""

from bs4 import BeautifulSoup as bs
import hashlib
from urllib.request import (urlopen)
import telebot
import os
import click
import configparser
import difflib

def getTextContent(url):
    soup = bs(urlopen(url),features="lxml")
    textContent = ''

    for not_wanted_tag in soup.find_all(['script','style','Cdata']):
        not_wanted_tag.decompose()

    for div_tag in soup.find_all('div'):
        textContent += div_tag.getText()

    textContent = " ".join(textContent.split())
    return textContent

def getHash(url):
    textContent = getTextContent(url)
    hashValue = hashlib.md5(textContent.encode("utf-8")).hexdigest()
    return hashValue
    

class Cfu(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        scriptDir = os.path.dirname(__file__)
        self.configFilePath = os.path.join(scriptDir, 'configCfu.ini')

        if not os.path.exists(self.configFilePath):
            self.setup('','','')
        else:
            self.config.read(self.configFilePath)

    def setup(self, botToken, chatId, includeUrl):
        self.config['settings'] = {'bottoken': botToken, 'chatid': chatId, 'url_in_msg': includeUrl}
        self.writeConfig()

    def writeConfig(self):
        """ Write config object to configuration file """
        with open(self.configFilePath, 'w') as configFile:
            self.config.write(configFile)

    def update(self, sectionName, newValue):
        """ Update the value in config and send a message """
        self.sendMessage(sectionName)

        if self.config[sectionName]['value_type'] == 'full':
            filename = sectionName + '.txt'
            with open(filename, 'w') as f:
                f.write(newValue)
        else:
            self.config[sectionName]['value'] = newValue
            self.writeConfig()

    def sendMessage(self, sectionName):
        message = sectionName + ' has been updated!';
        if self.config['settings']['url_in_msg'] == 'yes':
            message += self.config[sectionName]['url']

        botToken = self.config['settings']['bottoken']
        chatId = self.config['settings']['chatid']
        bot = telebot.TeleBot(botToken)
        bot.send_message(chatId, message)

    def add(self, name, url, vtype):
        """ Add a website to config """
        value = ''
        if vtype == 'hash':
            value = getHash(url)
        if vtype == 'full':
            textContents = getTextContent(url)
            value = name + '.txt'
            with open(value, 'w') as f:
                f.write(textContents)

        self.config[name] = {'url': url, 'value': value, 'value_type': vtype}
        self.writeConfig()

    def check(self, name):
        """ Compare value stored from last check to live, if it's different, it's updated """
        url = self.config[name]['url']
        value = ''
        newValue = ''
        valueType = self.config[name]['value_type']
        
        if valueType == 'hash':
            value = self.config[name]['value']
            newValue = getHash(url)
        elif valueType == 'full':
            with open(self.config[name]['value'], 'r') as file:
                value = file.read()
            newValue = getTextContent(url)

        if newValue != value:
            self.update(name, newValue)
        

@click.group()
@click.pass_context
def cli(ctx):
    """ Checks for updates to websites in configuratin file """
    ctx.obj = Cfu()

@cli.command("setup")
@click.option("--bottoken", prompt="Telegram bot token: ")
@click.option("--chatid", prompt="Telegram chat id: ")
@click.option("--includeurl", prompt="Include URL in update messages? (yes/no): ", type=click.Choice(['yes', 'no'], case_sensitive=False))
@click.pass_obj
def setup(cfu, bottoken, chatid, includeurl):
    """ Setup configuration file """
    cfu.setup(bottoken, chatid, includeurl)

@cli.command("add")
@click.option("--name", prompt="Your name for the website: ")
@click.option("--url", prompt="Url: ")
@click.option("--vtype", prompt="Type of storage/comparison (hash,full): ", type=click.Choice(['hash','full'], case_sensitive=False))
@click.pass_obj
def add(cfu, name, url, vtype):
    """ Add a webpage to check for updates """
    if name in cfu.config:
        click.echo("A website by the name of " + name + " is already in use")
        return False

    cfu.add(name, url, vtype)
    
@cli.command("check")
@click.pass_obj
def check(cfu):
    """ Check for updates to websites listed in configuration file """
    if (len(cfu.config.sections()) <= 1):
        click.echo("No Websites to check, add a website with add command")
    else:
        for section in cfu.config.sections():
            if section == 'settings':
                continue
            if 'url' not in cfu.config[section]:
                continue

            cfu.check(section)

if __name__ == '__main__':
    cli()