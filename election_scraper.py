"""
ProjectEngeto_03.py: The third project to Engeto Online Python Academy

Author: Tomáš Zvardoň
Email: zvardont@seznam.cz
Discord: Tomáš Z.#3385
"""

from sys import argv
import os
import csv
import re
from requests import get
from bs4 import BeautifulSoup as bs


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


def filtered_html(input_link: str):
    """
    Filter parsed html code of input link by <tr> (table row).
    :param: input_link:
        String which represents user's input link.
    :return:
        Filtered parsed html code.
    """
    s = parsed_html_lau1(input_link)
    return s.find_all("tr")


def id_lau2(input_link: str) -> list:
    """
    Generate name and code for each municipality (LAU2) from
    selected district (from input link).
    :param: input_link:
        String which represents user's input link.
    :return:
        Nested lists of each municipality id [code, name] in
        output list.
    """
    muns = filtered_html(input_link)
    muns_id = []
    for mun in muns:
        mun_code = mun.find("td", {"class": "cislo"})
        mun_name = mun.find("td", {"class": "overflow_name"})
        if mun_code:
            muns_id.append([mun_code.text, mun_name.text])
        else:
            continue
    return muns_id


def links_lau2(parsed_html: bs) -> list:
    """
    Generate list of LAU2 links from certain parsed LAU1 link.
    LAU2 = municipality.
    :param parsed_html:
        Parsed html code of input link.
    :return:
        List of LAU2 links.
    """
    links = ["https://volby.cz/pls/ps2017nss/" + x.get("href") for i in parsed_html.find_all("td", {"class": "cislo"})
             for x in i.find_all("a")]
    return links


def elect_lau1(mun_url: list) -> list:
    """
    Generate data of registered voters, issued envelopes and
    valid votes for each municipality (LAU2) from selected
    district.
    :param: mun_url:
        List of LAU2 links.
    :return:
        Nested lists of electoral data for each LAU2 in
        output list.
    """
    elect_muns = []
    for url in mun_url:
        s = parsed_html_lau1(url)
        # filter necessary data only
        v = s.find("table", {"class": "table"})
        # find data using indexing within table data
        voters = v.find_all("td", {"class": "cislo"})[3].text.replace("\xa0", "")
        envelopes = v.find_all("td", {"class": "cislo"})[4].text.replace("\xa0", "")
        valid_votes = v.find_all("td", {"class": "cislo"})[7].text.replace("\xa0", "")
        elect_muns.append([voters, envelopes, valid_votes])
    return elect_muns


def elect_parties(mun_url: list) -> list:
    """
    Generate data of votes for each electoral party in each municipality (LAU2)
    from selected district.
    :param: mun_url:
        List of LAU2 links.
    :return:
        Nested lists of electoral data for each LAU2 in output list.
    """
    p_votes = []
    for url in mun_url:
        s = parsed_html_lau1(url)
        # filter necessary data only
        votes = s.find_all("div", {"class": "t2_470"})
        table_full = []
        table_rows = []
        mun_votes_sum = []
        # operating with table rows
        for vote in votes:
            rows = vote.find_all("tr")
            table_full.extend(rows)
        # find all elements containing specific code associated with the numerical value
        # of the electoral votes
        for mun in table_full:
            row = mun.find_all("td", headers="t1sb3") + mun.find_all("td", headers="t2sb3")
            if row:
                table_rows.append(row)
            else:
                continue
        # get numerical values only and remove the thousand separator
        for row in table_rows:
            mun_votes_sum.append(row[0].text.replace("\xa0", ""))
        p_votes.append(mun_votes_sum)
    return p_votes


def party_names(input_link: str) -> list:
    """
    Generate list of available electoral party names for each municipality in certain district.
    :param: input_link:
        String which represents user's input link.
    :return:
        List of available electoral party names for each municipality in certain district.
    """
    parties_link = links_lau2(parsed_html_lau1(input_link))[0]
    split_html_parties = parsed_html_lau1(parties_link)
    parties_elements = split_html_parties.find_all("td", {"class": "overflow_name"})
    return [party.text for party in parties_elements]


def table_header(input_link: str) -> list:
    """
    Generate list of table header.
    :param: input_link:
        String which represents user's input link.
    :return:
        List of table header such as municipality code, municipality name, registered
        voters, issued envelopes, valid votes and names of electoral parties.
    """
    headers = ["LAU2 Code", "LAU2 Name", "Voters", "Issued Envelopes", "Valid Votes"]
    party_n = party_names(input_link)
    # extend list of table header by names of electoral parties
    headers.extend(party_n)
    return headers


def mun_result(input_link: str) -> list:
    """
    Generate final list of electoral values for each municipality (LAU2) in certain district.
    :param: input_link:
        String which represents user's input link.
    :return:
        Nested lists of electoral data for each LAU2 in output list.
    """
    # LAU2 (municipality) links from certain parsed LAU1 link
    mun_url = links_lau2(parsed_html_lau1(input_link))
    # municipality id (code, name)
    mun_res = id_lau2(input_link)
    # general electoral data in municipalities (registered votes,
    # issued envelopes, valid votes)
    mun_voters = elect_lau1(mun_url)
    # votes for electoral parties
    el_parties = elect_parties(mun_url)
    # assigning general electoral data for particular municipality
    for g_votes in range(len(mun_res)):
        mun_res[g_votes].extend(mun_voters[g_votes])
    # assigning votes of electoral parties for particular municipality
    for p_votes in range(len(mun_res)):
        mun_res[p_votes].extend(el_parties[p_votes])
    return mun_res


def csv_export(input_link: str, output_file: str) -> csv:
    """
    Generate final output file of electoral data for selected district (LAU2).
    :param: input_link:
        String which represents user's input link.
    :param: output_file:
        Name of output file in format *csv.
    :return:
        Output file in *csv format containing electoral data for selected district (LAU2).
    """
    print(f"\u2193 Downloading data from input link: {input_link}", "Please, wait...", sep="\n")
    muns = mun_result(input_link)
    headers = table_header(input_link)
    with open(output_file, "w", encoding="utf-8") as file:
        w = csv.writer(file)
        w.writerow(headers)
        for row in muns:
            w.writerow(row)


def main():
    # check right number of input arguments in terminal
    if len(argv) != 3:
        print("Wrong number of input arguments! Process terminated.")
        quit()
    # check if input link is valid -> is included in list of LAU1 links
    elif valid_link(argv[1]) is not True:
        print("Your input link is not valid! Process terminated.")
        quit()
    # check if output file is in *csv format
    elif not argv[2].endswith('.csv'):
        print("Please, save output file into *csv. Process terminated.")
        quit()
    # valid combination
    else:
        csv_export(argv[1], argv[2])
    # path of output *csv file
    path = os.path.abspath(argv[2])
    print("\u2193 Data were successfully downloaded!", f"\u2192 Your file was saved into: {path}", sep="\n")


if __name__ == "__main__":
    main()
