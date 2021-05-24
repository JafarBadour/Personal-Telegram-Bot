import time
import telepot
import os
import subprocess
import traceback

import _thread


class PersonalTelBot(telepot.Bot):
    def __init__(self, api_token, password, whitelist):
        """

        :param api_token: API TOKEN for your telegram bot you can get from @BotFather  , you can register it there
        :param password:  Your password on your Linux/ MacOs system, it will be used for sudo commands or similar
        :param whitelist: path to whitelisted chat_id telegram accounts, you dont need to create, it will be created
                          on first run and then will be appended on every login
        """
        super(PersonalTelBot, self).__init__(api_token)
        self.password = password
        self.whitelist = whitelist

    import subprocess


class BashCommandHandler(PersonalTelBot):

    def __init__(self, api_token, password, whitelist):
        if not os.path.isfile(whitelist):
            open(whitelist, 'w').write('')

        super(BashCommandHandler, self).__init__(api_token, password, whitelist)

    def run_command(self, s: str, chat_id):
        s = s.replace('  ', ' ')
        tokens = s.split(' ')
        command = tokens[0].lower()
        tokens[0] = command
        print('Tokens are\n', tokens)

        if command == 'jlogin':
            print('Login attempt')
            print(' '.join(tokens), 'vs', self.password)
            if ' '.join(tokens[1:]) != self.password:
                return 'wrong password'
            else:
                f = open(self.whitelist, 'r')
                ids = f.readlines()
                f.close()
                if chat_id in ids:
                    return 'Already logged in'
                f = open(self.whitelist, 'a')
                f.write('\n' + str(chat_id))
                f.close()
                return 'Right password, delete message from your end'
        f = open(self.whitelist, 'r')
        ids = list(map(int,
                       map(lambda x: x.strip('\n'), f.readlines())))
        f.close()
        print('New command from a logged in account with chat id', chat_id, ids)
        if not chat_id in ids:
            return 'Not logged in'

        if command == 'jlogout':
            ids.remove(chat_id)

            f = open(self.whitelist, 'w')
            f.write('\n'.join(ids))
            f.close()
            return 'Logged out'

        if command == 'cd':
            try:
                dir = tokens[1]
                print(dir[0], 'directory token')
                tokens[1] = tokens[1].replace('~', '/home/jafar')  ## CHange to whatever you need
                cur = os.curdir
                cur = os.path.join(cur, ' '.join(tokens[1:]))
                os.chdir(cur)
                print('Changing directory to', cur)
                return os.path.abspath(os.curdir)
            except Exception:
                print('error changing dir')
                print(traceback.format_exc())
                return 'error changing dir'

        if command == 'sendme':
            if len(tokens) < 3:
                self.sendMessage(chat_id, 'Error if you want a video write sendme video vidname\n'
                                          'otherwise if you want file write sendme file filename\n'
                                          'Options are \'video\', \'file\' or \'photo\'')

            path = os.path.join(os.curdir, ' '.join(tokens[2:]))
            functions = {
                'video': self.sendVideo,
                'photo': self.sendPhoto,
                'file': self.sendDocument
            }
            print('Sending file with path', path)
            self.sendMessage(chat_id, f'On it wait, sending file with path:  {path}')
            if not os.path.isfile(path):
                return 'No file in current directory'
            functions[tokens[1]](chat_id, open(path, 'rb'), caption=' '.join(tokens[3:]))
            return 'Success'

        def encode(out):
            if out is None:
                return ''
            return '\n'.join([str(outi, encoding='utf-8') for outi in out])

        print('Running command')
        bash_command = ' '.join(tokens)
        if tokens[0] == 'sudo':
            bash_command = f'echo {self.password} | ' + bash_command

        p = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        # print(list(p.stdout))
        # print(p.stderr)
        print('Ended command')
        return 'R:\n' + encode(p.stdout) + '\n' + encode(p.stderr)

    def process_command(self, s, chat_id):
        try:
            stdout = self.run_command(s, chat_id)
            stdout = stdout.replace('\n\n', '\n')
            for line in stdout.split('\n'):
                if len(line) == 0:
                    continue
                self.sendMessage(chat_id, line)
        except Exception:
            print(traceback.format_exc())
            self.sendMessage(chat_id, 'Command parsing error')


# bash_handler = BashCommandHandler(
#     api_token='HERE API TOKEN from @botfather @BotFather',
#     password='Your device password',
#     whitelist='path to whitelisted chat_id telegram accounts, you dont need to create, it will be created '
#               'on first run and then will be appended on every login'
# )

bash_handler = BashCommandHandler(
    api_token='1470811324:AAGwv7qdGNuztGVhIkuHsVRyeikcHqlqbbI',
    password='bakhetle',
    whitelist='/home/jafar/PycharmProjects/Personal-Telegram-Bot/whitelist'
)
last_date_path = '/home/jafar/PycharmProjects/Personal-Telegram-Bot/last_date'


def timed_update(bash_handler, command_text, chat_id):
    bash_handler.process_command(command_text, chat_id)


if __name__ == '__main__':

    wait_time = 10  # this variable usually is 2 seconds but grows to 2 minutes if last time active is more
    # than 1 hour ago

    try:
        last_date = int(open(last_date_path).read())
    except:
        last_date = 0
        open(last_date_path, 'w').write('0')

    while True:
        # print(TelegramBot.getMe())
        try:

            messages = bash_handler.getUpdates(offset=last_date + 1)
            print('last date id is', last_date, len(messages))
            if len(messages) > 0:
                wait_time = 2
            else:
                wait_time = min(wait_time + 0.5, 120)
            for message_ in messages:
                if 'message' not in message_:
                    continue
                message = message_['message']
                chat_id = message['from']['id']

                print(message_)

                if 'text' in message:
                    _thread.start_new_thread(timed_update, (bash_handler, message['text'], chat_id))
                else:
                    bash_handler.sendMessage(chat_id, 'Command error check logs on serverside (your device)')
            last_date = last_date if len(messages) == 0 else messages[-1]['update_id']
            open(last_date_path, 'w').write(str(last_date))
        except Exception:
            print(traceback.format_exc())

        time.sleep(wait_time)
