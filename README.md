# Crunchbase API
A full-featured API (application programming interface) library for downloading and presenting organization and people data from Crunchbase.

## Usage
### Retrieving organization data:
Optional parameters include:
* Query (Full text search of an Organization's name, aliases (i.e. previous names or "also known as"), and short description)
* Name
* Domain Name
* Locations
* Organization Types
* Page

### Retrieving people data:
Optional parameters include:
* Query (A full-text query of name, title, and company)
* Name
* Locations
* Socials
* Types
* Page

The return type is a Pandas dataframe. Note that if the page number is not specified, then all matches will be returned.

Examples:

    import cbapi
    
    org_search = cbapi.get_orgs(name="capital management", types="investor", page="2")
    ppl_search = cbapi.get_ppl(name="John", locations="New York")

## Installation
Install cbapi using pip:

    pip install git+https://github.com/simonxhx/cbapi.git

### Requirements
* Python
* Pandas
* requests
