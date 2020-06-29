import json


BIO_BOOKS = json.dumps(
{
    'items': {
        'numFound': 0,
        'docs': [],
    }
}
)

BIO_PRINTS = json.dumps(
{
    'items': {
        'numFound': 0,
        'docs': [],
    }
}
)

ANNOTATIONS = json.dumps(
{
    'response': {
        'numFound': 1,
        'docs': [{'rel_is_annotation_of_ssim': ['test:1234']}],
    }
}
)

PAGES = json.dumps(
{
    'response': {
        'numFound': 1,
        'docs': [{'pid': 'test:5678'}],
    }
}
)

PRINTS = json.dumps(
{
    'response': {
        'numFound': 1,
        'docs': [{'pid': 'testsuite:123456'}],
    }
}
)

ITEM_API_DATA = json.dumps(
{
    'brief': {
        'title': ['test item']
    },
    'pid': 'testsuite:123456',
    'rel_has_pagination_ssim': ['1'],
    'relations': {
        'hasAnnotation': [{'pid': 'testsuite:234'}]
    },
    'uri': 'https://localhost/studio/item/testsuite:123456/',
}
)

BOOK_ITEM_API_DATA = json.dumps(
{
    'brief': {
        'title': ['test book item']
    },
    'pid': 'testsuite:123',
    'relations': {
        'hasPart': [{'pid': 'testsuite:123456'}],
    },
}
)

SAMPLE_ANNOTATION_XML = '''<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd">
  <mods:abstract>This book was first published in the 1630's. The plates were later used to illustrate the Antiquités Romaines expliquées dans les memoires de comte de B*** (1750) http://library.brown.edu/projects/rome/books/253682/?book_list_page=1</mods:abstract>
  <mods:originInfo>
    <mods:dateOther type="impression">1695</mods:dateOther>
  </mods:originInfo>
  <mods:note type="resp">Evie Lincoln</mods:note>
  <mods:titleInfo lang="la">
    <mods:title>Roma vetus ac recens utriusque Ædificiis illustrata</mods:title>
  </mods:titleInfo>
  <mods:titleInfo lang="en">
    <mods:title>Ancient and Modern Rome</mods:title>
  </mods:titleInfo>
  <mods:genre authority="aat">book</mods:genre>
  <mods:name xlink:href="0260">
    <mods:namePart>Donati, Alessandro</mods:namePart>
    <mods:role>
      <mods:roleTerm>author</mods:roleTerm>
    </mods:role>
  </mods:name>
</mods:mods>'''

INVALID_SAMPLE_ANNOTATION_XML = '''<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd">
  <mods:titleInfo lang="la">
    <mods:title>Roma vetus ac recens utriusque Ædificiis illustrata</mods:title>
  </mods:titleInfo>
  <mods:titleInfo lang="en">
    <mods:title>Ancient and Modern Rome</mods:title>
  </mods:titleInfo>
  <mods:name xlink:href="">
    <mods:namePart>Donati, Alessandro</mods:namePart>
    <mods:role>
      <mods:roleTerm>author</mods:roleTerm>
    </mods:role>
  </mods:name>
</mods:mods>'''

