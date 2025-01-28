import sys
import asyncio
from urllib.parse import urljoin
from typing import Any, Self, Optional, Iterable, Generator

import scrapy
from scrapy.http import Response
from playwright.async_api import Page, TimeoutError
from scrapy_playwright.page import PageMethod
from medium_blog_scraper.items import MediumBlogItems


class BlogScraperSpider(scrapy.Spider):
    name: str = "blog_scraper"
    allowed_domains: list[str] = ['medium.com']
    keywords: dict[str, int] = {"Scrapy": 5}

    def __init__(self: Self, keywords: Optional[dict[str, int]] = None, *args: Any, **kwargs: Any) -> None:
        super(BlogScraperSpider, self).__init__(*args, **kwargs)

        if keywords:
            self.keywords = keywords

    def start_requests(self: Self) -> Iterable[scrapy.Request]:
        """
        Generate initial requests for each keyword with Playwright enabled.
        """
        for keyword, num_items in self.keywords.items():
            self.logger.info(f"Starting request for keyword: {keyword}")
            yield scrapy.Request(
                url=f"https://medium.com/search?q={keyword}",
                meta={
                    'keyword': keyword,
                    'num_items': num_items,
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector",
                                   "xpath=/html/body/div[1]/div/div[3]/div[2]/div/main/div/div/div[2]/div")
                    ],
                },
                callback=self.parse
            )

    async def parse(self: Self, response: Response, **kwargs: Any) -> Generator[scrapy.Request, None, None]:
        """
        Parse search results page and yield article requests.
        """
        page: Page = response.meta['playwright_page']
        keyword: str = response.meta['keyword']
        num_items: int = response.meta['num_items']

        self.logger.info(f"Parsing search results for keyword: {keyword}")

        try:
            counter: int = 0
            scraped: int = 0
            max_global_retries: int = 3
            global_retries: int = max_global_retries

            while scraped < num_items:
                if global_retries == 0:
                    self.logger.info(f"No more articles found after {max_global_retries} retries. Exiting loop.")
                    break

                # Locate the article element based on the counter
                article_xpath: str = f"/html/body/div[1]/div/div[3]/div[2]/div/main/div/div/div[2]/div/div[{counter + 1}]"
                article = await page.query_selector(f"xpath={article_xpath}")

                if not article:
                    self.logger.info(f"Article {counter + 1} not found. Attempting to load more articles.")
                    retries: int = 3
                    flag: bool = False

                    while retries > 0:
                        try:
                            self.logger.info(f"Clicking 'Show more' button (Retry {4 - retries}/3)...")
                            await page.click(f"xpath=//button[text()='Show more']")
                            await page.wait_for_selector(f"xpath={article_xpath}", timeout=3000)
                            flag = True
                            break
                        except TimeoutError:
                            self.logger.warning(f"Timeout while waiting for article {counter + 1}. Retries left: {retries - 1}")
                            retries -= 1
                        except Exception as e:
                            self.logger.error(f"Error clicking 'Show more': {e}")
                            retries -= 1

                    if not flag:
                        global_retries -= 1
                        self.logger.info(f"No articles found after retrying. Remaining retries: {global_retries}/{max_global_retries}.")
                    counter += 1
                    continue

                # Reset retries upon finding an article
                global_retries = max_global_retries

                # Extract the link to the article
                link_element = await article.query_selector("xpath=.//a[h2]")
                if not link_element:
                    self.logger.info(f"No link element found in article {counter + 1}. Skipping...")
                    counter += 1
                    continue

                link: Optional[str] = await link_element.get_attribute("href")
                if link:
                    link = urljoin("https://medium.com", link)
                    self.logger.info(f"Found article link: {link}")
                    yield scrapy.Request(
                        url=link,
                        meta={
                            'keyword': keyword,
                            'playwright': True,
                            'playwright_include_page': True,
                        },
                        callback=self.parse_article
                    )
                    scraped += 1
                counter += 1

        except Exception as e:
            self.logger.error(f"Error parsing search results: {e}")
        finally:
            self.logger.info("Closing the Playwright page...")
            await page.close()

    async def parse_article(self: Self, response: Response) -> Generator[scrapy.Item, None, None]:
        """
        Parse individual article page and extract details.
        """
        page: Page = response.meta['playwright_page']
        items: MediumBlogItems = MediumBlogItems()
        items['link'] = response.url
        items['search_term'] = response.meta['keyword']

        self.logger.info(f"Parsing article: {response.url}")

        await self.check_click_button(
            page=page,
            button_xpath="/html/body/div[1]/div/div[3]/div[2]/div[4]/div/div/div/div[1]/div[1]/div/button"
        )

        await page.wait_for_selector("xpath=//p[contains(@class, 'pw-post-body-paragraph')]")

        items = await self.extract_items(response, page, items)
        if items:
            self.logger.info(f"Extracted items for article: {response.url}")
            yield items

        await page.close()

    async def extract_items(self: Self, response: Response, page: Page, items: MediumBlogItems) -> MediumBlogItems:
        """
        Extract article details using both Scrapy and Playwright.
        """
        self.logger.info(f"Extracting details from article: {response.url}")

        xpath_dict: dict[str, str] = {
            "title": "//h1[@data-testid='storyTitle']",
            "subtitle": "//h2[contains(@class, 'pw-subtitle-paragraph')]",
            "summary": "//p[contains(@class, 'pw-post-body-paragraph')]",
            "tags": "//a[contains(@href, '/tag/')]/div",
            "author": "//a[@data-testid='authorName']",
            "publication": "//a[@data-testid='publicationName']/p",
            "claps": "//div[contains(@class, 'pw-multi-vote-count')]/div/div/p/button",
            "comments": "//span[contains(@class, 'pw-responses-count')]",
            "publish_date": "//span[@data-testid='storyPublishDate']",
            "read_length": "//span[@data-testid='storyReadTime']",
            "member_only": "//div[contains(@class, 'speechify-ignore')]//p[text()='Member-only story']"
        }

        # Extracting items using Scrapy
        for field_name, xpath in xpath_dict.items():
            if field_name in ("tags", "summary"):
                items[field_name] = response.xpath(f"{xpath}/text()").getall()
            else:
                items[field_name] = response.xpath(f"{xpath}/text()").get()

        # Extracting items using Playwright
        async def plw_extract_items(field_name: str, xpath: str) -> None:
            if field_name in ("tags", "summary"):
                items[field_name] = []
                elements = await page.query_selector_all(f"xpath={xpath}")
                for el in elements:
                    if el:
                        items[field_name].append(await el.text_content())
            else:
                element = await page.query_selector(f"xpath={xpath}")
                if element:
                    items[field_name] = await element.text_content()

        tasks = [plw_extract_items(field_name, xpath) for field_name, xpath in xpath_dict.items() if not items[field_name]]
        await asyncio.gather(*tasks)

        return items

    @staticmethod
    async def check_click_button(page: Page, button_xpath: str) -> None:
        """
        Check if a button exists and click it if found.
        """
        try:
            button = await page.query_selector(f"xpath={button_xpath}")
            if button:
                await button.click()
        except TimeoutError:
            pass
