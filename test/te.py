from lxml import html
with open('test/output.html', 'r') as f:
    html_content = f.read()
    print(type(html_content))
tree = html.fromstring(html_content)

# Using CSS Selectors
link_element = tree.cssselect('a[class="re__pagination-icon"]')[0]
link_elements = tree.cssselect('a[class="js__product-link-for-product-id"]')
link = link_element.get('href')

print("Link URL:", link, link_elements)