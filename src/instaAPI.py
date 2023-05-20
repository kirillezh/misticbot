import instaloader
import logging
class instaAPI:
    def __init__(self, username, password):
        self.api = instaloader.Instaloader()
        try:
            self.api.login(username, password)
        except instaloader.exceptions.InstaloaderException:
            logging.error('InstaAPI: username does not exist')
            return
        except instaloader.exceptions.BadCredentialsException:
            logging.error('InstaAPI: password is wrong')
            return
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            logging.error('InstaAPI: need 2FA')
            return
        except:
            logging.error('InstaAPI: login error')
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
