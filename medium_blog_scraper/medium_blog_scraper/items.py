from scrapy import Field, Item


class MediumBlogItems(Item):
    # Search term used to find the article
    search_term = Field()

    # Metadata about the article
    title = Field()
    subtitle = Field()
    summary = Field()
    tags = Field()
    member_only = Field()

    # Author and publication information
    author = Field()
    publication = Field()

    # Engagement metrics
    claps = Field()
    comments = Field()

    # Time and length
    publish_date = Field()
    read_length = Field()

    # Link to the article
    link = Field()
