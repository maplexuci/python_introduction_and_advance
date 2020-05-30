import re

from urllib import request


class Spider():
    url = 'https://www.huya.com/g/100043'
    root_pattern = '<span class="txt">([\s\S]*?)</li>'
    name_pattern = '<i class="nick" title="([\s\S]*?)">'
    number_pattern = '<i class="js-num">([\s\S]*?)</i>'

    def __fetch_content(self):
        r = request.urlopen(Spider.url)

        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        # To remove any non-necessary spaces if any, and to convert the list format of each match to string.
        lamb = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0].strip()
        }
        return map(lamb, anchors)

    def __sort(self, anchors):
        """Sort the data fetched from the web

        Arguments:
            anchors {[type]} -- [description]
        """
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor): ## anchor here represents each individule dict element in anchors.
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print(str(rank+1) + ': ' + anchors[rank]['name'] + '     ' + anchors[rank]['number'])

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
