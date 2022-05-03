def read_chunk():
    file = open("teste.txt", "r")

    for line in file:
        yield line.strip()
        



#main
for buffer in read_chunk():
    print(buffer)
    print("-----------------------")
def fit():
    pass