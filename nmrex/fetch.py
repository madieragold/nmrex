import requests
from lxml import html


def structure(rcsb):
    url = 'http://www.rcsb.org/pdb/explore/explore.do?structureId={}'\
        .format(rcsb)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    urls = tree.xpath(
        '//div[@id="DownloadFilesButton"]/ul/li/a[text()="PDB Format"]/@href')
    if len(urls) > 0:
        pdb = requests.get(urls[0]).content
        with open('peptide.pdb', 'wb') as file:
            file.write(pdb)
    else:
        raise RuntimeError('PDB not found for {}'.format(rcsb))


def shifts(bmrb):
    url = 'http://www.bmrb.wisc.edu/data_library/summary/index.php?bmrbId={}'\
        .format(bmrb)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    urls = tree.xpath(
        '//div[@class="entry_details_box"]'
        '/div[@class="entry_info_float"]'
        '/p/a[text()="text file."]/@href'
    )
    star3 = [s for s in urls if s.find('/bmrb/NMR-STAR3/') >= 0]
    star2 = [s for s in urls if s.find('/bmrb/NMR-STAR2/') >= 0]
    if star3 or star2:
        star2 = requests.get(star2[0]).content
        with open('star2.str', 'wb') as file:
            file.write(star2)
        star3 = requests.get(star3[0]).content
        with open('star3.str', 'wb') as file:
            file.write(star3)
    else:
        raise RuntimeError(
            'Found {} star2 links and {} star3 links for {}'\
                .format(len(star2), len(star3), bmrb)
        )
