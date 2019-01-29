#!/usr/bin/env python3
""" functions related to printing cards """
import sys
import os.path


def writedict():
    """ return the dictionnary """
    col = ["♠", "♥", "♦", "♣"]
    d = {}
    for i in range(0, 4):
        for j in range(1, 15):
            if j <= 10:
                d[i*14+j] = col[i] + str(j)
            else:
                a = ""
                if j == 11:
                    a = "V"
                if j == 12:
                    a = "C"
                if j == 13:
                    a = "Q"
                if j == 14:
                    a = "K"
                d[i*14+j] = col[i] + a
    for i in range(14*4 + 1, 14*4 + 2 + 21):
        d[i] = "T" + str(i - 14*4)
    d[78] = "JJ"
    return d


if __name__ == "__main__":
    """ save the dictionnary """
    if len(sys.argv) != 2:
        print("error : require one argument (filename)")
        sys.exit(1)
    fname = sys.argv[1]
    if os.path.isfile(fname):
        print("Delete {}? y/n".format(fname))
        a = input()
        if a != "" and a == 'n':
            sys.exit(0)
    try:
        with open(fname, 'w') as f:
            d = writedict()
            for i in range(1, 79):
                f.write("d[{}] = \"{}\"\n".format(i, d[i]))
            f.write("\n\n")
            f.write("D = {\n")
            for i in range(1, 79):
                if i != 78:
                    f.write("\t\t{} : \"{}\",\n".format(i, d[i]))
                else:
                    f.write("\t\t{} : \"{}\"\n".format(i, d[i]))
            f.write("\t\t}\n")
        print("Done, saved as {}".format(fname))
    except Exception as e:
        #print("error :", e.message, e.args)
        print(e)
        sys.exit(0)

