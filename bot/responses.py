def handle_response(text: str) -> str:
    text = text.lower()
    if 'hello' in text:
        return 'Hey there!'
    elif 'hey' in text:
        return 'Hello there!'
    return 'I do not understand..'