import json
import requests
import threading
import os
import pandas as pd


def get_orgs(query="", name="", domain="", locations="", types="", page=""):
    rapidapi_key = os.environ.get("CBAPI_KEY")

    def run(p=page):
        url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"

        querystring = {
            "query": query, "name": name, "domain_name": domain, "locations": locations,
            "organization_types": types, "page": p
        }

        headers = {
            'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
            'x-rapidapi-key': rapidapi_key
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response_df = pd.DataFrame(json.loads(response.text))  # response in a pandas dataframe
        return response_df

    summary = run()
    result = pd.DataFrame(list(pd.DataFrame(summary["data"]["items"])["properties"]))

    if not page:  # if page number is not indicated, return all results using multithreading

        def more_orgs(results, idx, p):
            results[idx] = pd.DataFrame(list(pd.DataFrame(run(p)["data"]["items"])["properties"]))

        npages = summary["data"]["paging"]["number_of_pages"]
        threads = [None] * (npages - 1)
        pages = [None] * (npages - 1)
        for i in range(len(threads)):
            threads[i] = threading.Thread(target=more_orgs, args=(pages, i, str(i + 2)))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
            result = result.append(pages[i])

    # set index to organization name
    result.set_index(result["name"], inplace=True)
    return result
