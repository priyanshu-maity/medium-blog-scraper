<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/priyanshu-maity/medium-blog-scraper">
    <img src="logo.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Medium Blog Scraper</h3>

  <p align="center">
    An advanced web scraper for Medium.com built with Scrapy and Playwright
    <br />
    <br />
    <br />
    <a href="https://github.com/priyanshu-maity/medium-blog-scraper/issues">Report Bug</a>
    ·
    <a href="https://github.com/priyanshu-maity/medium-blog-scraper/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The Medium Blog Scraper is a sophisticated web scraping solution designed to extract articles and their metadata from Medium.com. It combines the power of Scrapy's scraping framework with Playwright's browser automation capabilities to handle dynamic content and JavaScript-rendered pages effectively.

Key Highlights:
* Intelligent article search and extraction based on keywords
* Advanced retry mechanisms and error handling
* Automatic article summarization using BART model
* Comprehensive data validation and cleaning pipeline

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.org]][Python-url]
* [![Scrapy][Scrapy.org]][Scrapy-url]
* [![Playwright][Playwright.dev]][Playwright-url]
* [![HuggingFace][HuggingFace.co]][HuggingFace-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.8 or higher
* pip
```sh
python -m pip install --upgrade pip
```

### Installation

1. Get a free API Key at [https://huggingface.co](https://huggingface.co)
2. Clone the repo
   ```sh
   git clone https://github.com/priyanshu-maity/medium-blog-scraper.git
   ```
3. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your API key
   ```sh
   HF_API_KEY='your_api_key'
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. Basic usage with default settings:
```python
python run.py
```

2. Custom keyword search:
```python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from medium_blog_scraper.spiders.blog_scraper_spider import BlogScraperSpider

process = CrawlerProcess(get_project_settings())
process.crawl(
    BlogScraperSpider,
    keywords={
        "Artificial Intelligence": 10,
        "Machine Learning": 15
    }
)
process.start()
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

- [x] Keyword-based article search
- [x] Dynamic content handling
- [x] Article summarization
- [x] Data validation pipeline
- [x] Rate limiting and retry mechanisms
- [x] Random user agent rotation

See the [open issues](https://github.com/priyanshu-maity/medium-blog-scraper/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Priyanshu Maity: [@linkedin](https://www.linkedin.com/in/priyanshu-maity-34a92230a/) | priyanshu.maity2006@gmail.com

Project Link: [https://github.com/priyanshu-maity/medium-blog-scraper](https://github.com/priyanshu-maity/medium-blog-scraper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Scrapy Documentation](https://docs.scrapy.org/)
* [Playwright Python API](https://playwright.dev/python/)
* [Hugging Face Transformers](https://huggingface.co/transformers/)
* [Medium.com](https://medium.com)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/priyanshu-maity/medium-blog-scraper.svg?style=for-the-badge
[contributors-url]: https://github.com/priyanshu-maity/medium-blog-scraper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/priyanshu-maity/medium-blog-scraper.svg?style=for-the-badge
[forks-url]: https://github.com/priyanshu-maity/medium-blog-scraper/network/members
[stars-shield]: https://img.shields.io/github/stars/priyanshu-maity/medium-blog-scraper.svg?style=for-the-badge
[stars-url]: https://github.com/priyanshu-maity/medium-blog-scraper/stargazers
[issues-shield]: https://img.shields.io/github/issues/priyanshu-maity/medium-blog-scraper.svg?style=for-the-badge
[issues-url]: https://github.com/priyanshu-maity/medium-blog-scraper/issues
[license-shield]: https://img.shields.io/github/license/priyanshu-maity/medium-blog-scraper.svg?style=for-the-badge
[license-url]: https://github.com/priyanshu-maity/medium-blog-scraper/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/priyanshu-maity
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[Scrapy.org]: https://img.shields.io/badge/Scrapy-60A839?style=for-the-badge&logo=scrapy&logoColor=white
[Scrapy-url]: https://scrapy.org/
[Playwright.dev]: https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white
[Playwright-url]: https://playwright.dev/
[HuggingFace.co]: https://img.shields.io/badge/HuggingFace-FF9D00?style=for-the-badge&logo=huggingface&logoColor=white
[HuggingFace-url]: https://huggingface.co/
