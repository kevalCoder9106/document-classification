from bs4 import BeautifulSoup

page = ''
count = 0

with open('page.txt', 'r') as f:
    for l in f:
        page = page + l

page = BeautifulSoup(page, 'html.parser')

el = page.find_all('a', {'class': 'MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button'})

for e in el:
    count += 1
    print(e.get('href'))

print('\n\nCount: ', count)