def gameLog(message):
    f = open(f"log/log.txt", "a")
    f.write(message + '\n')
    f.close()

