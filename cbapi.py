import json
import requests
import threading
import os
import pandas as pd

RAPIDAPI_KEY = os.environ.get("CBAPI_KEY")


def more_ppl(result, idx, name, query, page, locations, socials, types):
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

    querystring = {
        "name": name, "query": query, "page": page, "locations": locations, "socials": socials, "types": types
    }

    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_df = pd.DataFrame(json.loads(response.text))   # response in a pandas dataframe
    output_df = pd.DataFrame(list(pd.DataFrame(response_df["data"]["items"])["properties"]))
    result[idx] = output_df


def get_ppl(name="", query="", page="", locations="", socials="", types=""):
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

    querystring = {
        "name": name, "query": query, "page": page, "locations": locations, "socials": socials, "types": types
    }

    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_df = pd.DataFrame(json.loads(response.text))   # response in a pandas dataframe
    output_df = pd.DataFrame(list(pd.DataFrame(response_df["data"]["items"])["properties"]))

    if not page:    # if page number is not indicated, return all results using multithreading
        npages = response_df["data"]["paging"]["number_of_pages"]
        threads = [None] * (npages - 1)
        results = [None] * (npages - 1)
        for i in range(len(threads)):
            threads[i] = threading.Thread(target=more_ppl,
                                          args=(results, i, name, query, str(i + 2), locations, socials, types))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
            output_df = output_df.append(results[i])

    # set index to first_name last_name
    output_df.set_index(output_df["first_name"] + " " + output_df["last_name"], inplace=True)
    return output_df


def more_orgs(results, idx, query, name, domain, locations, types, page):
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"

    querystring = {
        "query": query, "name": name, "domain_name": domain, "locations": locations,
        "organization_types": types, "page": page
    }

    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_df = pd.DataFrame(json.loads(response.text))  # response in a pandas dataframe
    output_df = pd.DataFrame(list(pd.DataFrame(response_df["data"]["items"])["properties"]))
    results[idx] = output_df


def get_orgs(query="", name="", domain="", locations="", types="", page=""):
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"

    querystring = {
        "query": query, "name": name, "domain_name": domain, "locations": locations,
        "organization_types": types, "page": page
    }

    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_df = pd.DataFrame(json.loads(response.text))  # response in a pandas dataframe
    output_df = pd.DataFrame(list(pd.DataFrame(response_df["data"]["items"])["properties"]))

    if not page:  # if page number is not indicated, return all results using multithreading
        npages = response_df["data"]["paging"]["number_of_pages"]
        threads = [None] * (npages - 1)
        results = [None] * (npages - 1)
        for i in range(len(threads)):
            threads[i] = threading.Thread(target=more_orgs,
                                          args=(results, i, query, name, domain, locations, types, str(i + 2)))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
            output_df = output_df.append(results[i])

    # set index to organization name
    output_df.set_index(output_df["name"], inplace=True)
    return output_df