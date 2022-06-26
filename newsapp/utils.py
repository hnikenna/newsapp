
def breadcrumb(text: str, num: int):
    if len(text) > num:
        return text[:num].rstrip(' ') + '...'
    else:
        return text
