def to_unicode_escape(text):
    """
    Converts a given text to Unicode escape sequences for Chinese characters (CJK Unified Ideographs).

    Args:
        text (str): The input text to convert.

    Returns:
        str: The input text with Chinese characters converted to Unicode escape sequences.

    Example:
        >>> to_unicode_escape('你好')
        '%u4F60%u597D'
    """
    return ''.join(['%u{:04X}'.format(ord(char)) if '\u4e00' <= char <= '\u9fff' else char for char in text])

def txt_to_unicode(text):
    """
    Converts a text containing Chinese characters to Unicode escape sequences.

    Args:
        text (str): The input text to convert.

    Returns:
        str: The input text with Chinese characters converted to Unicode escape sequences.

    Example:
        >>> txt_to_unicode('你好')
        '%u4F60%u597D'
    """
    unicode_encoded = to_unicode_escape(text)
    return unicode_encoded