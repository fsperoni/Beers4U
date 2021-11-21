

def add_image(beers):
    """Iterate through beers and add generic image if needed."""

    for beer in beers:
        print("**************************")
        print(beer['image_url'])
        if not beer['image_url']:
            beer.update({'image_url': "/static/generic_beer.png"})
    
    return beers