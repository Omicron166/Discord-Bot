<img src="https://www.adweek.com/wp-content/uploads/2021/01/DiscordLogo3-2.jpg" height="100">

# A simple discord bot that just plays music

## Feature:

- Join the channel you're in
- Play from Youtube / Any platform supported by yt-dlp
- Skip command
- Pause command
- Stop command
- Resume command
- Song queue

## To do:

- Help command
- Some optimization until it runs smooth on a raspberry pi 3b

## Setup guide:
### For windows users:
If you are a normie who just wants to use the bot, you can download the compiled version with all it's dependencies from [releases](https://github.com/Omicron166/Discord-Bot/releases/latest) and run it.
![](./images/release.jpg)
<br> Also don't forget to put your token and prefix in `config.json`
### For Linux users:
- Clone the repo
- Run a `pip install -r requirements.txt` or a `pipenv install -r requirements.txt`, pick your favourite option.
- Fill the `config.json`.
- Check you have ffmpeg installed
