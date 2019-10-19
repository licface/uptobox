import os
import sys
import argparse
import requests
import configset
from pydebugger.debug import debug
from make_colors import make_colors
import re
import urlparse
import json
import clipboard
from pywget import wget
import traceback
import time

class uptobox(object):
    def __init__(self):
        super(uptobox, self)
        self.url = 'https://uptobox.com/api/'
        self.CONFIG = configset.configset()
        self.configname = 'uptobox.ini'
        self.CONFIG.configname = self.configname
        
    def get_token(self):
        token = self.CONFIG.read_config('AUTH', 'token')
        if not token:
            print make_colors('NO TOKEN FOUND !', 'lr', 'lw', ['blink'])
            return False
        return token
    
    def get_user_data(self, token = None, debugx = False):
        if not token:
            token = self.CONFIG.read_config('AUTH', 'token')
        if not token:
            print make_colors('NO TOKEN FOUND !', 'lr', 'lw', ['blink'])
            return False
        url = "user/me"
        url = self.url + url
        params = {
            'token': token,
        }
        debug(token = token, debug = debugx)
        a = requests.get(url, params= params)
        content = a.content
        debug(content = content, debug = debugx)
        
    def generate_link(self, link, token = None, downloadit = False, download_path = os.getcwd(), save_name = None, download_prompt = False, debugx = False):
        url = self.url + 'link'
        debug(url = url, debug = debugx)
        file_code = urlparse.urlparse(link).path[1:]
        debug(file_code = file_code, debug = debugx)
        if not token:
            token = self.get_token()
            if not token:
                sys.exit(0)
        params = {
            'token': token,
            'file_code': file_code,
        }
        debug(params = params, debug = debugx)
        a = requests.get(url, params = params)
        content = json.loads(a.content)
        debug(content = content, debug = debugx)
        download_url = ''
        if not content.get('data').get('dlLink'):
            while 1:
                if content.get('data').get('waitingToken') and content.get('data').get('waiting'):
                    waitingToken = content.get('data').get('waitingToken')
                    waiting = content.get('data').get('waiting')
                    debug(waitingToken = waitingToken, debug = debugx)
                    debug(waiting = waiting, debug = debugx)
                    params = {
                        'token': token,
                        'file_code': file_code,
                        'waitingToken': waitingToken
                    }
                    a = requests.get(url, params = params)
                    content = json.loads(a.content)
                    debug(content = content, debug = debugx)                    
                    time.sleep(1)
                    sys.stdout.write(".")
                else:
                    download_url = content.get('data').get('dlLink')
        else:       
            download_url = content.get('data').get('dlLink')
        if not download_url:
            print make_colors("GENERATE FAILED !", 'lr', 'lw', ['blink'])
        debug(download_url = download_url, debug = debugx)
        clipboard.copy(str(download_url))
        if downloadit:
            self.download(download_url, download_path, save_name, download_prompt)
        return download_url
    
    def download(self, url, download_path = os.getcwd(), altname = None, prompt = False):
        print make_colors('start downloading ...', 'lr')
        try:
            import idm
            dm = idm.IDMan()
            dm.download(url, download_path, altname, confirm= prompt)
        except:
            traceback.format_exc()
            print make_colors("Internet Download Manager NOT FOUND !", 'lr', 'lw', ['blink'])
            print make_colors('Download with wget (buildin) ...', 'b', 'ly')
            
            if altname:
                download_path = os.path.join(download_path, altname)
                print make_colors("SAVE AS ", 'lc') + " : " + make_colors(download_path, 'lw', 'lr')
            wget.download(str(url), download_path)
            
    def usage(self):
        parser = argparse.ArgumentParser(formatter_class= argparse.RawTextHelpFormatter)
        parser.add_argument('URL', help = 'uptobox url, example: "http://uptobox.com/sdi0ap5pw5fv"', action = 'store')
        parser.add_argument('-d', '--download', help = 'Direct download', action = 'store_true')
        parser.add_argument('-p', '--path', help = 'Save download to path, if option "-d" not given, it would download direct too', action = 'store')
        parser.add_argument('-s', '--saveas', help = 'Save as other name', action = 'store')
        parser.add_argument('-T', '--token', help = 'Generate with spesific token not from configfile', action = 'store')
        parser.add_argument('-P', '--prompt', help = 'Prompt before download', action = 'store_true')
        parser.add_argument('-D', '--debug', help = 'Show debug process', action = 'store_true')
        if len(sys.argv) == 1:
            
            parser.print_help()
        else:
            IS_DOWNLOAD = False
            args = parser.parse_args()
            if args.path:
                IS_DOWNLOAD = True
            elif args.download:
                IS_DOWNLOAD = True
            else:
                IS_DOWNLOAD = False
            
            saveas = None
            if args.saveas:
                ext = os.path.splitext(args.saveas)
                debug(ext = ext, debug = args.debug)
                if not ext[1]:
                    download_url = self.generate_link(args.URL, args.token, False, args.path, args.saveas, args.prompt, args.debug)
                    debug(download_url = download_url, debug = args.debug)
                    print make_colors("GENERATE", 'lc') + " : " + make_colors(download_url, 'lw', 'lr')
                    ext1 = os.path.splitext(download_url)[1]
                    debug(ext1 = ext1, debug = args.debug)
                    saveas = ext[0] + ext1
                    debug(saveas = saveas, debug = args.debug)
                else:
                    download_url = self.generate_link(args.URL, args.token, False, args.path, args.saveas, args.prompt, args.debug)
                    debug(download_url = download_url, debug = args.debug)
                    ext1 = os.path.splitext(download_url)[1]
                    debug(ext1 = ext1, debug = args.debug)
                    if not ext[1] == ext1:
                        q = raw_input(make_colors('Do you want to save as other extention ? [y/n]: '))
                        if str(q).lower() == 'y':
                            saveas = args.saveas
                    else:
                        saveas = args.saveas
                debug(saveas = saveas, debug = args.debug)
                debug(download_url = download_url, debug = args.debug)
                self.download(download_url, args.path, saveas, args.prompt)
            else:   
                download_url = self.generate_link(args.URL, args.token, args.download, args.path, args.saveas, args.prompt, args.debug)
                print make_colors("GENERATE", 'lc') + " : " + make_colors(download_url, 'lw', 'lr')
            
                
        
if __name__ == '__main__':
    a = uptobox()
    a.usage()
    #a.get_user_data(debugx= True)
    #a.generate_link("http://uptobox.com/sdi0ap5pw5fv", debugx = True)
        
    