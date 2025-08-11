from utils.helpers import extract_manwha_name, sanitize_filename

def test_extract_manwha_name():
    url = "https://dashboard.olympusbiblioteca.com/api/series/isecaikr20-225-arochino13424/chapters?page=1"
    assert extract_manwha_name(url) == "isecaikr20-225-arochino13424"

def test_sanitize_filename():
    assert sanitize_filename("Capítulo: 1/2*3?") == "Capítulo_ 1_2_3_"