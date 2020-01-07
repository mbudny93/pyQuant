from src import scrap

def test_scrap_us500():
    result = scrap.scrap_us500()
    print(result)
    assert len(result) >= 500

def test_scrap_dax():
    result = scrap.scrap_dax()
    print(result)
    assert len(result) >= 30

def test_scrap_ftse100():
    result = scrap.scrap_ftse100()
    print(result)
    assert len(result) >= 100

def test_scrap_wig20():
    result = scrap.scrap_wig20()
    print(result)
    assert len(result) >= 20
