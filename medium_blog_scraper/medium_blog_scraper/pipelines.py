import os
from datetime import datetime
import textwrap
from typing import Any

from transformers import AutoTokenizer
import requests

from itemadapter import ItemAdapter

# Hugging Face API configuration
API_URL: str = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_KEY: str = os.getenv("HF_API_KEY")
HEADERS: dict[str, str] = {"Authorization": f"Bearer {API_KEY}"}

# Initialize the tokenizer for summarization
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")


def limit_to_token_count(text: str, max_tokens: int = 1024) -> str:
    """
    Truncate the input text to a specified number of tokens.
    """
    tokens: list[str] = tokenizer.tokenize(text)

    if len(tokens) > max_tokens:
        truncated_tokens: list[str] = tokens[:max_tokens]
        truncated_text: str = tokenizer.convert_tokens_to_string(truncated_tokens)
        return truncated_text
    return text


def summarize_article(text: str, max_tokens: int = 1024, word_limit_min: int = 50, word_limit_max: int = 150) -> str:
    """
    Summarize the input text using the Hugging Face API.
    """
    truncated_text: str = limit_to_token_count(text, max_tokens)

    payload: dict[str, Any] = {
        "inputs": truncated_text,
        "parameters": {
            "min_length": word_limit_min,
            "max_length": word_limit_max,
        },
    }

    response: requests.Response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0].get("summary_text", text)
    else:
        return textwrap.shorten(text, width=500, placeholder="...")


class DataValidationPipeline:
    """
    Pipeline to validate and transform scraped data.
    """
    def process_item(self, item: dict[str, Any], spider: Any) -> dict[str, Any]:
        """
        Validate and clean the scraped item.
        """
        adapter: ItemAdapter = ItemAdapter(item)

        # Symbol mapping for numerical values
        num_symbols: dict[str, int] = {
            "K": 1_000,
            "M": 1_000_000,
            "B": 1_000_000_000,
            "T": 1_000_000_000_000,
        }

        # Validate claps field
        if adapter.get("claps") is None:
            adapter["claps"] = 0
        elif isinstance(adapter.get("claps"), str) and adapter.get("claps").isdigit():
            adapter["claps"] = int(adapter.get("claps"))
        elif adapter.get("claps")[-1].upper() in num_symbols:
            num_symbol: str = adapter.get("claps")[-1].upper()
            num: float = float(adapter.get("claps")[:-1])
            adapter["claps"] = int(num * num_symbols[num_symbol])

        # Validate comments field
        if adapter.get("comments") is None:
            adapter["comments"] = 0
        elif isinstance(adapter.get("comments"), str) and adapter.get("comments").isdigit():
            adapter["comments"] = int(adapter.get("comments"))
        elif adapter.get("comments")[-1].upper() in num_symbols:
            num_symbol: str = adapter.get("comments")[-1].upper()
            num: float = float(adapter.get("comments")[:-1])
            adapter["comments"] = int(num * num_symbols[num_symbol])

        # Format publish_date field
        if adapter.get("publish_date") is not None:
            try:
                date: datetime = datetime.strptime(adapter.get("publish_date"), "%b %d, %Y")
                adapter["publish_date"] = date.strftime("%Y-%m-%d")
            except ValueError as e:
                print(f"[WARNING] Invalid publish date format: {adapter.get('publish_date')} - {e}")

        # Clean read_length field
        if isinstance(adapter.get("read_length"), str) and adapter.get("read_length").endswith("read"):
            adapter["read_length"] = adapter.get("read_length").removesuffix("read").strip()

        # Check if member-only story
        if isinstance(adapter.get("member_only"), str) and adapter.get("member_only").lower() == "member-only story":
            adapter["member_only"] = "Yes"
        else:
            adapter["member_only"] = "No"

        # Summarize article if summary field is available
        if adapter.get("summary") is not None:
            summary: str = summarize_article("\n".join(adapter.get("summary")))
            adapter["summary"] = summary

        # Apply word wrap to text fields
        wrap_length: int = 80
        for field in ['summary', 'title', 'subtitle']:
            if item[field] is not None and len(item[field]) > wrap_length:
                item[field] = textwrap.wrap(item[field], width=wrap_length)

        spider.logger.info(f"Item processed successfully: {item}")
        return item
