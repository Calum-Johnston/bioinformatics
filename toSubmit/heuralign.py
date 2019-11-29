# FASTA algorithm (Heuristic)
import itertools

def heuralign(alphabet, subMat, a, b, ktup):
    indexTable = initialiseIndexTable(a, ktup)
    matches = getMatches(indexTable, b, ktup)
    #if matches are 0 reduce ktup by 1 and start again
    diagonalPairs = orderPairs(matches, a, b)
    scoreDiagonals(diagonalPairs, subMat, alphabet, a, b)

def initialiseIndexTable( a, ktup):
    keywords = [''.join(i) for i in itertools.product("ABCD", repeat = 2)]
    indexTable = {}
    for keyword in keywords:
        indexTable[keyword] = []
    for i in range(0, len(a) + 1 - ktup):
        lst = indexTable[a[i:i+ktup]]
        lst.append(i)
        indexTable[a[i:i+ktup]] = lst
    return indexTable

def getMatches(indexTable, b, ktup):
    matches = []
    for i in range(0, len(b) + 1 - ktup):
        bsubString = b[i:i+ktup]
        aMatchPositions = indexTable[bsubString]
        for position in aMatchPositions:
            matches.append([position, i])
    return matches

def orderPairs(matches, a, b):
    diagonalPairs = {}
    for x in range(-len(a), len(b) + 1):
        diagonalPairs[x] = []
    for match in matches:
        lst = diagonalPairs[(match[1]-match[0])]
        lst.append(match)
        diagonalPairs[(match[1]-match[0])] = lst
    return diagonalPairs

def scoreDiagonals(diagonalPairs, subMat, alphabet, a, b, ktup):
    x = 0; y = 0
    diagonalScores = {}
    for diagonalNum,diagonalValues in diagonalPairs.items():
        if(diagonalValues != []):  # i.e. diagona
            currentAlign = []
            currentScore = 0
            previousAlign = []
            previousScore = 0
            for dia in diagonalValues:     
                if not(dia in previousAlign):
                    currentScore += subMat[alphabet.index(a[dia[0]])][alphabet.index(b[dia[1]])] + subMat[alphabet.index(a[dia[0] + 1])][alphabet.index(b[dia[1] + 1])]
                    currentAlign.append(dia)
                    x = dia[0] + 1; y = dia[1] + 1; scoreDecreasing = False
                    while(x + ktup < len(a) + 1 and  y < len(b) + 1 and scoreDecreasing == False):
                        tempScore = subMat[alphabet.index(a[x])][alphabet.index(b[y])] + subMat[alphabet.index(a[x + 1])][alphabet.index(b[y + 1])]
                        if(tempScore + currentScore < currentScore):
                            scoreDecreasing = True
                        else:
                            currentScore += tempScore
                            currentAlign.append([a[x],b[y]])
                
            



# SMITH-WATERSON (local alignment of two strings)
# LIMITED to only part of the matrices

def dynprog(alphabet, subMat, a, b, diagonal, diagonalWidth):
    lst = populateScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth)
    scoMat = lst[0]; dirMat = lst[1]; maxValue = lst[2]; maxValuePosition = lst[3]
    alignment = getBestMatching(scoMat, dirMat, a, b, maxValuePosition)
    scoreAndAlignment = [maxValue, alignment[0], alignment[1]]
    return scoreAndAlignment

def populateScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth):
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth)
    maxValue = 0
    maxValuePosition = [0, 0]
    startX = 0; startY = 0;

    # Find starting positions
    if(diagonal > 0):
        startY = diagonal #(startX is already 0 so no need to do that here)
    elif(diagonal < 0):
        startX = diagonal
    
    # Loop through matrix until we are out of bounds
    while(startX < len(a) and startY < len(b)):
        # For each row, loop through values that could only be within diagonal restriction
        for diagonalPoint )

    for x in range(1, len(a) + 1):
        for y in range(1, len(b) + 1):
            if((diagonal - diagonalWidth) < (y-x) < (diagonal + diagonalWidth)):

                dia = scoMat[x-1][y-1] + subMat[alphabet.index(a[x - 1])][alphabet.index(b[y - 1])]

                if(scoMat[x-1][y] != ' '): #up is available
                    up = scoMat[x-1][y] + subMat[len(alphabet)][alphabet.index(a[x - 1])]
                    bestScore = max(dia, up, 0)
                    if bestScore == dia: dirMat[x][y] = "D"
                    elif bestScore == up: dirMat[x][y] = "U"
                elif(scoMat[x][y-1] != ' '): #left is available
                    left = scoMat[x][y-1] + subMat[alphabet.index(b[y - 1])][len(alphabet)]
                    bestScore = max(dia, left, 0)
                    if bestScore == dia: dirMat[x][y] = "D"
                    elif bestScore == left: dirMat[x][y] = "L"
                else:
                    left = scoMat[x][y-1] + subMat[alphabet.index(b[y - 1])][len(alphabet)]
                    up = scoMat[x-1][y] + subMat[len(alphabet)][alphabet.index(a[x - 1])]
                    bestScore = max(dia, left, up, 0)
                    if bestScore == dia: dirMat[x][y] = "D"
                    elif bestScore == up: dirMat[x][y] = "U"
                    elif bestScore == left: dirMat[x][y] = "L"
                scoMat[x][y] = bestScore
                if(bestScore > maxValue):
                    maxValue = bestScore; maxValuePosition[0] = x; maxValuePosition[1] = y
    printMatrix(scoMat)
    printMatrix(dirMat)
    return [scoMat, dirMat, maxValue, maxValuePosition]

def initialiseScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth):
    scoMat = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    scoMat[0][0] = 0
    y = 0
    for x in range(1, len(a) + 1):
        if((diagonal - diagonalWidth) < (y-x) < (diagonal + diagonalWidth)):
            scoMat[x][0] = 0
    x = 0
    for y in range(1, len(b) + 1):
        if((diagonal - diagonalWidth) < (y-x) < (diagonal + diagonalWidth)):
            scoMat[0][y] = 0
    return scoMat

def initialiseDirectionMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth):
    dirMat = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    y = 0
    for x in range(1, len(a) + 1):
        if((diagonal - diagonalWidth) < (y-x) < (diagonal + diagonalWidth)):
            print("s")
            dirMat[x][0] = "U"
    x = 0
    for y in range(1, len(b) + 1):
        if((diagonal - diagonalWidth) < (y-x) < (diagonal + diagonalWidth)):
            dirMat[0][y] = "L"
    return dirMat

def getBestMatching(scoMat, dirMat, a, b, maxValuePos):
    xPos = maxValuePos[0]; yPos = maxValuePos[1]
    aMatch = []; bMatch = []
    while(scoMat[xPos][yPos] != 0):
        if(dirMat[xPos][yPos] == "D"):
            aMatch = [xPos - 1] + aMatch
            bMatch = [yPos - 1] + bMatch
            xPos -= 1 ; yPos -= 1
        elif(dirMat[xPos][yPos] == "U"):
            xPos -= 1
        else:
            yPos -= 1
    return [aMatch, bMatch]  

def printMatrix(matrix):
    for mat in matrix:
        print(mat)  



a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "ABDAAB", "AB", 2)

#a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC4", "CCAAADDAAAACCAAADDCCAAAA", 2)
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])

#e = dynprog("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "ABDAAAA", "ABACC", 1, 2)
