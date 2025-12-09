from random import randint

class UserInputError(Exception):
    pass

def validate_key(key):
    if len(key) < 5:
        raise UserInputError("Viiteavaimen pitää olla vähintään 5 merkkiä pitkä")

    if len(key) > 100:
        raise UserInputError("Viiteavaimen pituus ei saa ylittää 100 merkkiä")

def validate_ref_type(ref_type):
    types = ["article", "book", "inproceedings"]
    if ref_type not in types:
        raise UserInputError("Valitse oikea viitetyyppi")

def validate_author(author):
    if len(author) > 100:
        raise UserInputError("Tekijän nimen pituus ei saa ylittää 100 merkkiä")

def validate_title(title):
    if len(title) < 5:
        raise UserInputError("Otsikon pituuden tulee olla vähintään 5 merkkiä")

    if len(title) > 100:
        raise UserInputError("Otsikon pituus ei saa ylittää 100 merkkiä")

def validate_year(year):
    try:
        year = int(year)
        if year < 0:
            raise UserInputError("Vuosi ei voi olla negatiivinen luku")
    except:
        raise UserInputError("Vuoden tulee olla numero")

def validate_journal(journal):
    if len(journal) < 5:
        raise UserInputError("Lehden tai konferenssin nimen tulee olla vähintään 5 merkkiä pitkä")

    if len(journal) > 100:
        raise UserInputError("Lehden tai konferenssin nimi ei saa ylittää 100 merkkiä")

def validate_publisher(publisher):
    if len(publisher) < 5:
        raise UserInputError("Kustantajan nimen tulee olla vähintään 5 merkkiä pitkä")

    if len(publisher) > 100:
        raise UserInputError("Kustantajan nimen pituus ei saa ylittää 100 merkkiä")

def validate_book(key, ref_type, author, title, year, journal, publisher, doi=None):
    validate_key(key)
    validate_ref_type(ref_type)
    validate_author(author)
    validate_title(title)
    validate_year(year)
    if journal:
        validate_journal(journal)
    if publisher:
        validate_publisher(publisher)

def get_random_gif():
    return f"gifs/{randint(1,8)}.gif"