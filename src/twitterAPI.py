import requests
import json
import re
import urllib.parse

class twitterAPI:
    def __init__(self, ):
        self.features = {
                "responsive_web_graphql_exclude_directive_enabled":True,
                "verified_phone_label_enabled":False,
                "responsive_web_graphql_timeline_navigation_enabled":True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,
                "tweetypie_unmention_optimization_enabled": True,    
                "vibe_api_enabled": False,
                "responsive_web_edit_tweet_api_enabled": False,   
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": False,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled":True,
                "tweet_awards_web_tipping_enabled":False,
                "freedom_of_speech_not_reach_fetch_enabled":False,
                "standardized_nudges_misinfo": False,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":False,
                "interactive_text_enabled": False,   "responsive_web_twitter_blue_verified_badge_is_enabled":True,
                "responsive_web_text_conversations_enabled":False,
                "longform_notetweets_richtext_consumption_enabled":False,
                "responsive_web_enhance_cards_enabled":False
            }
        self.variables = {
                "with_rux_injections":False,
                "includePromotedContent":True,
                "withCommunity":True,
                "withQuickPromoteEligibilityTweetFields":True,
                "withBirdwatchNotes":True,
                "withDownvotePerspective":False,
                "withReactionsMetadata":False,
                "withReactionsPerspective":False,
                "withVoice":True,
                "withV2Timeline":True
            }


    def get_tokens(self, tweet_url):
        html = requests.get(tweet_url)
        assert html.status_code == 200, f'Failed to get tweet page. Status code: {html.status_code}.  Tweet url: {tweet_url}'
        mainjs_url = re.findall(r'https://abs.twimg.com/responsive-web/client-web-legacy/main.[^\.]+.js', html.text)
        assert mainjs_url is not None and len(
            mainjs_url) > 0, f'Failed to find main.js file. Tweet url: {tweet_url}'
        mainjs_url = mainjs_url[0]
        mainjs = requests.get(mainjs_url)
        assert mainjs.status_code == 200, f'Failed to get main.js file. Status code: {mainjs.status_code}. Tweet url: {tweet_url}'
        bearer_token = re.findall(r'AAAAAAAAA[^"]+', mainjs.text)
        assert bearer_token is not None and len(
            bearer_token) > 0, f'Failed to find bearer token. Tweet url: {tweet_url}, main.js url: {mainjs_url}'
        bearer_token = bearer_token[0]
        with requests.Session() as s:
            s.headers.update({
                "user-agent"	:	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
                "accept"	:	"*/*",
                "accept-language"	:	"de,en-US;q=0.7,en;q=0.3",
                "accept-encoding"	:	"gzip, deflate, br",
                "te"	:	"trailers",})
            s.headers.update({"authorization"	:	f"Bearer {bearer_token}"})
            guest_token = s.post(
                "https://api.twitter.com/1.1/guest/activate.json").json()["guest_token"]
        assert guest_token is not None, f'Failed to find guest token. Tweet url: {tweet_url}, main.js url: {mainjs_url}'
        return bearer_token, guest_token


    def get_details_url(self, tweet_id):
        self.variables['focalTweetId'] = tweet_id
        return f"https://twitter.com/i/api/graphql/wTXkouwCKcMNQtY-NcDgAA/TweetDetail?variables={urllib.parse.quote(json.dumps(self.variables))}&features={urllib.parse.quote(json.dumps(self.features))}"


    def get_tweet_details(self, tweet_url, guest_token, bearer_token):
        tweet_id = re.findall(r'(?<=status/)\d+', tweet_url)
        assert tweet_id is not None and len(
            tweet_id) == 1, f'Could not parse tweet id from your url. Tweet url: {tweet_url}'
        tweet_id = tweet_id[0]
        url = self.get_details_url(tweet_id)

        details = requests.get(url, headers={
            'authorization': f'Bearer {bearer_token}',
            'x-guest-token': guest_token,
        })
        max_retries = 10
        cur_retry = 0
        while details.status_code == 400 and cur_retry < max_retries:
            try:
                error_json = json.loads(details.text)
            except:
                assert False, f'Failed to parse json from details error. details text: {details.text}   Status code: {details.status_code}.  Tweet url: {tweet_url}'

            assert "errors" in error_json, f'Failed to find errors in details error json.   Status code: {details.status_code}.  Tweet url: {tweet_url}'

            needed_variable_pattern = re.compile(r"Variable '([^']+)'")
            needed_features_pattern = re.compile(r'The following features cannot be null: ([^"]+)')

            for error in error_json["errors"]:
                needed_vars = needed_variable_pattern.findall(error["message"])
                for needed_var in needed_vars:
                    self.variables[needed_var] = True

                needed_features = needed_features_pattern.findall(error["message"])
                for nf in needed_features:
                    for self.feature in nf.split(','):
                        self.features[self.feature.strip()] = True

            url = self.get_details_url(tweet_id)

            details = requests.get(url, headers={
                'authorization': f'Bearer {bearer_token}',
                'x-guest-token': guest_token,
            })

            cur_retry += 1

        return details

    def get_tweet_status_id(self, tweet_url) :
        sid_patern = r'https://twitter\.com/[^/]+/status/(\d+)'
        if tweet_url[len(tweet_url)-1] != "/" :
            tweet_url = tweet_url + "/"

        match = re.findall(sid_patern, tweet_url)
        if len(match) == 0 :
            print("error, could not get status id from this tweet url :", tweet_url)
            exit()
        status_id = match[0]
        return status_id

    def get_associated_media_id(self, j, tweet_url):
        sid = self.get_tweet_status_id(tweet_url)
        pattern = r'"expanded_url"\s*:\s*"https://twitter\.com/[^/]+/status/'+sid+'/[^"]+",\s*"id_str"\s*:\s*"\d+",'
        matches = re.findall(pattern, j)
        if len(matches) > 0 :
            target = matches[0]
            target = target[0:len(target)-1]
            return json.loads("{"+target+"}")["id_str"]
        return None


    def extract_mp4s(self, tweet_url):
        bearer_token, guest_token = self.get_tokens(tweet_url)
        resp = self.get_tweet_details(tweet_url, guest_token, bearer_token)
        j = resp.text
        amplitude_pattern = re.compile(r'(https://video.twimg.com/amplify_video/(\d+)/vid/(\d+x\d+)/[^.]+.mp4\?tag=\d+)')
        ext_tw_pattern = re.compile(r'(https://video.twimg.com/ext_tw_video/(\d+)/pu/vid/(\d+x\d+)/[^.]+.mp4\?tag=\d+)')

        tweet_video_pattern = re.compile(r'https://video.twimg.com/tweet_video/[^"]+')
        container_pattern = re.compile(r'https://video.twimg.com/[^"]*container=fmp4')
        media_id = self.get_associated_media_id(j, tweet_url)
        matches = amplitude_pattern.findall(j)
        matches += ext_tw_pattern.findall(j)
        container_matches = container_pattern.findall(j)

        tweet_video_matches = tweet_video_pattern.findall(j)

        if len(matches) == 0 and len(tweet_video_matches) > 0:
            return tweet_video_matches, resp

        results = {}

        for match in matches:
            url, tweet_id, resolution = match
            if tweet_id not in results:
                results[tweet_id] = {'resolution': resolution, 'url': url}
            else:
                my_dims = [int(x) for x in resolution.split('x')]
                their_dims = [int(x) for x in results[tweet_id]['resolution'].split('x')]

                if my_dims[0] * my_dims[1] > their_dims[0] * their_dims[1]:
                    results[tweet_id] = {'resolution': resolution, 'url': url}
        if media_id:
            all_urls = []
            for twid in results :
                all_urls.append(results[twid]["url"])
            all_urls += container_matches
            url_with_media_id = []
            for url in all_urls :
                if url.__contains__(media_id) :
                    url_with_media_id.append(url)
            if len(url_with_media_id) > 0:
                return url_with_media_id, resp
        if len(container_matches) > 0:
            return container_matches, resp

    def getvideo(self, url):
        video, desc = self.extract_mp4s(url)
        info = {
            'link': video[0],
            'name': re.sub(r'https://t.co\S+', '', desc.json()['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][3]['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
        }
        return info