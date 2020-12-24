# Personal Telegram Bot to run bash commands and send files to end user

Code is pretty simple

Steps to run


* Create new telegram bot using @BotFather from telegram. The @BotFather will send you an
API token then you can insert in the code, check below
  
* Insert your password and paths to two files ```last_date``` and ```whitelist```
    
  ```lastdate``` contains the date of the last message processed by the bot

  ```whitelist``` contains ids of telegram accounts that can access the functionalities
```python
bash_handler = BashCommandHandler(
    api_token='14*******:A****************VRyeikcHqlqbbI', # Here is your API_TOKEN
    password='*********', # password of the device that you run the code on
    whitelist='/home/jafar/PycharmProjects/Personal-Telegram-Bot/whitelist' # path of the file where you store that 
    # whitelisted accounts
)
last_date_path = '/home/jafar/PycharmProjects/Personal-Telegram-Bot/last_date'
```

## Using the bot

* ```jlogin *password*``` you type password of the device

    You will get a verdict

* ```jlogout``` to logout from this account

* ```sendme file relative_path``` where ```relative_path``` is the relative path for the file required to be sent

* ```sendme photo relative_path``` to send as a photo
  
* ```sendme video relative_path``` to send as a video

* ```sudo nordvpn connect germany``` this is just a bash command to run on your server machine


* Any other command is possible here is an animated gif for the possibility

![Demo](https://github.com/JafarBadour/Personal-Telegram-Bot/blob/master/animated.gif)


