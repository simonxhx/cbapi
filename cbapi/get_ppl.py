import json
import requests
import threading
import os
import pandas as pd


def get_ppl(name="", query="", page="", locations="", socials="", types=""):
    rapidapi_key = os.environ.get("CBAPI_KEY")

    def run(p=page):
        url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

        querystring = {
            "name": name, "query": query, "page": p, "locations": locations, "socials": socials, "types": types
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

    if not page:    # if page number is not indicated, return all results using multithreading

        def more_ppl(results, idx, p):
            results[idx] = pd.DataFrame(list(pd.DataFrame(run(p)["data"]["items"])["properties"]))

        npages = summary["data"]["paging"]["number_of_pages"]
        threads = [None] * (npages - 1)
        pages = [None] * (npages - 1)
        for i in range(len(threads)):
            threads[i] = threading.Thread(target=more_ppl, args=(pages, i, str(i + 2)))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
            result = result.append(pages[i])

    # set index to first_name last_name
    result.set_index(result["first_name"] + " " + result["last_name"], inplace=True)
    return result
