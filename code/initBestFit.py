import numpy as np

def bestFit(numberOfPieces, numberOfBins, pieceDimensions, binDimensions):
    bestFitResult = np.zeros(numberOfPieces, dtype=int)

    # Loop through all pieces
    for i in range(numberOfPieces):
        bestFit = 0 # Best fit for the current piece
        bestFitIndex = -1 # Index of the bin with the best fit

        # Loop through all bins
        for j in range(numberOfBins):
            binWidth, binHeight = binDimensions[j] # Get the dimensions of the current bin

            # Get the dimensions of the current piece
            pieceWidth, pieceHeight = pieceDimensions[i]
            # Check if the piece fits in the bin
            if pieceWidth <= binWidth and pieceHeight <= binHeight:
                wastedSpace = binWidth * binHeight - pieceWidth * pieceHeight

                # Check if the current bin is the best fit
                if binWidth * binHeight < bestFit or bestFit == 0:
                    bestFit = binWidth * binHeight

                    # Check if wasted space is less than the best fit to update the best fit
                    if wastedSpace < bestFit:
                        bestFit = wastedSpace
                        bestFitIndex = j

        # Update the dimensions of the bin if the piece fits in the bin
        if bestFitIndex != -1:
            binDimensions[bestFitIndex] = (binDimensions[bestFitIndex][0] - pieceWidth, binDimensions[bestFitIndex][1] - pieceHeight)
            bestFitResult[i] = bestFitIndex

    return bestFitResult

# Code to test bestFit

numberOfPieces = 5
numberOfBins = 2
piecesDimensions = [(5,6), (1,1), (1,2), (4,2), (3,3)]
binDimensions = [(5, 10), (3, 9)]

print(bestFit(numberOfPieces, numberOfBins, piecesDimensions, binDimensions))