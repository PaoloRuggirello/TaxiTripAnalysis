import Utils

if __name__ == '__main__':
    args = Utils.initializeParser()
    year = Utils.getYearFromParser(args.year)
    month = Utils.getMonthFromParser(args.month)
    fileName = Utils.generateFileName(year, month)
    dataframe = Utils.readCsv(fileName)
    print('Hello world')