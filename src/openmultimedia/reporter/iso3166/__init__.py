from os.path import join


class CountriesParser:

    def __init__(self, path):
        self._path = path
        self._countries = {}

    def parse(self):
        countriesFile = file(join(self._path, 'countries.txt'))
        for line in countriesFile.readlines():
            if ':' not in line:
                continue
            self._parseCountry(line)

    def _parseCountry(self, line):
        code, name = line.split(':')
        code = code.strip()
        self._countries[code] = name.strip().decode('ISO-8859-1')

    def getCountries(self):
        return self._countries.items()

    def getCountriesNameOrdered(self):
        invertedItems = map(lambda (x, y): (y, x), self._countries.items())
        invertedItems.sort()
        return map(lambda (x, y): (y, x), invertedItems)


if __name__ == '__main__':
    c = CountriesParser('iso3166')
    c.parse()
