from httpx import AsyncClient
from re import findall
from ast import literal_eval
from src.decoder import decoder

class SnaptikAsync(AsyncClient):
    '''
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    '''

    def __init__(self, tiktok_url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/86.0.4240.111 Safari/537.36'
            }
        self.tiktok_url = tiktok_url

    async def get_media(self):
        '''
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        '''
        resp = await self.get(
            'https://snaptik.app/abc2.php',
            params={
                'url': self.tiktok_url,
                'lang': 'en',
                **dict(
                    findall(
                        'name="(token)" value="(.*?)"',
                        (await self.get('https://snaptik.app/en')).text))},
        )
        if 'error_api_web;' in resp.text or 'Error:' in resp.text:
            raise InvalidUrl()
        
        dec = decoder(*literal_eval(
            findall(
                r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',
                resp.text
            )[0]
        ))
        
        try:
            name = findall(r'<div class=\\"video-title\\">(.*?)</div>', dec)[0].encode('latin-1').decode('utf-8')
        except:
            name = ''
        
        link = findall(r'<a href=\\"(https?://[\w\./\-&?=]+)\\" class=\\"button download-file mt-3\\" ', dec)
        if(len(link) == 0):
            token =  findall(r'<button class=\\"button btn-render\\" data-token=\\"(.*?)\\" data-ad=\\"true\\" data-event=\\"click_render\\" rel=\\"nofollow\\">', dec)[0]
            resp2 = await self.get(
            'https://snaptik.app/render.php',
            params={
                'token': token,
                },
            )
            if 'error_api_web;' in resp2.text or 'Error:' in resp2.text:
                raise InvalidUrl()

            linkv = findall(r'\",\"task_url\":\"(.*?)\",\"status\"', resp2.text)[0]
            resp3 = await self.get(linkv)
            link = findall(r'\"download_url\":\"(.*?)\"}', resp3.text)
        
        try:
            return {
                'name': name if name != 'No description' else '',
                'link': link[0]
            }
        except:
            return ""
        
    async def __aiter__(self):
        return await self.get_media()


async def snaptik(url: str):
    return await SnaptikAsync(url).get_media()



