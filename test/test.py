def lineCount():
    with open("./TELLTALE_01_30.TAB") as fileName:
        x = 0
        for line in fileName:
            x += 1
        print(x)

if __name__ == '__main__':
    lineCount()
