# cfu

## Description

Checks for updates to webpages, sends a telegram message with the url if the website is updated. Once configured, set it up as a cronjob and get notified whenever a webpage is updated!

## Future Updates

- Add different ways of being updated (Email, logfile).
- Have an option to display what has updated
- Crawl a website and check for updates accross entire site

## Setup

### Telegram

You'll need to register a bot in telegram. Just message [BotFather](https://t.me/botfather) and follow the prompts.
Second, you'll need to obtain a chat id to send the messages to. To find your chat id message [RawDataBot](https://t.me/rawdatabot). The bot will respond with some JSON data. Look for the 'chat' object and then 'id' property. That's your chat id.

### Configuration file

`python3 cfu.py setup`

Starts an interactive prompt that will request your bot token, chat id, and if you'd like to have the url of the webpage included in your update messages.

## Add webpages

`python3 cfu.py add --name "Google" --url "https://google.com"`

Where --name option describes the name you'd like to give the website and --url is the site. cfu will now check for updates to this website whenever check command is executed

## Check for updates

`python3 cfu.py check`

Checks all added webpages for updates since last run. I set this up as a cronjob to run every 15 minutes.

## Help

`python3 cfu.py --help`
