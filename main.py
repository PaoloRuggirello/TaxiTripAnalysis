import Utils

if __name__ == '__main__':
    args = Utils.initializeParser()
    year = Utils.getYearFromParser(args.year)
    month = Utils.getMonthFromParser(args.month)
    print(Utils.generateFileName(year, month))
    print('Hello world')