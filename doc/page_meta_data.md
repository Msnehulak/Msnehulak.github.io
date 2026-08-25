# Page meta data documentation

## from mark down (.md)
 - title: str `title of page`
 - description: str `description of page`
 - slug: str `short name of page` `use only: a-z, 0-9, '-', '_'`
 - lang: ISO 639-1 `language of page`
 - template: str `which template Pelican is going to use`
 - folder: str `use to create deeper sub page` `{{ folder }}/{{ slug }}`
 - js: str `add to page js from` `page: /theme/js/{{ name }}.js` `folder: /theme/static/js/`
 - js_lib: str `add to page js from` `page: /theme/extra/{{ name }}.js` `folder: /theme/static/extra/` **`is use only for code aces`**
 - css: str `add to page css from` `page: /theme/extra/{{ name }}.css` `folder: /theme/static/extra/` **`is use only for code aces`**
 - sitemap_priority: float `level of priority for sitemap` `use 0.0 - 1.0`

 ## form git 
  - date: Unix Timestamp `Preation of page`
  - modified: Unix Timestamp `last modify of page`



