from terminaltables import AsciiTable

data = [
    ('something', '21'),
    ("helo", 'world')
]

table = AsciiTable(data)

print(table.table)