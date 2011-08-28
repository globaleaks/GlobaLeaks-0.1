response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
    (T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
    (T('Submission'),URL('default','submission')==URL(),URL('default','submission'),[]),
    (T('Tulips'),URL('default','tulip')==URL(),URL('default','tulip'),[]),
]
