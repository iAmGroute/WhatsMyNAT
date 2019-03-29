# Usage:
from SmartTabs import t
print(t('Column 1 Header\t Col2\t Col3'))
print(t('Shorter 1\t Col2\t Col3'))
print(t('Longer message on column 1\t Col2\t Col3'))
print(t('Again shorter 1\t Col2\t Col3'))
print(t('Longer message on column 1\t Col2\t Col3'))
print(t('Something in between\t Col2\t Col3'))
print(t('Something in between v2\t I didn\'t move !\t But now I did'))
print(t('Something in between v10\t shorter\t Now I didn\'t move either'))
print(t('Everything in between\t from now on\t will be aligned'))
print(t('Until you call\t t.reset()'))
t.reset()
print(t('like this,\t see ?'))
print(t('test 1\t test 2'))
print(t('test 10\t test 20'))
print('Use it with unknown length variables like this:')
for url in ['example.com', 'linux.org', 'superlongurl.long.tld.too', 'wikipedia.com', 'notsolongurl.tld', 'github.com', 'git-scm.com']:
    print(t('Sending request to:\t {0}\t and waiting for reply on {1}'.format(url, 123)))
print(t.over('You can also\t avoid modifying the existing layout by calling t.over() instead of t().'))