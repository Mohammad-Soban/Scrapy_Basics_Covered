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