# cfu

## Description

Python script that checks for textual updates to webpages, sends a telegram message with the url if the website is updated. Once configured, set it up as a cronjob and get notified whenever a webpage is updated!

## Future Updates

- Add different ways of being updated (Email, logfile).
- Ability to choose to be updated when script,style or a specific divs are updated
- Have an option to display what has updated
- Crawl a website and check for updates accross entire site

## Setup

### Telegram

You'll need to register a bot in telegram. Just message [BotFather](https://t.me/botfather) and follow the prompts. The bot will respond with your new bot token.
You'll also need to obtain a chat id to send the messages to. To find your chat id message [RawDataBot](https://t.me/rawdatabot). The bot will respond with some JSON data. Look for the 'chat' object and then 'id' property. That's your chat id.

### Configuration file

`python3 cfu.py setup`

Starts an interactive prompt that will request your bot token, chat id, and if you'd like to have the url of the webpage included in your update messages.

## Add webpages

`python3 cfu.py add`

Starts an interactive prompt that will request the name of the website, url, and the way you'd like the script to store the value of the website (hash is the only implemented option currently).

## Check for updates

`python3 cfu.py check`

Checks all added webpages for any updates since last run.

## Help

`python3 cfu.py --help`
