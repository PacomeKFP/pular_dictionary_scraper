"""A collection of utilities to make your life easy with titanscraper"""

def convert_to_csv(data:dict) -> list :
    """conversts a dictionary into a single line of comma separated values"""
    # convert all headers keys into a sigle line string
    headings = ",".join(list(data.keys()))

    # convert the items into string wrapped with double quotes and join all 
    # into a single string
    items = ",".join([f"\"{i[1]}\"" for i in list(data.items())])
    return [headings, items]