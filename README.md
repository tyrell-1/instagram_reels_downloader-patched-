## Instagram Reel Scraper
This project is an Instagram Reel scraper that uses the `aiohttp`, `BeautifulSoup` and `requests` libraries to fetch and parse JSON data from Instagram, extract hashtags from the reel description, and save the reel to file.

## Installation
To install this project, you will need to have Python 3.6 or higher installed. Once you have Python installed, you can install the required libraries for this project using the following command:

```pip install -r requirements.txt```

## Usage
You can use the following code to scrape the reel:

```python
from instagram_reel_downloader import InstagramReel

reel = InstagramReel(reel_url)

source_url = reel.source_url
```

## Save the reel to file.
```python
reel.save(filename='reels/video.mp4')
```

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
