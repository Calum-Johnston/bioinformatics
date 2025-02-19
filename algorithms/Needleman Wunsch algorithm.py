# Needleman Wunsch algorithm

def dynprog(alphabet, subMat, a, b):
    lst = populateScoringMatrix(alphabet, subMat, a, b)
    scoMat = lst[0]
    dirMat = lst[1]
    alignment = getBestMatching(scoMat, dirMat, a, b)
    scoreAndAlignment = [scoMat[len(a)][len(b)], alignment[0], alignment[1]]
    printMatrix(scoMat)
    printMatrix(dirMat)
    print(scoreAndAlignment)
    return scoreAndAlignment

def populateScoringMatrix(alphabet, subMat, a, b):
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            diagonal = scoMat[i-1][j-1] + subMat[alphabet.index(a[i - 1])][alphabet.index(b[j - 1])]
            up = scoMat[i-1][j] + subMat[len(alphabet)][alphabet.index(a[i - 1])]
            left = scoMat[i][j-1] + subMat[alphabet.index(b[j - 1])][len(alphabet)]
            bestScore = max(diagonal, left, up)
            if bestScore == diagonal: dirMat[i][j] = "D"
            elif bestScore == up: dirMat[i][j] = "U"
            else: dirMat[i][j] = "L"
            scoMat[i][j] = bestScore
    return [scoMat, dirMat]

def initialiseScoringMatrix(alphabet, subMat, a, b):
    scoringMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    scoringMatrix[0][0] = 0
    for x in range(1, len(a) + 1):
        scoringMatrix[x][0] = scoringMatrix[x-1][0] + subMat[len(alphabet)][alphabet.index(a[x - 1])]   
    for y in range(1, len(b) + 1):
        scoringMatrix[0][y] = scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(b[y - 1])]
    return scoringMatrix

def initialiseDirectionMatrix(alphabet, subMat, a, b):
    directionMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    for x in range(1, len(a) + 1):
        directionMatrix[x][0] = "U"
    for y in range(1, len(b) + 1):
        directionMatrix[0][y] = "L"
    return directionMatrix

def getBestMatching(scoMat, dirMat, a, b):
    xPos = len(a)
    yPos = len(b)
    aMatch = []
    bMatch = []
    while(xPos > 0 or yPos > 0):
        if(dirMat[xPos][yPos] == "D"):
            aMatch = [a[xPos - 1]] + aMatch
            bMatch = [b[yPos - 1]] + bMatch
            yPos -= 1
            xPos -= 1
        elif(dirMat[xPos][yPos] == "U"):
            aMatch = [a[xPos - 1]] + aMatch
            bMatch = ["-"] + bMatch
            xPos -= 1
        else:
            aMatch = ["-"] + aMatch
            bMatch = [b[yPos - 1]] + bMatch
            yPos -= 1
    return [aMatch, bMatch]


def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


#Examples 

#a = [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]]
#dynprof("ABC", a, "ABCACA", "BAACB")

#b = [[1,-1,-1,-1,-2],[-1,1,-1,-1,-2],[-1,-1,1,-1,-2],[-1,-1,-1,1,-2],[-2,-2,-2,-2,1]]
#dynprof("ACGT", b, "AAAC", "AGC") 

#c = [[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]]
#dynprof("ACGT", c, "GACTTAC", "CGTGAATTCAT") 

e = dynprog("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "AGTACGCA", "TATGC")
e = dynprog("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "ACGCATGA", "CGTAT")