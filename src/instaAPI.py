import instaloader
import logging
class instaAPI:
    def __init__(self, username, password):
        self.api = instaloader.Instaloader()
        try:
            #self.api.login(username, password)
            self.api.load_session_from_file(username, 'instauser')
        except instaloader.exceptions.InstaloaderException as s:
            logging.error('InstaAPI: username does not exist\n'+s)
            return
        except instaloader.exceptions.BadCredentialsException as s:
            logging.error('InstaAPI: password is wrong\n'+s)
            return
        except instaloader.exceptions.TwoFactorAuthRequiredException as s:
            logging.error('InstaAPI: need 2FA\n'+s)
            return
        except Exception as s:
            logging.error('InstaAPI: login error\n'+s)
            return
    def searchid(self, text):
        split_text = text.split('/')
        for i in range(0, len(split_text)):
            if "reel" in split_text[i]:
                id = split_text[i+1]
        try:
            return id
        except:
            return ''
        
    def download_video(self, url):
        post = instaloader.Post.from_shortcode(self.api.context, self.searchid(url))
        info = {
            'link':post.video_url,
            'name': post.caption
        }
        return info
