# FASTA algorithm (Heuristic)
import itertools

def heuralign(alphabet, subMat, a, b, ktup):
    indexTable = initialiseIndexTable(a, ktup)
    matches = getMatches(indexTable, b, ktup)
    #if matches are 0 reduce ktup by 1 and start again
    diagonalPairs = orderPairs(matches, a, b)
    scoreDiagonals(diagonalPairs, subMat, alphabet, a, b, ktup)

def initialiseIndexTable(a, ktup):
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
            firstMatch = diagonalValues[0]
            lastMatch = diagonalValues[len(diagonalValues) - 1]
            if(firstMatch == lastMatch):
                diagonalScores[diagonalNum] = scoreDiagonal(alphabet, subMat, a, b, firstMatch[0], firstMatch[1], lastMatch[0], ktup) 
            else:
                print(firstMatch, lastMatch)
                diagonalScores[diagonalNum] = scoreDiagonal(alphabet, subMat, a, b, firstMatch[0], firstMatch[1], lastMatch[0], ktup)
    return diagonalScores

def scoreDiagonal(alphabet, subMat, a, b, startA, startB, end, ktup):
    totalScore = 0
    currentPos = 0
    while(startA + currentPos < end + ktup):
        totalScore += subMat[alphabet.index(a[startA + currentPos])][alphabet.index(b[startB + currentPos])]
        currentPos += 1
    return totalScore



# SMITH-WATERSON (local alignment of two strings)
# LIMITED to only part of the matrices

def dynprog(alphabet, subMat, a, b, diagonal, diagonalWidth):
    lst = populateScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth)
    scoMat = lst[0]; dirMat = lst[1]; maxValue = lst[2]; maxValuePosition = lst[3]
    alignment = getBestMatching(scoMat, dirMat, a, b, maxValuePosition)
    scoreAndAlignment = [maxValue, alignment[0], alignment[1]]
    return scoreAndAlignment

def populateScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth):
    maxValue = 0
    maxValuePosition = [0, 0]
    startX = 1; startY = 1

    # Initialise matrices
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)

    # Find starting positions
    if(diagonal > 0):
        startY = diagonal + 1 #(startX is already 0 so no need to do that here)
    elif(diagonal < 0):
        startX = abs(diagonal) + 1

    # Get constraining diagonals (left and right)
    diagonalL = diagonal - diagonalWidth
    diagonalR = diagonal + diagonalWidth

    # Loop through matrix until we are out of bounds
    while(startX < len(a) + 1 or startY < len(b) + 1):

        # For each row, loop through values that could only be within diagonal restriction
        for diagonalPoint in range(startY - diagonalWidth, startY + diagonalWidth + 1):
        
            #Check if new y position is actually within the y range
            if(diagonalPoint >= 1 and diagonalPoint < len(b) + 1):

                # Get the diagonal score
                dia = scoMat[startX-1][diagonalPoint - 1] + subMat[alphabet.index(a[startX - 1])][alphabet.index(b[diagonalPoint - 1])]

                # Get the left point (if possible)
                if(scoMat[startX][diagonalPoint - 1] != ' '): 
                    left = scoMat[startX][diagonalPoint-1] + subMat[alphabet.index(b[diagonalPoint - 1])][len(alphabet)]
                else:
                    left = False

                # Get the up point (if possible)
                if(scoMat[startX-1][diagonalPoint] != ' '): #up is available
                    up = scoMat[startX-1][diagonalPoint] + subMat[len(alphabet)][alphabet.index(a[startX - 1])]
                else:
                    up = False

                # Calculates the value for the backtracking matrix
                if(up == False):
                    bestScore = max(dia, left, 0)
                    if bestScore == dia: dirMat[startX][diagonalPoint] = "D"
                    elif bestScore == left: dirMat[startX][diagonalPoint] = "L"
                elif(left == False):
                    bestScore = max(dia, up, 0)
                    if bestScore == dia: dirMat[startX][diagonalPoint] = "D"
                    elif bestScore == up: dirMat[startX][diagonalPoint] = "U"
                else:
                    bestScore = max(dia, left, up, 0)
                    if bestScore == dia: dirMat[startX][diagonalPoint] = "D"
                    elif bestScore == up: dirMat[startX][diagonalPoint] = "U"
                    elif bestScore == left: dirMat[startX][diagonalPoint] = "L"

                # Updates the scoring matrix
                scoMat[startX][diagonalPoint] = bestScore

                # Updates the best score value
                if(bestScore > maxValue):
                    maxValue = bestScore; maxValuePosition[0] = startX; maxValuePosition[1] = diagonalPoint

        # Increment the values of which diagonal we are following
        startX += 1
        startY += 1

    return [scoMat, dirMat, maxValue, maxValuePosition]

# Function simply initialises the scoring Matrix
def initialiseScoringMatrix(alphabet, subMat, a, b):
    scoMat = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    scoMat[0][0] = 0
    for x in range(1, len(a) + 1):
        scoMat[x][0] = 0
    for y in range(1, len(b) + 1):
        scoMat[0][y] = 0
    return scoMat

def initialiseDirectionMatrix(alphabet, subMat, a, b):
    dirMat = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    for x in range(1, len(a) + 1):
        dirMat[x][0] = "U"
    for y in range(1, len(b) + 1):
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



#a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "ABDAAB", "AB", 2)

a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC", "CCAAADDAAAACCAAADDCCAAAA", 2)
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])

#e = dynprog("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "ABDAAAA", "ABACC", 1, 2)
#print(e[1], e[2])