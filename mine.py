import lib


if __name__ == '__main__':
    filePath = "./Data/"
    files = getFiles(filePath)
    splits = splitName(files)
    matched = match(splits)
    searchCategory(matched, filePath)
