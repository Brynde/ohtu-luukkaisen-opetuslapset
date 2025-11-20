class UserInputError(Exception):
    pass

def validate_key(key):
    if len(key) < 5:
        raise UserInputError("Key length must be greater than 4")

    if len(key) > 100:
          raise UserInputError("Key length must be smaller than 100")
    
def validate_ref_type(ref_type):
    types = ["article", "book", "inproceedings"]
    if ref_type not in types:
        raise UserInputError("You must choose a valid reference type")

def validate_author(author):
    if len(author) > 100:
          raise UserInputError("Author length must be smaller than 100")

def validate_title(title):
    if len(title) < 5:
        raise UserInputError("Title length must be greater than 4")

    if len(title) > 100:
          raise UserInputError("Title length must be smaller than 100")

def validate_year(year):
    try:
        year = int(year)
        if year < 0:
            raise UserInputError("The year cannot be negative")
    except:
        raise UserInputError("The year must be a number")
    
    
    
def validate_journal(journal):
    if len(journal) < 5:
        raise UserInputError("Journal length must be greater than 4")

    if len(journal) > 100:
          raise UserInputError("Journal length must be smaller than 100")
    
def validate_publisher(publisher):
    if len(publisher) < 5:
        raise UserInputError("Publisher length must be greater than 4")

    if len(publisher) > 100:
          raise UserInputError("Publisher length must be smaller than 100")

def validate_book(key, ref_type, author, title, year, journal, publisher):
    validate_key(key)
    validate_ref_type(ref_type)
    validate_author(author)
    validate_title(title)
    validate_year(year)
    validate_journal(journal)
    validate_publisher(publisher)
