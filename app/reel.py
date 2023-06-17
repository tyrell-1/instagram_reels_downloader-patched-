import asyncio
import json
import re
import time
from datetime import datetime
from functools import lru_cache

import aiohttp
import requests
from bs4 import BeautifulSoup

from author import Author
from exceptions import InvalidURL, ScrapingError


class InstagramReel:
    def __init__(self, url: str) -> None:
        """
        Keyword arguments:
        url -- The Reel URL.
        """
        
        self.url = url.strip().split('?')[0]
        url_regex = re.compile(r'https?://www\.instagram\.com/reel/(.*)')
        match = url_regex.match(url)
        if not match:
            raise InvalidURL()
        
        asyncio.run(self._scrape())
        self._parse_stats()
        

    async def _scrape(self) -> None:
        """Gets the json file which contains the reel data.

        Return: NO RETURN.
        """
        
        async with aiohttp.ClientSession() as session:
            t1 = time.time()
            async with session.get(self.url) as response:
                content = await response.text()
                t2 = time.time()
                self.elapsed = t2 - t1
                soup = BeautifulSoup(content, 'html.parser')
                script = soup.find('script', {'type': 'application/ld+json'})
                if not script:
                    raise ScrapingError
                self._json = json.loads(script.text)
            

    def _parse_stats(self) -> None:
        """Parses the videos stats from the json object
        
        Return: NO RETURN.
        """
        
        stats = self._json['interactionStatistic']
        for i in range(len(stats)):
            match stats[i]['interactionType']:
                case "https://schema.org/CommentAction":
                    exec(f'self._comment_count = int({stats[i]["userInteractionCount"]})')
                case "http://schema.org/LikeAction":
                    exec(f'self._like_count = int({stats[i]["userInteractionCount"]})')
                case "http://schema.org/WatchAction":
                    exec(f'self._views = int({stats[i]["userInteractionCount"]})')
                
    @property
    def video_url(self) -> str:
        """
        Returns the reel video url.
        """

        return self.url
    
    @property
    def source_url(self) -> str:
        """
        Returns the reel source url (instagram cdn url).
        """
        
        return self._json['video'][0]['contentUrl']
    
    @property
    @lru_cache
    def created_at(self) -> datetime:
        """
        Returns the creation date of the reel.
        """
        
        return datetime.strptime(self._json['video'][0]['uploadDate'], "%Y-%m-%dT%H:%M:%S%z")
    
    @property
    def description(self) -> str:
        """
        Returns the reel description.
        """

        return self._json['video'][0]['description']
    
    @property
    def caption(self) -> str:
        """
        Returns the reel caption.
        """
        return self._json['video'][0]['caption']
    
    @property
    def thumbnail_url(self) -> str:
        """
        Returns the reel thumbnail source (instagram cdn url).
        """
        return self._json['video'][0]['thumbnailUrl']
    
    @property
    def comment_count(self) -> int:
        """
        Returns the reel comment count.
        """
        
        return self._comment_count
    
    @property
    def like_count(self) -> int:
        """
        Returns the reel likes count.
        """
        
        return self._like_count
    
    @property
    def views(self) -> int:
        """
        Returns the reel views.
        """
        
        return self._views
    
    @property
    def author(self) -> Author:
        """
        Returns the reel author info.
        """
        
        return Author(self._json['author'])
    
    @property
    @lru_cache
    def hashtags(self) -> list:
        """
        Returns the reel hashtags.
        """
        
        desc = self.description
        regex = re.compile(r"#(\w+)")
        hashtags = regex.findall(desc)
        return [f'#{hashtag}' for hashtag in hashtags]
    
    def to_dict(self) -> dict:
        """
        Returns the reel info into a dictionary.
        """
        
        return {
            'url': self.video_url,
            'source': self.source_url,
            'thumbnail': self.thumbnail_url,
            'created_at': self._json['video'][0]['uploadDate'],
            'description': self.description,
            'caption': self.caption,
            'stats': {
                'likes': self.like_count,
                'comments': self.comment_count,
                'views': self.views
            },
            'author': self.author.to_dict(),
            'hashtags': self.hashtags
        }
    
    def save(self, filename: str = None) -> None:
        """Saves the reel to file.
        
        Keyword arguments:
        filename -- the reel filename.
        
        Example:
        reel.save(filename='reels/video.mp4')
        
        Returns: Nothing
        """
        
        res = requests.get(self.source_url)
        with open(f"{filename if filename else str(datetime.now().date())}{'.mp4' if not filename.endswith('.mp4') else ''}", 'wb') as out:
            out.write(res.content)
            out.close()