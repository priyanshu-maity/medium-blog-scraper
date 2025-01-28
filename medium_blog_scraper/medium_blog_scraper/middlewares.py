from random import choice, randint

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; ARM64; rv:91.0) Gecko/20100101 Firefox/91.0",
]

PLATFORMS = [
    "Windows NT 10.0; Win64; x64",
    "Macintosh; Intel Mac OS X 10_15_7",
    "X11; Linux x86_64",
    "Windows NT 11.0; Win64; x64",
    "Macintosh; Intel Mac OS X 12_6",
    "X11; Ubuntu; Linux x86_64",
    "iPhone; CPU iPhone OS 15_0 like Mac OS X",
    "Linux; Android 11; SM-G998B",
    "Windows NT 10.0; ARM64",
]


def generate_headers():
    """Generate random headers for requests."""
    user_agent = choice(USER_AGENTS)
    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": str(randint(0, 1)),  # Randomly enable/disable Do Not Track
    }


class RandomHeadersMiddleware:
    def process_request(self, request, spider):
        """Assign random headers to each request."""
        headers = generate_headers()
        request.headers.update(headers)
        spider.logger.info(f"Assigned headers: {headers}")
