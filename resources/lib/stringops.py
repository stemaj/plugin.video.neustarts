def extract_inner_part(content, beginString, endString):
    if isinstance(content, str) and isinstance(beginString, str) and isinstance(endString, str):
        splitt = content.split(beginString)
        if len(splitt) > 1:
            splitt = splitt[1].split(endString)
            if len(splitt) > 1 and isinstance(splitt[0], str):
                return splitt[0]
    return ""
