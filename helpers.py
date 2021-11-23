

def add_image(beers):
    """Iterate through beers and add generic image if needed."""

    for beer in beers:
        if not beer['image_url']:
            beer.update({'image_url': "/static/generic_beer.png"})
    
    return beers

def get_id_query_string(id_list):
    """Generate id query string"""

    query_string = '?ids='
    for id in id_list:
        query_string += f"{id}|"  
    l = len(query_string)
    return query_string[:l-1] #remove extra "|"

def get_recipe_query_string(recipe_list):
    """Generate recipe query string"""

    query_string = '?'
    for item in recipe_list:
        query_string += f"{item[0]}={item[1]}&"
    l = len(query_string)
    return query_string[:l-1] #remove extra "&"