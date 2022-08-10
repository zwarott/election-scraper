"""
ProjectEngeto_03.py: The third project to Engeto Online Python Academy

Author: Tomáš Zvardoň
Email: zvardont@seznam.cz
Discord: Tomáš Z.#3385
"""

from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd
import re


def valid_link(input_link: str) -> bool:
    """
    Check if input link is valid -> if is included in list of LAU1 links. LAU1 = district.

    :param input_link:
        String which represents user's input link.

    :return:
        True -> user's link is valid.
        False -> user's link is not valid.
    """
    # parse HTML of the main link
    parsed_html = bs(get("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ").text, features="html.parser")
    # create list of LAU1 links
    links_lau1 = ["https://volby.cz/pls/ps2017nss/" + link.get("href")
                  for link in parsed_html.find_all(href=re.compile("ps32"))]
    return input_link in links_lau1


def parsed_html_lau1(input_link: str) -> bs:
    """
    Parse html code of input link.

    :param: input_link:
        String which represents user's input link.

    :return:
        Parsed html code.
    """
    return bs(get(input_link).text, features="html.parser")


def mun_code(parsed_html: bs) -> list:
    """
    Generate list of municipality (LAU2) codes from input LAU1 link.

    :param: parsed_html:
        Parsed html code of input link.

    :return:
        List of municipality (LAU2) codes from certain LAU1 link.
    """
    code_elements = parsed_html.find_all('td', {"class": "cislo"})
    return [int(code.find('a').text) for code in code_elements]


def mun_name(parsed_html: bs) -> list:
    """
    Generate list of municipality (LAU2) names from certain parsed
    LAU1 html code.

    :param: parsed_html:
        Parsed html code of input link.

    :return:
        List of municipality (LAU2) names.
    """
    # generate municipality names
    name_elements = parsed_html.find_all('td', {"class": "overflow_name"})
    names_mun = [name.text for name in name_elements]
    return names_mun


def links_lau2(parsed_html: bs) -> list:
    """
    Generate list of LAU2 links from certain parsed LAU1 link.
    LAU2 = municipality.

    :param parsed_html:
        Parsed html code of input link.

    :return:
        List of LAU2 links.
    """
    links = []
    for i in parsed_html.find_all("td", {"class": "cislo"}):
        for x in i.find_all("a"):
            links.append("https://volby.cz/pls/ps2017nss/" + x.get("href"))
    return links


def reg_voters(url_lau2: list) -> list:
    """
    Generate list of registered voters for all municipalities in certain district.

    :param: url_lau2:
        List of LAU2 links.

    :return:
        List of registered voters for all municipalities in certain district.
    """
    voters_count = []
    for x in url_lau2:
        soup = bs(get(x).text, features="html.parser")
        voters_elements = soup.find_all('td', headers='sa2')

        # eliminate space between
        for voters in voters_elements:
            x = voters.text.replace(u'\xa0', u'')
            voters_count.append(x)
    return voters_count


def sub_envelopes(url_lau2: list) -> list:
    """
    Generate list of issued envelopes for all municipalities in certain district.

    :param: url_lau2:
        List of LAU2 links.

    :return:
        List of issued envelopes for all municipalities in certain district.
    """
    envelopes_count = []
    for x in url_lau2:
        result = get(x)
        soup = bs(result.text, features="html.parser")
        envelopes_elements = soup.find_all('td', headers='sa3')

        for envelopes in envelopes_elements:
            x = envelopes.text.replace(u'\xa0', u'')
            envelopes_count.append(x)
    return envelopes_count


def valid_votes(url_lau2: list) -> list:
    """
    Generate list of valid votes for all municipalities in certain district.

    :param: url_lau2:
        List of LAU2 links.

    :return:
        List of valid votes for all municipalities in certain district.
    """
    valid_votes_count = []
    for x in url_lau2:
        result = get(x)
        soup = bs(result.text, features="html.parser")
        valid_votes_elements = soup.find_all('td', headers='sa6')

        for votes in valid_votes_elements:
            x = votes.text.replace(u'\xa0', u'')
            valid_votes_count.append(x)
    return valid_votes_count


def party_names() -> list:
    """
    Generate list of available electoral party names for each municipality in certain district.

    :return:
        List of available electoral party names for each municipality in certain district.
    """
    parties_link = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=529303&xvyber=2101"
    split_html_parties = bs(get(parties_link).text, features="html.parser")
    parties_elements = split_html_parties.find_all('td', class_='overflow_name')
    return [party.text for party in parties_elements]


def party_votes(url_lau2: list) -> list:
    """
    Generate list of votes for each electoral party in all municipalities of certain district.

    :param:m url_lau2:
        List of LAU2 links.

    :return:
        List of votes for each electoral party in all municipalities of certain district.
    """
    party_votes_all = []
    for x in url_lau2:
        result = get(x)
        soup = bs(result.text, features="html.parser")
        party_votes_elements = soup.find_all('td', headers='t1sb3') + soup.find_all('td', headers='t2sb3')

        for votes in party_votes_elements:
            x = votes.text.replace(u'\xa0', u'')
            party_votes_all.append(x)
    return party_votes_all


def main(input_link: str, output_file: str):
    """
    Main function to generate file of election results for municipalities
    in the selected district.

    :param: input_link:
        String which represents user's input link.

    :param: output_file:
        String which represents name of output file. Only *csv file
        format is allowed.

    :return:
        If True -> *csv file with election results for municipalities
        in the selected district.
    """
    answer = parsed_html_lau1(input_link)
    code = mun_code(answer)
    location = mun_name(answer)
    lau2_links = links_lau2(answer)
    registered = reg_voters(lau2_links)
    envelopes = sub_envelopes(lau2_links)
    valid = valid_votes(lau2_links)
    pn = party_names()
    pv = party_votes(lau2_links)
    double_sep = 50 * "="

    while not valid_link(input_link):
        print(double_sep, "Your input link is not valid. Please, try again.", double_sep, sep="\n")
        quit()
    while not output_file.endswith('.csv'):
        print(double_sep, "Please, save output file into *csv.", double_sep, sep="\n")
        quit()

    df = pd.DataFrame({"code": code, "location": location, "registered": registered, "envelopes": envelopes,
                       "valid": valid, pn[0]: pv[0::26], pn[1]: pv[1::26], pn[2]: pv[2::26],
                       pn[3]: pv[3::26], pn[4]: pv[4::26], pn[5]: pv[5::26], pn[6]: pv[6::26],
                       pn[7]: pv[7::26], pn[8]: pv[8::26], pn[9]: pv[9::26], pn[10]: pv[10::26],
                       pn[11]: pv[11::26], pn[12]: pv[12::26], pn[13]: pv[13::26], pn[14]: pv[14::26],
                       pn[15]: pv[15::26], pn[16]: pv[16::26], pn[17]: pv[17::26], pn[18]: pv[18::26],
                       pn[19]: pv[19::26], pn[20]: pv[20::26], pn[21]: pv[21::26], pn[22]: pv[22::26],
                       pn[23]: pv[23::26], pn[24]: pv[24::26], pn[25]: pv[25::26]})
    df.to_csv(output_file, encoding='utf-8')


if __name__ == "__main__":
    main("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101", "lau1_benesov.csv")
