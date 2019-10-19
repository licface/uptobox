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
        download_url = content.get('data').get('dlLink')
        debug(download_url = download_url, debug = debugx)
        clipboard.copy(download_url)
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
            print make_colors("Internet Download Manager NOT FOUND !", 'lr', 'lw', ['blink'])
            print make_colors('Download with wget (buildin) ...', 'b', 'ly')
            
            if altname:
                download_path = os.path.join(download_path, altname)
                print make_colors("SAVE AS ", 'lc') + " : " + make_colors(download_path, 'lw', 'lr')
            wget.download(url, download_path)
            
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
            
            download_url = self.generate_link(args.URL, args.token, args.download, args.path, args.saveas, args.prompt, args.debug)
            print make_colors("GENERATE", 'lc') + " : " + make_colors(download_url, 'lw', 'lr')
            
                
        
if __name__ == '__main__':
    a = uptobox()
    a.usage()
    #a.get_user_data(debugx= True)
    #a.generate_link("http://uptobox.com/sdi0ap5pw5fv", debugx = True)
        
    