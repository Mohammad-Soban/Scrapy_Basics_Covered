# FROM ZERO TO HERO IN SCRAPY

## INTRODUCTION
Scrapy is a Python framework for large-scale web scraping. It provides a robust set of tools and libraries to extract data from websites efficiently. Scrapy is designed to handle complex scraping tasks, including navigating through multiple pages, handling cookies and sessions, and managing requests and responses.

Unlike requests and BeautifulSoup, Scrapy is
- Faster due to its asynchronous architecture.
- It has built-in support for handling requests, responses, and data extraction.
- It handles large scale scraping very easily.
- It has built-in support for exporting data in various formats like JSON, CSV, and XML.
- It has a built-in mechanism for handling retries, redirects, and user-agent rotation.
- It has a built-in mechanism for handling cookies and sessions.
- It provides pipelines for processing and cleaning the scraped data.

<br>

## INSTALLATION
To install Scrapy, you can use pip, the Python package manager. Open your terminal and run the following command. But it is always recommended to use a virtual environment for your projects. So after creating and activating a virtual environment, run the following command:

```bash
pip install scrapy
```

<br>

## STARTING A NEW PROJECT
To start a new Scrapy project, navigate to the directory where you want to create the project and run the following command by replacing `project_name` with your desired project name:

```bash
scrapy startproject project_name
```

This will create a new directory called `project_name` in your current directory. Now we need to move inside the project directory. To do that run the following command:

```bash
cd project_name
```

On running the above command, you will see a directory structure like this:

```
myproject/
│
├── myproject/          # Main project folder
│   ├── spiders/        # Store spiders here
│   │   ├── __init__.py
│   │   └── example.py  # Example spider
│   ├── __init__.py
│   ├── settings.py     # Configurations
│   ├── pipelines.py    # Data cleaning/storage
│   ├── middlewares.py  # Custom request handling
│   └── items.py        # Data structure
│
└── scrapy.cfg
```

<br>

## CREATING OUR FIRST SPIDER
### What is a spider?
- A spider is nothing but a class that defines how a certain site (or a group of sites) will be scraped, including how to perform the crawl (i.e., follow links) and how to extract structured data from their pages (i.e., what data to extract and how to extract it).

### Creating a Spider
- Any kinds of spider (basically a scrapper and a crawler) are created inside the spiders directory. To create a spider, navigate to the spiders directory and create a new Python file. You can name the file anything you want, but it is recommended to use a name that describes the purpose of the spider. For example, if you are creating a spider to scrape quotes from a website, you can name the file `quotes_spider.py`.

- For creating a spider, we can run the following command inside the parent directory of the spiders directory, For our case the first myproject folder will be the parent directory.

```bash
scrapy genspider spider_name domain_name
```

- Here, `spider_name` is the name of the spider you want to create, and `domain_name` is the domain name of the website you want to scrape. For example, if you want to create a spider to scrape quotes from `quotes.toscrape.com`, you can run the following command:

```bash
scrapy genspider quotes quotes.toscrape.com
```

This command will create a new file called `quotes.py` in the `spiders` directory with a basic spider template. You can then edit this file to implement your scraping logic. Start by creating a function called `start_requests` that has all the request URLs and a callback function to handle the response. Then create a `parse` function to extract the data from the response. All the cookies, sessions and other things that are required to handle requests are sent in the start_requests function.

The callback function, generally named `parse`, is where you define how to process the response from the requests made in `start_requests`. This function is responsible for extracting the data you want from the web pages and can also generate additional requests if needed.

The `parse` function takes a single argument, which is the response object returned by Scrapy after making a request. The response.text is the entire HTML content of the page where in we can make selectors to extract the required data.

Here is a simple example of a spider that scrapes quotes from `quotes.toscrape.com`:


```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.text)
```

- In the above code, we have created a spider named `QuotesSpider` that scrapes quotes from `quotes.toscrape.com`. The `start_requests` function sends a request to the first page of the website and the `parse` function is called which prints the HTML content of the page.

## Running the Spider

- To run the spider, navigate to the parent directory of the spiders directory (the first myproject folder) and run the following command:

```bash
scrapy crawl quotes
```

- To get the output in a file, you can use the `-o` option followed by the desired file name and format. For example, to save the output in a JSON file named `quotes.json`, you can run the following command:

```bash
scrapy crawl quotes -o quotes.json
```

- This will run the `quotes` spider and save the output in a file named `quotes.json` in the current directory. You can also use other formats like CSV or XML by changing the file extension accordingly (e.g., `quotes.csv` or `quotes.xml`).

- But for the above spider, we are not extracting any data yet, hence the output file will be empty. To extract data, we need to use selectors to select the required data from the HTML content.


## Extracting The Required Data
Now suppose we need to get all the tags, quotes and their corresponding authors from this simple website, then we need selectors to select the required data from the HTML content. We can use CSS selectors like the class/id selectors or even we can use XPath selectors to select the required data. 

We will try to use different selectors to extract the required data and then send it to `output.csv`, `output.json` or `output.xml` Here is the updated code:

```python
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')
        first_quote = quotes[0]

        quote_text = first_quote.css('span.text::text').get()
        author = first_quote.css('small.author::text').get()
        tags = first_quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()

        yield {
            'quote': quote_text,
            'author': author,
            'tags': tags
        }
```

On running the above spider, we can see the output in the desired file. We can also extract all the quotes from the page by iterating through the `quotes` list. For that we just need to use a loop to iterate the quotes list and catch all the titles, authors and tags in separate lists and then finally yield the data. It is shown in the file `quotes_first_page.py` inside the spiders directory.


## Working with Multiple Pages

To scrape data from multiple pages, we need to identify the link to the next page and send a request to that link in the `parse` function. We can use CSS or XPath selectors to select the link to the next page. Then we can send a request to that link and call the `parse` function again. Here is an example of how to do this:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_all_pages"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            quote_text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()

            yield {
                'quote': quote_text,
                'author': author,
                'tags': ", ".join(tags)
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
```

### The importance Of Yield (Glance Through)
In Python, the `yield` keyword is used in a function to make it a generator. A generator is a special type of iterator that allows you to iterate over a sequence of values without having to store the entire sequence in memory at once. When a function contains the `yield` keyword, it will return a generator object when called, instead of executing the function and returning a single value.

So for our case when we use `yield` in the `parse` function, it allows us to generate and return multiple items (quotes, authors, tags) one at a time, instead of returning a single item or a list of items. This is particularly useful when scraping data from web pages, as it allows us to process and store each item as it is extracted, rather than waiting until all items have been extracted before returning them.

Hence we can store the output in a file without worrying about the memory constraints. This is especially important when scraping large amounts of data, as it allows us to avoid running out of memory or crashing the program.

This covers the basics of Scrapy. But the data scraped might be messy and definitely need some cleaning. So for that the pipelines may need some pre-processing. Also, the code can get repetitive and lengthy. So we will try to find the solutions for that in the next sections.

## Using The Item Loader

### What are Items in Scrapy?
Items in Scrapy are simple containers used to collect and structure the data scraped from web pages. They are similar to Python dictionaries but provide a more structured way to define and validate the data you want to scrape.

### Defining Items
To define an item, you need to create a class that inherits from `scrapy.Item` and define the fields you want to scrape as class attributes using `scrapy.Field()`. For example, if you want to scrape quotes, authors, and tags, you can define an item like this:

```python
import scrapy

class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```
This code can be placed in the items.py file inside the folder where spiders directory is present.

### What are item Loaders?
Item Loaders in Scrapy are a convenient way to populate items with data scraped from web pages. They provide a way to apply input and output processors to the data, allowing you to clean and format the data as it is being loaded into the item. In simple terms Item loaders are helper classes that make it easier to populate items with data scraped from web pages.

- They collect data from the response using selectors (CSS or XPath).
- They help in cleaning and transforming of the data 
- They apply input and output processors

### Using Item Loaders
To use an Item Loader, you need to import the `ItemLoader` class from `scrapy.loader` and create an instance of it, passing in the item class you defined earlier. You can then use the `add_css`, `add_xpath`, or `add_value` methods to populate the fields of the item with data scraped from the web page. Here is an example of how to use an Item Loader to populate a `QuoteItem`:

```python
import scrapy
from scrapy.loader import ItemLoader
from myproject.items import QuoteItem  

class QuotesSpider(scrapy.Spider):
    name = "quotes_with_item_loader"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css('quote', 'span.text::text')
            loader.add_css('author', 'small.author::text')
            loader.add_xpath('tags', './/div[@class="tags"]/a[@class="tag"]/text()')

            yield loader.load_item()
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
```

- In the above code, the only change is that we are using an Item Loader to populate the `QuoteItem` instead of manually creating a dictionary. The `add_css` and `add_xpath` methods are used to extract data from the response using CSS and XPath selectors, respectively. Finally, the `load_item` method is called to return the populated item.

### Benefits of Using Item Loaders
- Cleaner Code: Item Loaders help in keeping the code clean and organized by separating the data extraction logic from the item definition.
- Data Cleaning: Item Loaders allow you to apply input and output processors to clean and format the data as it is being loaded into the item.

### How to Apply Cleaning And Transformations

`Scrapy.loader` has a subclass named `processors` which has a lot of methods like TakeFirst, MapCompose, Join etc which can be used inside the spiders for different purposes. Like for example when we scraped the data lastly, we got lists and multiple quotes inside the text of the quote, so we try to clean that here

Here is the code for the same

```python

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from myproject.items import QuoteItem

def clean_quote(text):
    return text.replace('“', '').replace('”', '').strip()

def make_tags_in_string(tags):
    return ", ".join(tags)

class QuotesSpider(scrapy.Spider):
    name = "quotes_with_item_loader_and_processors"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/page/1/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.default_output_processor = TakeFirst()

            loader.add_css('quote', 'span.text::text', MapCompose(clean_quote))
            loader.add_css('author', 'small.author::text')
            loader.add_xpath('tags', './/div[@class="tags"]/a[@class="tag"]/text()', MapCompose(str.strip), Join(", "))

            yield loader.load_item()

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
```

- `TakeFirst()`: This processor takes the first non-null/non-empty value from the list of values. It is useful when you expect only one value for a field and want to ignore any additional values.

- `MapCompose()`: This processor applies a series of functions to each value in the list. It is useful for cleaning and transforming data. In the above code, we used `MapCompose(clean_quote)` to clean the quote text by removing unwanted characters and whitespace.

- `Join()`: This processor joins a list of strings into a single string using a specified separator. In the above code, we used `Join(", ")` to join the list of tags into a single string separated by commas.


## The Core Modules Of Scrapy
Scrapy organizes its workflow around three core modules that turn raw, unstructured web content into structured data you can use. These are:

1. **Spiders**: The components responsible for defining how a website should be scraped. They contain the logic for navigating the site and extracting the desired data. It includes. The spiders specifies the name, allowed and denied domains, start URLs, and the parsing methods to extract data from the responses.

2. **Item Pipelines**: The components that process the data extracted by the spiders. They can be used for cleaning, validating, and storing the data in a database or file. Pipelines are classes that define methods to process the items scraped by the spiders. They can perform tasks such as cleaning, validating, and storing the data.

3. **Middlewares**: These components act as a request/response interceptor between Scrapy’s engine and the target website. They are used to modify requests and responses, handle retries, manage cookies, and implement custom behaviors like user-agent rotation or proxy usage. Thus Middlewares give fine-grained control over the request and response processing.


## Scrapy Item Pipelines
### What are Pipelines in Scrapy?
Pipelines are mechanisms to process the data once we have scraped or extracted the data using spiders. They can be used for various purposes such as cleaning the data, validating the data, storing the data in a database or a file, etc.

### How To Create A Pipeline
To create a pipeline, you need to create a class that defines the methods for processing the items. The class should be defined in the `pipelines.py` file inside the folder where the spiders directory is present. Here is an example of a simple pipeline that cleans the data by removing any leading or trailing whitespace from the fields:

Here is the code for `pipelines.py` file:

```python
from itemadapter import ItemAdapter

class CleanDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean quote
        if adapter.get('quote'):
            adapter['quote'] = adapter['quote'].strip()

        # Clean author
        if adapter.get('author'):
            adapter['author'] = adapter['author'].strip()

        # Normalize & clean tags so we never iterate over characters
        if 'tags' in adapter and adapter['tags'] is not None:
            tags_val = adapter['tags']

            cleaned_tags = []
            if isinstance(tags_val, str):
                # If a single string (possibly joined), split on comma if present; otherwise keep single tag
                parts = [p.strip() for p in tags_val.split(',')] if ',' in tags_val else [tags_val.strip()]
                cleaned_tags = [p for p in parts if p]
            elif isinstance(tags_val, (list, tuple)):
                cleaned_tags = [str(t).strip() for t in tags_val if str(t).strip()]
            else:
                # Fallback: coerce to single-element list
                one = str(tags_val).strip()
                cleaned_tags = [one] if one else []

            adapter['tags'] = cleaned_tags

        return item


class SaveToCsvPipeline:
    def open_spider(self, spider):
        self.file = open('outputs/output.csv', 'w', encoding='utf-8')
        self.file.write('quote,author,tags\n')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        quote = adapter.get('quote', '')
        author = adapter.get('author', '')
        tags = adapter.get('tags', [])

        # Ensure tags are written as comma-separated words
        if isinstance(tags, (list, tuple)):
            tags_str = ", ".join(tags)
        else:
            tags_str = str(tags).strip()

        line = f'"{quote}","{author}","{tags_str}"\n'
        self.file.write(line)

        return item
```

The rest of the code for `items.py` and `spiders/quotes_with_item_loader_and_processors.py` remains the same as before.

### Activating The Pipeline
To activate the pipeline, you need to add it to the `ITEM_PIPELINES` setting in the `settings.py` file inside the folder where the spiders directory is present. Here is an example of how to activate the `CleanDataPipeline` and `SaveToCsvPipeline`:

```python
ITEM_PIPELINES = {
    'myproject.pipelines.CleanDataPipeline': 300,
    'myproject.pipelines.SaveToCsvPipeline': 400,
}
```

- The keys in the `ITEM_PIPELINES` dictionary are the paths to the pipeline classes, and the values are the order in which the pipelines will be executed. Lower values are executed first. In this example, the `CleanDataPipeline` will be executed before the `SaveToCsvPipeline`.

### Running The Spider With Pipelines
To run the spider with the pipelines activated, you can use the same command as before:

```bash
scrapy crawl quotes_with_item_loader_and_processors
```

This will run the `quotes_with_item_loader_and_processors` spider and process the items through the activated pipelines. The cleaned data will be saved to a file named `output.csv` in the current directory.


### A Brief Summary Of What Has Been Discussed Recently
- **Item** : A simple container to collect and structure the data scraped from web pages.

- **Item Loader** : Basically a Data cleaner at the spider level. 

- **Spider** : The component that defines how a website should be scraped.

- **Pipeline** : The component that processes the data extracted by the spiders.


### Trying To Create A Pipeline With Item Loaders And Processors And Storing The Result To Sqlite Database.

- We first define how the data should be stored and hence we start with the `items.py` file

1. Code For `items.py` file
```python
import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def strip_quotes(s: str) -> str:
    # Example: “The truth…” -> The truth…
    return s.strip("“”\"' \t\r\n ")

class QuoteItem(scrapy.Item):
    text = scrapy.Field(
        input_processor=MapCompose(str.strip, strip_quotes),
        output_processor=TakeFirst(),
    )
    author = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    # keep tags as a list; switch to Join if you want a single string
    tags = scrapy.Field(
        input_processor=MapCompose(str.strip),
    )
```

The cleaning done here is in the `items.py` file while scraping of the data we can use the item loaders and processors to clean the data at the spider level itself. 

Here is the code for the spider file `quotes_items_processors.py` inside the spiders directory.

```python
import scrapy
from scrapy.loader import ItemLoader
from ..items import QuoteItem

class QuotesLoaderSpider(scrapy.Spider):
    name = "quotes_loader"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            loader = ItemLoader(item=QuoteItem(), selector=quote)

            loader.add_css("text", "span.text::text")
            loader.add_css("author", "small.author::text")
            loader.add_css("tags", "div.tags a.tag::text")

            yield loader.load_item()

        # pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

- Finally we create a pipeline to store the data in a CSV file. Here is the code for the `pipelines.py` file

```python
from itemadapter import ItemAdapter
import sqlite3

class SaveToSqlitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("quotes.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                text TEXT,
                author TEXT,
                tags TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        text = adapter.get('text', '')
        author = adapter.get('author', '')
        tags = adapter.get('tags', [])
        tags_str = ", ".join(tags) if isinstance(tags, (list, tuple)) else str(tags).strip()

        self.cursor.execute('''
            INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)
        ''', (text, author, tags_str))
        self.connection.commit()
        return item
```

- To activate the pipeline, you need to add it to the `ITEM_PIPELINES` setting in the `settings.py` file inside the folder where the spiders directory is present. Here is an example of how to activate the `SaveToSqlitePipeline`:

```python
ITEM_PIPELINES = {
    'your_project_name.pipelines.SaveToSqlitePipeline': 300,
}

# Replace 'your_project_name' with the actual name of your Scrapy project
```

Finally to run the spider, you can use the same command as before:

```bash
scrapy crawl quotes_loader
```

This will run the `quotes_loader` spider and process the items through the activated pipeline. The cleaned data will be saved to a SQLite database named `quotes.db` in the current directory.


## MIDDLEWARES IN SCRAPY
### What are Middlewares in Scrapy?
Middlewares in Scrapy are hooks into the request/response processing. They are used to modify requests and responses, handle retries, manage cookies, and implement custom behaviors like user-agent rotation or proxy usage. Middlewares give fine-grained control over the request and response processing.

### Types of Middlewares
There are two types of middlewares in Scrapy:
1. **Spider Middlewares**: These middlewares are used to process the requests and responses that are sent to and received from the spiders. They can be used to modify the requests before they are sent to the spiders and to modify the responses before they are sent back to the engine. The methods that exist here are as follows:
    - `process_spider_input`: For processing responses before they reach the spider.
    - `process_spider_output`: For processing the results returned by the spider.
    - `process_spider_exception`: For handling exceptions raised in the spider or in `process_spider_input`.
    - `process_start_requests`: For processing the start requests of the spider.

2. **Downloader Middlewares**: These middlewares are used to process the requests and responses that are sent to and received from the downloader. They can be used to modify the requests before they are sent to the downloader and to modify the responses before they are sent back to the engine.
The methods that exist here are as follows:
    - `process_request`: For processing requests before they are sent to the downloader.
    - `process_response`: For processing responses before they are sent back to the engine.
    - `process_exception`: For handling exceptions raised during the download process.

The code of middlewares should be placed inside the middlewares.py file inside the folder where the spiders directory is present.

### Creating a Middleware
Suppose we want to create a middleware that rotates the user-agent for each request. Here is an example of how to do this:

```python
import random

class RotateUserAgentMiddleware:
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agent

        return None
```

### Activating the Middleware
To activate the middleware, you need to add it to the `DOWNLOADER_MIDDLEWARES` setting in the `settings.py` file inside the folder where the spiders directory is present. Here is an example of how to activate the `RotateUserAgentMiddleware`:

```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.RotateUserAgentMiddleware': 543,
}
```

- The keys in the `DOWNLOADER_MIDDLEWARES` dictionary are the paths to the middleware classes, and the values are the order in which the middlewares will be executed. Lower values are executed first. In this example, the `RotateUserAgentMiddleware` will be executed with a priority of 543.

### Running the Spider With Middleware
To run the spider with the middleware activated, you can use the same command as before:
```bash
scrapy crawl quotes_loader
```

Apart from this, there are many middlewares available in Scrapy that can be used for purposes like handling retries, managing cookies, etc. You can also create your own custom middlewares to implement specific behaviors as per your requirements.


### Using Logging In Scrapy

Logging is an essential part of any application, and Scrapy provides a built-in logging mechanism that allows you to log messages at different levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). You can use logging to track the progress of your spider, debug issues, and monitor the performance of your scraping tasks.

We can directly use the logger provided by Scrapy in our spiders, pipelines, and middlewares. Here is an example of how to use logging in a spider:

```python
logger.info("This is an info message")
```

**NOTE**: This marks the end of the concepts of Scrapy. Always try to learn new things and keep exploring. Happy Scraping!

© 2025 | Mohammad Soban Shaikh | Please use this repository for educational purposes only.