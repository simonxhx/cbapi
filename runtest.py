import cbapi
import pandas as pd


def test_cbapi():
    test_ppl = cbapi.get_ppl(name="Simon", types="investor")
    test_orgs = cbapi.get_orgs(name="capital management", types="investor")

    # check that results are pandas dataframes
    assert isinstance(test_ppl, pd.DataFrame)
    assert isinstance(test_orgs, pd.DataFrame)

    print("OK")


if __name__ == "__main__":
    test_cbapi()
