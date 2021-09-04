"""

Chess Game
made with pygame

by Daniel Escorriola

"""

import pygame, sys

# window size
frame_size_x = 720
frame_size_y = 620

check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')
    

# initialise game window
pygame.display.set_caption('Chess Game')
game_window = pygame.display.set_mode((frame_size_x,frame_size_y))

page = 'initial'
game_status = 'initial'
turn = 'whites'
message = ""
click_position = ""
x, y = None, None
winner = None
cell_piece = [None]*3   # [piece name, x, y]  example: ['knight', 0, 1]

board = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8]

# determine colors (r,g,b)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(80, 80, 80)
dark_brown = pygame.Color(101, 67, 33)
light_brown = pygame.Color(218, 179, 139)
background_color = pygame.Color(248, 240, 232)
lime_green = pygame.Color(50,205,50)

# load icons
king_img = pygame.image.load('img/chess-king-solid.svg')
queen_img = pygame.image.load('img/chess-queen-solid.svg')
knight_img = pygame.image.load('img/chess-knight-solid.svg')
bishop_img = pygame.image.load('img/chess-bishop-solid.svg')
rook_img = pygame.image.load('img/chess-rook-solid.svg')
pawn_img = pygame.image.load('img/chess-pawn-solid.svg')

# resize icons
king_img = pygame.transform.scale(king_img, (53, 53))
queen_img = pygame.transform.scale(queen_img, (53, 53))
knight_img = pygame.transform.scale(knight_img, (53, 53))
bishop_img = pygame.transform.scale(bishop_img, (53, 53))
rook_img = pygame.transform.scale(rook_img, (53, 53))
pawn_img = pygame.transform.scale(pawn_img, (53, 53))

option_img = [queen_img, knight_img, bishop_img, rook_img]
options = ['queen', 'knight', 'bishop', 'rook']


def main():
    """
    This function wil hold the main part of the game,
    """
    global board
    
    if game_status == 'initial':
        board = [['rookbl','knightbl','bishopbl','queenbl','kingbl','bishopbl','knightbl','rookbl'],
                 ['pawnbl']*8,[None]*8,[None]*8,[None]*8,[None]*8,['pawnwh']*8,
                 ['rookwh','knightwh','bishopwh','queenwh','kingwh','bishopwh','knightwh','rookwh']]
    
    draw_board()
    
    if click_position != "":
        pygame.draw.polygon(game_window, lime_green, click_position)

    ilustrate()
    
    pygame.display.update()
    game_window.fill(background_color)
    


def draw_board():
    """
    This function will draw the chess board.
    """
    # Draw vertical lines 
    for i in range(108,613,63):
        pygame.draw.line(game_window, black, (i,58), (i,562), 3)
    
    # Draw horizontal lines
    for i in range(58,563,63):
        pygame.draw.line(game_window, black, (108,i), (612,i), 3)
        
    # Paint the cells
    big_back = pygame.draw.polygon(game_window, light_brown, [(108,58),(612,58),(108,562),(612,562)])
    game_window.fill(light_brown, rect=big_back)
    
    count_i = 0
    count_j = 0
    
    for i in range(108,611, 63):
        for j in range(58,561, 63):
            if ( count_i + count_j ) % 2 != 0:
                cell = pygame.draw.polygon(game_window, dark_brown, [(i,j),(i+63,j),(i+63,j+63),(i,j+63)])
                game_window.fill(dark_brown, rect=cell)
            count_j += 1
        count_i += 1


def fill(img, color):
    """
    This function fills the pixels of an image with a color
    """
    w, h = img.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = img.get_at((x, y))[3]
            img.set_at((x, y), pygame.Color(r, g, b, a))


def ilustrate():
    """
    This function will show all the pictures of the pieces.
    """
    global board
    
    for i in range(0,8):
        for j in range(0,8):
            img = ""
            color = ""
            
            if board[i][j] != None and 'bl' in board[i][j]:
                color = black
                if 'king' in board[i][j]:
                    img = king_img
                elif 'queen' in board[i][j]:
                    img = queen_img
                elif 'knight' in board[i][j]:
                    img = knight_img
                elif 'bishop' in board[i][j]:
                    img = bishop_img
                elif 'rook' in board[i][j]:
                    img = rook_img
                elif 'pawn' in board[i][j]:
                    img = pawn_img
            elif board[i][j] != None and 'wh' in board[i][j]:
                color = white
                if 'king' in board[i][j]:
                    img = king_img
                elif 'queen' in board[i][j]:
                    img = queen_img
                elif 'knight' in board[i][j]:
                    img = knight_img
                elif 'bishop' in board[i][j]:
                    img = bishop_img
                elif 'rook' in board[i][j]:
                    img = rook_img
                elif 'pawn' in board[i][j]:
                    img = pawn_img
            
            if img != '':
                fill(img, color)
                game_window.blit(img, (113+63*(j),63+63*(i)))
                

def user_click():
    """
    This function determines what happens when the player clicks
    """
    global page, turn, winner, board, click_position, cell_piece, game_status, x, y
    
    # get coordenates of the mouse click
    
    
    if page == 'home' and game_status != 'ended':
        x, y  = pygame.mouse.get_pos()
        counter = 0
        
        x = (x - 108) // 63
        y = (y - 58) // 63
        
        if click_position == [(108+63*x,58+63*y),(108+63*(x+1),58+63*y),(108+63*(x+1),58+63*(y+1)),(108+63*x,58+63*(y+1))]:
            click_position = ""
            cell_piece = [None]*3
        elif board[y][x] == None:
            if cell_piece[0] == None:
                click_position = ""
            else:
                if is_legal(x, y, kill=False):
                    board[cell_piece[1]][cell_piece[2]] = None
                    board[y][x] = cell_piece[0]
                    
                    if turn == 'whites':
                        turn = 'blacks'
                    else:
                        turn = 'whites'
                        
                    click_position = ""
                    cell_piece = [None]*3
                    
        elif board[y][x] != None and cell_piece[0] == None:
            if turn[:2] in board[y][x]:
                click_position = [(108+63*x,58+63*y),(108+63*(x+1),58+63*y),(108+63*(x+1),58+63*(y+1)),(108+63*x,58+63*(y+1))]
                cell_piece = [board[y][x],y,x]
            
            game_status = 'started'
        elif board[y][x] != None and cell_piece[0] != None:
            if ('wh' in board[y][x] and 'bl' in cell_piece[0]) or ('bl' in board[y][x] and 'wh' in cell_piece[0]):
                # If the king gets killed, the game is over
                if is_legal(x, y, kill=True) and 'king' in board[y][x]:
                    click_position = ""
                    cell_piece = [None]*3
                    
                    if turn == 'whites':
                        winner = 'whites'
                    else:
                        winner = 'blacks'
                    
                    page = 'over'
                elif is_legal(x, y, kill=True):
                    board[cell_piece[1]][cell_piece[2]] = None
                    board[y][x] = cell_piece[0]
                    
                    if turn == 'whites':
                        turn = 'blacks'
                    else:
                        turn = 'whites'

                    click_position = ""
                    cell_piece = [None]*3        

        for i in range(0,8):
            for j in range(0,8):
                if board[i][j] != None:
                    counter += 1
                    
        if counter == 2:
            winner = 'draw'
            page = 'over'
        
    elif page == 'options':
        z, w = pygame.mouse.get_pos()
        
        z = (z - 234) // 63
        w = (w - 252) // 63
        
        if w == 0 and z in range(0,4):
            board[cell_piece[1]][cell_piece[2]] = None
            if 'bl' in cell_piece[0]:
                board[y][x] = options[z] +  'bl'
            elif 'wh' in cell_piece[0]:
                board[y][x] = options[z] + 'wh'
                
            click_position = ""
            cell_piece = [None]*3
            page = 'home'


def is_legal(x, y, kill):
    """
    This function will determine whether the movement is legal or not
    """
    global page
    
    if 'king' in cell_piece[0]:
        return ((cell_piece[2] == x+1 or cell_piece[2] == x-1) and cell_piece[1] == y) or (cell_piece[2] == x and (cell_piece[1] == y+1 or cell_piece[1] == y-1)) or (cell_piece[1] == y+1 and cell_piece[2] == x+1) or (cell_piece[1] == y+1 and cell_piece[2] == x-1) or (cell_piece[1] == y-1 and cell_piece[2] == x+1) or (cell_piece[1] == y-1 and cell_piece[2] == x-1)
    
    elif 'queen' in cell_piece[0]:
        diff = abs(cell_piece[1] - y)
        if cell_piece[1] == y+diff and cell_piece[2] == x+diff:
            for i in range(1, diff):
                if board[cell_piece[1]+(i-diff)][cell_piece[2]+(i-diff)] != None:
                    return False
            return True
        elif cell_piece[1] == y+diff and cell_piece[2] == x-diff:
            for i in range(1, diff):
                if board[cell_piece[1]+(i-diff)][cell_piece[2]-(i-diff)] != None:
                    return False
            return True
        elif cell_piece[1] == y-diff and cell_piece[2] == x+diff:
            for i in range(1, diff):
                if board[cell_piece[1]-(i-diff)][cell_piece[2]+(i-diff)] != None:
                    return False
            return True
        elif cell_piece[1] == y-diff and cell_piece[2] == x-diff:
            for i in range(1, diff):
                if board[cell_piece[1]-(i-diff)][cell_piece[2]-(i-diff)] != None:
                    return False
            return True
        elif cell_piece[2] == x:
            if cell_piece[1] > y:
                for i in range(y+1, cell_piece[1]):
                    if board[i][x] != None:
                        return False
                return True
            elif cell_piece[1] < y:
                for i in range(cell_piece[1]+1, y):
                    if board[i][x] != None:
                        return False
                return True
        elif cell_piece[1] == y:
            if cell_piece[2] > x:
                for i in range(x+1, cell_piece[2]):
                    if board[y][i] != None:
                        return False
                return True
            if cell_piece[2] < x:
                for i in range(cell_piece[2]+1, x):
                    if board[y][i] != None:
                        return False
                return True
        
    elif 'knight' in cell_piece[0]:
        return (cell_piece[2] == x-2 and cell_piece[1] == y+1) or (cell_piece[2] == x-1 and cell_piece[1] == y+2) or (cell_piece[2] == x+1 and cell_piece[1] == y+2) or (cell_piece[2] == x+2 and cell_piece[1] == y+1) or (cell_piece[2] == x+2 and cell_piece[1] == y-1) or (cell_piece[2] == x+1 and cell_piece[1] == y-2) or (cell_piece[2] == x-1 and cell_piece[1] == y-2) or (cell_piece[2] == x-2 and cell_piece[1] == y-1)
    
    elif 'bishop' in cell_piece[0]:
        diff = abs(cell_piece[1] - y)       
        if cell_piece[1] == y+diff and cell_piece[2] == x+diff:
            for i in range(1, diff):
                if board[cell_piece[1]+(i-diff)][cell_piece[2]+(i-diff)] != None:
                    return False
            return True
        elif cell_piece[1] == y+diff and cell_piece[2] == x-diff:
            for i in range(1, diff):
                if board[cell_piece[1]+(i-diff)][cell_piece[2]-(i-diff)] != None:
                    return False
            return True
        elif cell_piece[1] == y-diff and cell_piece[2] == x+diff:
            for i in range(1, diff):
                if board[cell_piece[1]-(i-diff)][cell_piece[2]+(i-diff)] != None:
                    return False
            return True
        elif cell_piece[1] == y-diff and cell_piece[2] == x-diff:
            for i in range(1, diff):
                if board[cell_piece[1]-(i-diff)][cell_piece[2]-(i-diff)] != None:
                    return False
            return True

    elif 'rook' in cell_piece[0]:
        if cell_piece[2] == x:
            if cell_piece[1] > y:
                for i in range(y+1, cell_piece[1]):
                    if board[i][x] != None:
                        return False
                return True
            elif cell_piece[1] < y:
                for i in range(cell_piece[1]+1, y):
                    if board[i][x] != None:
                        return False
                return True
        elif cell_piece[1] == y:
            if cell_piece[2] > x:
                for i in range(x+1, cell_piece[2]):
                    if board[y][i] != None:
                        return False
                return True
            if cell_piece[2] < x:
                for i in range(cell_piece[2]+1, x):
                    if board[y][i] != None:
                        return False
                return True
            
    elif 'pawn' in cell_piece[0]:
        if 'b' in cell_piece[0]:
            if kill:
                if (cell_piece[2] == x+1 and cell_piece[1] == y-1) or (cell_piece[2] == x-1 and cell_piece[1 == y-1]):
                    if y == 7:
                        page = 'options'
                        #return True
                    else:
                        return True
            else:
                if cell_piece[1] == 1:
                    if cell_piece[2] == x and cell_piece[1] == y-1:
                        return True
                    elif cell_piece[2] == x and cell_piece[1] == y-2:
                        return board[2][x] == None
                else:
                    if cell_piece[2] == x and cell_piece[1] == y-1:
                        if y == 7:
                            page = 'options'
                            #return True
                        else:
                            return True
        elif 'w' in cell_piece[0]:
            if kill:
                if (cell_piece[2] == x+1 and cell_piece[1] == y+1) or (cell_piece[2] == x-1 and cell_piece[1 == y+1]):
                    if not 'king' in board[y][x]:
                        if y == 0:
                            page = 'options'

                    return True
            else:
                if cell_piece[1] == 6:
                    if cell_piece[2] == x and cell_piece[1] == y+1:
                        return True
                    elif cell_piece[2] == x and cell_piece[1] == y+2:
                        return board[5][x] == None
                else:
                    if cell_piece[2] == x and cell_piece[1] == y+1:
                        if y == 0:
                            page = 'options'
                            #return True
                        else:
                            return True

    return False


def show_options():
    """
    This function will show the different option to choose
    when a pawn gets to the last cell
    """
    # Sentence
    title_font = pygame.font.SysFont('times new roman', 24)
    title_surface = title_font.render('Choose what your pawn will become:', True, black)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (frame_size_x/2, frame_size_y/4)
    
    # Background color
    game_window.fill(background_color)
    
    # Rectangle
    pygame.draw.polygon(game_window, light_brown, [(234,252), (486,252), (486,315), (234,315)])
    
    # Options
    if 'bl' in cell_piece[0]:
        color = black
    elif 'wh' in cell_piece[0]:
        color = white
    
    for i in range(len(options)):
        fill(option_img[i], color)
        game_window.blit(option_img[i], (239+63*i,257))
    
    game_window.blit(title_surface, title_rect)
    pygame.display.flip()
    


def initial_page():
    """
    This function will show the initial page of the game where the player
    will choose between single-player, two-player or online mode.
    """
    # Title
    title_font = pygame.font.SysFont('times new roman', 90)
    title_surface = title_font.render('CHESS.COM', True, black)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (frame_size_x/2, frame_size_y/4)
    
    # Subtitle
    sub_font = pygame.font.SysFont('times new roman', 24)
    sub_surface = sub_font.render('Press B to start', True, grey)
    sub_rect = sub_surface.get_rect()
    sub_rect.midtop = (frame_size_x/2, frame_size_y/2)
    
    # Show in the screen
    game_window.fill(background_color)
    game_window.blit(title_surface, title_rect)
    game_window.blit(sub_surface, sub_rect)
    pygame.display.flip() 
    


def game_over():
    """
    This function will show the game over page where the player
    will decide whether or not to continue playing.
    """
    # Game Over
    title_font = pygame.font.SysFont('times new roman', 90)
    if winner != 'draw':
        title_surface = title_font.render(winner + ' WIN!', True, black)
    elif winner == 'draw':
        title_surface = title_font.render('DRAW!', True, black)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (frame_size_x/2, frame_size_y/4)
    
    sub_font = pygame.font.SysFont('times new roman', 24)
    sub_surface = sub_font.render('Press B to show the board', True, grey)
    sub_rect = sub_surface.get_rect()
    sub_rect.midtop = (frame_size_x/2, frame_size_y/2)
    
    res_font = pygame.font.SysFont('times new roman', 24)
    res_surface = res_font.render('Press R to play again', True, grey)
    res_rect = res_surface.get_rect()
    res_rect.midtop = (frame_size_x/2, frame_size_y*2.3/4)
    
    game_window.fill(background_color)
    game_window.blit(title_surface, title_rect)
    game_window.blit(sub_surface, sub_rect)
    game_window.blit(res_surface, res_rect)
    pygame.display.flip()


while True:
    
    if page == 'initial':
        initial_page()
    elif page == 'home':
        main()
    elif page == 'options':
        show_options()
    elif page == 'over':
        game_over()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('\n[+] Thanks for playing! Have a nice day!')
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if page == 'over':
                if event.key == ord('r'):
                    page = 'home'
                    game_status = 'initial'
                elif event.key == ord('b'):
                    page = 'home'
                    game_status = 'ended'
            elif page == 'initial':
                if event.key == ord('b'):
                    page = 'home'
            
            if event.key == ord('r'):
                cell_piece = [None]*3
                turn = 'whites'
                game_status = 'initial'
                page = 'home'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            user_click()

