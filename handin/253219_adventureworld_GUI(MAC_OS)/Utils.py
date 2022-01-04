def gameLog(message):
    """
        A global logging function that tracks the
        user's journey in a separate text file.
    """
    f = open(f"log/log.txt", "a")
    f.write(message + '\n')
    f.close()

