

def extract_avatar_url(full_avatar_url: str):
    print(f'\nExtracting avatar url: {full_avatar_url}...')
    try:
        the_url = full_avatar_url.split('/static')[1]
        print(f'Extracted the avatar url: {the_url}...')
        return the_url
    except Exception as ect:
        print(f'Error to extract url [{full_avatar_url}]:', ect)
        return 'default_user.jpg'
