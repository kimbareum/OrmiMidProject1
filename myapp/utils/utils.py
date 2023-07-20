def get_banner(main="Our Blog", sub="Python, Django, JavaScript & Life", text=''):
    banner = {
        "main": main,
        "sub": sub,
        "text": text,
    }
    return banner


def user_check(user1, user2):
    if user1 == user2:
        return True
    return False