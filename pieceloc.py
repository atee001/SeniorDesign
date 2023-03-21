import chess
import chess.svg
import cv2
import random
import sys
import serial
from random import randint
import math
import numpy as np
from picamera import PiCamera
from time import sleep
import json
import requests
from picamera.array import PiRGBArray
from roboflow import Roboflow
rf = Roboflow(api_key="njviJ6dI4x1A7Y4UhsDv")
project = rf.workspace().project("snd-aigsh")
model = project.version(4).model

camera = PiCamera(
    resolution=(1280, 720),
)
sleep(2)

origin = (17, 21)
x_end = (507, 21)
y_end = (17, 503)

def clrscrn():
    print("\n" * 10)
    
max_size = {"b_pawn": 8, "w_pawn": 8, "w_king": 1, "b_king": 1, "b_knight" : 2, "w_knight": 2, "w_rook": 2, "b_rook": 2,
        "w_bishop": 2, "b_bishop": 2, "b_queen": 1, "w_queen": 1}

def setup():
    prev_board = [["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
                  ["b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn", "b_pawn"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn", "w_pawn"],
                  ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"]]
    return prev_board

def numSize(arr, className):
    cnt = 0;
    for i in range(0, len(arr)):
        for j in range(0, len(arr[0])):
            if(arr[i][j] is None):
                pass
            elif(arr[i][j]['class'] == className):
                cnt = cnt + 1
    return cnt

def location(origin, x_end, y_end, obj_x, obj_y):
    if (obj_x >= origin[0]) and (obj_y >= origin[1]) and (obj_x <= x_end[0]) and (obj_y <= y_end[1]):
        x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        y_axis = range(8,0,-1)
        x_step = x_end[0]/(8.35)
        y_step = y_end[1]/(8.25)
        x_calib = 0
        y_calib = 0 
        x_offset = origin[0]
        y_offset = origin[1]
        x_index = math.floor((obj_x - x_offset + x_calib)/x_step)
        y_index = math.floor((obj_y - y_offset + y_calib)/y_step)
        
        if(x_index < 0):
            x_index = 0
        elif(x_index > 7):
            x_index = 7
            
        if(y_index < 0):
            y_index = 0
        elif(y_index > 7):
            y_index = 7
            
        return (x_axis[x_index], y_axis[y_index])
    else:
        return (-1,-1)

def test(image, numtests, origin, x_end, y_end):
    h, w = image.shape
    for i in range(numtests):
        randx = randint(1, w-1)
        randy = randint(1, h-1)
        image = cv2.circle(image, (randx, randy), 2, 0, 2)
        temp = location(origin, x_end, y_end, randx, randy)
        pos = str(temp[0]) + "," + str(temp[1])
        image = cv2.putText(image, pos, (randx+1, randy+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)

def ind_test(image, one_test, origin, x_end, y_end):
    h, w = image.shape
    for i in range(len(one_test)):
        randx = one_test[i][0]
        randy = one_test[i][1]
        image = cv2.circle(image, (randx, randy), 2, 0, 2)
        temp = location(origin, x_end, y_end, randx, randy)
        pos = str(temp[0]) + "," + str(temp[1])
        image = cv2.putText(image, pos, (randx+1, randy+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 2, cv2.LINE_AA)
        
def printJsonBoard(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            temp = board[i][j]
            if(temp is None):
                print(' empty ', end = " ")
            else:
                print(temp['class'], end = " ")
            if (j == 7):
                print('\n')
                
def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            temp = board[i][j]
            if(temp is None):
                print(' empty ', end = " ")
            else:
                print(temp, end = " ")
            if(j == 7):
                print('\n')
                
def takePic():
    rawCapture = PiRGBArray(camera) 
    camera.capture(rawCapture,format="bgr", use_video_port=True)
    img = rawCapture.array
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def preProc(img):
    pts1 = np.float32([[172, 270], [710, 275], [165, 800], [690, 820]])
    pts2 = np.float32([[0, 0], [525, 0], [0, 525], [525, 525]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (525, 525))
    return result

 def compare_board(board_one, board_two):
     return json.dumps(board_one, sort_keys = True) == json.dumps(board_two, sort_keys = True)


def chesser():
    board = chess.Board()
    prev_state = setup()
    player = "white"
    
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

        while(user_input not in san_moves):            
            clrscrn()
            print("Not a legal move, please try again")
            user_input = input()
        
        lastMove = board.push_san(user_input)
        last_move = str(lastMove)

        board.pop() #pops the board to get the check if there has is a piece to be taken at the destination
        piece_at_destination = board.piece_at(lastMove.to_square)

        board.push_san(user_input)        
        print(board)

        #create an SVG file of the current board for the virtual player to view
        boardsvg = chess.svg.board(board, size=350) 
        outputfile = open('current_board.svg', "w")
        outputfile.write(boardsvg)        
        
        if piece_at_destination is not None:
            print("A piece was captured!")
            send2 = 't' + last_move[2] + last_move[3]
            ser.write(send2.encode())
            ser.write(b'\n')
        
        sleep(1)
        
        send1 = 'm' + last_move
        print(send1)
        ser.write(send1.encode())
        ser.write(b'\n')              
                
        if(len(last_move) == 4): 
            start_pos = prev_state[len(prev_state) - int(last_move[1])][(ord(last_move[0])-97)]
            prev_state[len(prev_state) - int(last_move[1])][(ord(last_move[0])-97)] = "empty"
            prev_state[len(prev_state) - int(last_move[3])][(ord(last_move[2])-97)] = start_pos #update final position made by virtual player
        else:
            sys.exit(1)
            print("Error last move was no 4 digits: ", last_move)
        
        if(board.is_checkmate()):
            player = "white"
            sleep(15)
            break       
        
        while ser.in_waiting < 1:
#             print("Button not pressed")
            pass
        #polling until arduino sends signal that move was actuated
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print(data)
            
        ser.flushInput()   
        two_img = takePic()
        result_two = preProc(two_img)
        cv2.imwrite("PlayerTwo.jpg", result_two)
        cv2.imshow("PlayerTwo.jpg", result_two)
        predict_two = model.predict("PlayerTwo.jpg", confidence=70, overlap=50).json()
        curr_state = np.empty((8,8), dtype = 'object')
        for pred in predict_two['predictions']:
            middle = ((float(pred['x'])), (float(pred['y'])))
            position = location(origin, x_end, y_end, middle[0], middle[1])
            if position[1] != -1:
                x_pos = int(ord(position[0])-97)    
                y_pos = int(8 - int(position[1]))
                piece = (curr_state[y_pos][x_pos])
                if (piece is None):
                    curr_state[y_pos][x_pos] = (pred)
                else:  #collision so do non maximum suppression   
                    #if board pos already has three bishops and inference finds a knight and there is < 2 knights on the board
                #choose knight
                    if((numSize(curr_state, piece['class']) > max_size[piece['class']]) and (numSize(curr_state, pred['class']) < max_size[pred['class']])):
                        curr_state[y_pos][x_pos] = pred
    #               if board has 1 bishop and inference thinks there is a knight but there is already 3 knights choose bishop
                    elif(numSize(curr_state, pred['class']) >= max_size[pred['class']] and (numSize(curr_state, piece['class']) <= max_size[piece['class']])):
                        curr_state[y_pos][x_pos] = piece
    #                 if neither of these meaning board and inference < max size choose the one with greater confidence                   
                    elif(pred['confidence'] >= (piece['confidence'])):
                        curr_state[y_pos][x_pos] = (pred)
                    name = str(pred['class']) + " at " + str(position[0]) + ", " + str(position[1])
        old_pos = ''
        new_pos = ''
        for x in range(0,len(prev_state)):
            if(len(old_pos + new_pos) == 4):
                break
            for y in range(0,len(prev_state[0])):
                curr_pos = (curr_state[x][y])
                if(curr_pos is None):
                    if ((prev_state[x][y]) != "empty"):                    
                        old_pos = chr(y + 97) + str(8-x)                   
                else:
                    if((prev_state[x][y]) != curr_pos['class']):
                        new_pos = chr(y + 97) + str(8-x) 
                if(len(old_pos + new_pos) == 4):
                    break
        last_move = old_pos + new_pos
        try:
            board.push_san(last_move)
        except:
            #if error pushing last move means multiple pieces are different from current board state which should not be possible meaning bad inference from model
            printJsonBoard(curr_state)
            print("Bad Lighting for Object Detection Model")
            sys.exit(1)
            
        boardsvg = chess.svg.board(board, size=350) 
        outputfile = open('current_board.svg', "w")
        outputfile.write(boardsvg)
        
        if(len(last_move) == 4): 
            start_pos = prev_state[len(prev_state) - int(last_move[1])][(ord(last_move[0])-97)]
            prev_state[len(prev_state) - int(last_move[1])][(ord(last_move[0])-97)] = "empty"
            prev_state[len(prev_state) - int(last_move[3])][(ord(last_move[2])-97)] = start_pos #update final position made by virtual player
        else:            
            print("Error last move was not 4 digits: ", last_move)
            sys.exit(1)
        axis_img = result_two
        
        if(board.is_checkmate()):
            player = "black"
            break      
        
    print("Gameover, board is in checkmate ")
    print(player, " won!")
    cv2.destroyAllWindows()
def main():    
    sleep(3)
    chesser()
    
if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except:
        ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
        print("Wrong Address switched address to /dev/ttyACM1")
    finally:    
        ser.reset_input_buffer()
        main()
        
    

