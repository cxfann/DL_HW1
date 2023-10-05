def to_unicode_escape(text):
    return ''.join(['%u{:04X}'.format(ord(char)) for char in text])

text = "区间"
unicode_encoded = to_unicode_escape(text)
print(unicode_encoded)