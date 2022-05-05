
file = open("teste.txt", "r")

print([x.strip() for x in file.read().strip().splitlines() if x.strip()])

file.close()

        
