```import chess
import chess.svg
import serial

flag = 0

def clrscrn():
    print("\n" * 10)

def chesser():
    board = chess.Board()
    
    while(not board.is_checkmate()):
        #virtual player's turn
        print(board)

        #create an SVG file of the current board for the virtual player to view
        boardsvg = chess.svg.board(board, size=350) 
        outputfile = open('current_board.svg', "w")
        outputfile.write(boardsvg)

        print("Outputted SVG file to view gamestate \n")

        print("Please pick one of the following legal moves:")
        print(board.legal_moves)
        legalMoves = list(board.legal_moves)
        
        san_moves = []
        for move in legalMoves:
            san_move = board.san(move)
            san_moves.append(san_move)

        user_input = input()

        if(user_input not in san_moves):
            clrscrn()
            print("Not a legal move, please try again")
        else:

            lastMove = board.push_san(user_input)
            last_move = str(lastMove)
            print(lastMove)

            board.pop() #pops the board to get the check if there has is a piece to be taken at the destination
            piece_at_destination = board.piece_at(lastMove.to_square)
            print(piece_at_destination)

            board.push_san(user_input)

            send1 = 'm' + last_move[0] + last_move[1] + last_move[2] + last_move[3]
            print(send1)

            if piece_at_destination is not None:
                print("A piece was captured!")
                send2 = 't' + last_move[2] + last_move[3] #t designates the piece taken state of arduino SM, could switch out for a number character
                #ser.write(send2.encode('ascii')) UNCOMMENT

            #ser.write(send1.encode('ascii')) UNCOMMENT

        #start physical players turn
        #wait for button serial signal
        #while ser.in_waiting < 1:
        #    pass

        #after button serial signal is received
        #flush input buffer
        #ser.reset_input_buffer()

        #if ser.in_waiting > 0:
        #    line = ser.readline().decode('ascii').rstrip()

        #andrew code for taking a picture and sending it to API
        #while 1: #FIXME 
        #   pass
        #cross reference what APi sent back and prior 2D array

        #board.push_san()#put the full pos and destination in here

        #end of player 2 turn 
        
    print("Gameover, board is in checkmate")


def main():
    #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #ser.reset_input_buffer()

    chesser()

if __name__ == "__main__":
    main()