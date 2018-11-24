
eras = ['Jahiliy','SadrIslam','Umayyad','Abbasid','Dual','Modern']
eraStart = [0,610,661,750,1258,1798]
eraEnd = [610,661,750,1258,1798,2019]
path = "."

def createDirectories():
    import os
    for x in eras:
        if not os.path.isdir(path + '/' + x):
            os.mkdir(path + '/' + x)  # line B
            print(x + ' created.')

if __name__ == "__main__":
    createDirectories()