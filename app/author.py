class Author:
    def __init__(self, dict) -> None:
        self._dict = dict
    
    @property
    def username(self) -> str:
        """
        Returns the author's identifier.
        """
        
        return self._dict['identifier']['value']
    
    @property
    def name(self) -> str:
        """
        Returns the author's display name.
        """
        
        return self._dict['name']
    
    @property
    def avatar_url(self) -> str | None:
        """
        Returns the author's display avatar source url.
        """
        
        return self._dict['image'] if self._dict['image'] != "" else None
    
    @property
    def profile_url(self) -> str:
        """
        Returns the author's profile url.
        """
        
        return self._dict['url']
    
    def to_dict(self) -> dict:
        """
        Returns the author's info into a dictionary.
        """
        return {
            'username': self.username,
            'name': self.name,
            'avatar': self.avatar_url,
            'url': self.profile_url
        }