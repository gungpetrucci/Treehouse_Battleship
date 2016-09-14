import os



SHIP_INFO = [
    ("Aircraft Carrier", 5, "aircraft_carrier"),
    ("Battleship", 4, "battleship"),
    ("Submarine", 3, "submarine"),
    ("Cruiser", 3, "cruiser"),
    ("Patrol Boat", 2, "patrol_boat")
]



class Table():

    def __init__(self):
        self.columns = ['A','B','C','D','E','F','G','H','I','J']
        self.rows = ['1','2','3','4','5','6','7','8','9','10']
        self.position = []
        self.turn = []
        
        for row in self.rows:
            for column in self.columns:
                self.position.append(row + column)

    def clear(self):
        print('\033c', end='')

    def draw(self,player):
        rows = self.rows
        columns = self.columns
        
        print('   A B C D E F G H I J')
        for row in rows:
            if row != '10':
                print(' ', end='')
                print(row, end=' ')
            else:
                print(row, end=' ')
            for column in columns:
                check_location = row + column

                status = False
            
                for ship in player.fleet:
                    
                    if check_location in ship.hit_location:
                        if ship.status == 'live':
                            status = 'hit'
                            print('*', end=' ')
                            break
                        else:
                            print('#', end=' ')
                            status = 'sunk'
                            break
                    elif check_location in ship.location:
                        if ship.orientation == 'v':
                            status = 'v'
                            if player == game.turn:
                                print('|', end=' ')
                                break
                            else:
                                print('0', end=' ')
                                break
                        else:
                            status = 'h'
                            if player == game.turn:
                                print('-', end=' ')
                                break
                            else:
                                print('0', end=' ')
                                break
                    elif check_location in player.missed_location:
                        status = 'missed'
                        print('.', end=' ')
                        break
                    
                if status == False:
                    print('0', end=' ')
    
            print('\n')

    def draw_screen(self):
        self.clear()
        print(' Player 1: {}'.format(player_1.name))
        self.draw(player_1)
        print(' Player 2: {}'.format(player_2.name))
        self.draw(player_2)
        print('\n\n')
                        
                        
                        
                        
                
    

class Player():

    def __init__(self):
 
        self.name = ' '
        self.ship_placement_location = []
        self.missed_location = []
        self.hit_location = []
        self.aircraft_carrier = Ship('Aircraft Carrier', 5)
        self.battleship = Ship('Battleship', 4)
        self.submarine = Ship('Submarine', 3)
        self.cruiser = Ship('Cruiser', 3)
        self.patrol_boat = Ship('Patrol Boat', 2)
        self.fleet = [self.aircraft_carrier, self.battleship, self.submarine, self.cruiser,self.patrol_boat]

    def check_valid_position(self, enemy):

        valid_position = False

        while valid_position == False:
            answer = input("{}, Please select {}'s target location to shoot: ".format(self.name, enemy.name))
            answer = answer.replace(' ','')

            try:
                if len(answer) not in [2, 3]:
                    print('Your Location is INVALID!')
                    continue
                
                if len(answer) == 2:
                    answer_x = int(answer[0:1])
                    answer_y = answer[1:2].upper()
                else:
                    answer_x = int(answer[0:2])
                    answer_y = answer[2:3].upper()

                if str(answer_x) not in game.rows or answer_y not in game.columns:
                    print('You Given Location are not in the Table!')
                    continue

                return answer
                
            except ValueError:
                print('INVALID Location: Please enter row(number) follow by column(letter)')
                continue
        
    def get_name(self):
        game.turn = self
        self.name = input('Please Enter Your Name: ')

    def turn(self):
        game.turn = self
        game.draw_screen()
        print("{}'s Turn".format(self.name))
        
        if self == player_1:
            enemy = player_2
        else:
            enemy = player_1
            
        self.shoot(enemy)
        self.check_win(enemy)
        input('Press Enter to finish your turn...')

    def shoot(self, enemy):
        
        valid_position = False
        
        while valid_position == False:
            answer = self.check_valid_position(enemy)
            answer = answer.upper()
            if answer in enemy.missed_location or answer in enemy.hit_location:
                game.draw_screen()
                print('{}, you already shooted to this position, Try again new position'.format(self.name))
                continue
            valid_position = True

        hit_success = False

        for ship in enemy.fleet:
            if answer in ship.location:
                ship.location.remove(answer)
                ship.hit_location.append(answer)
                enemy.hit_location.append(answer)
                ship_status = ship.check_status()
                hit_success = True
                break
            else:
                pass

        if hit_success == False:
            enemy.missed_location.append(answer)
            game.draw_screen()
            print('Sorry {}, You missed.'.format(self.name))
            
        else:
            game.draw_screen()
            print("HIT !!! {} has succesfully hit {}'s ship!!".format(self.name, enemy.name))
            if ship_status == 'dead':
                print("{}'s ship has been destroy".format(enemy.name))
                ship_status = []
            
        


    def check_win(self, enemy):

        self.win = True
        
        for ship in enemy.fleet:
            if ship.status == 'live':
                self.win = False
                break

        if self.win == True:
            print(' CONGRATULATION ! YOU WIN!')
            print('{} HAVE DESTROY ALL OF {} FLEET'.format(self.name, enemy.name))
            exit()
                      
                
                
                
                
            


        
        
        
        
        
            
        
               

class Ship():

    def __init__(self, ship_type, length):
        self.status = 'live'
        self.hit_location = []
        self.location = []
        self.orientation = []
        self.ship_type = ship_type
        self.length = length

    def check_status(self):
        if self.location == []:
            self.status = 'dead'
            return 'dead'


    def ship_placement(self, player):
        valid_position = False

        while valid_position == False:
            
            answer = input('{}, Please Enter Your {} Location ({} Block required: '.format(player.name, self.ship_type, self.length))
            answer = answer.replace(' ','')

            try:
                if len(answer) not in [2, 3]:
                    print('Your Location is INVALID!')
                    continue
            
                if len(answer) == 2:
                    answer_x = int(answer[0:1])
                    answer_y = answer[1:2].upper()
                else:
                    answer_x = int(answer[0:2])
                    answer_y = answer[2:3].upper()

                if str(answer_x) not in game.rows or answer_y not in game.columns:
                    print('You Given Location are not in the Table!')
                    continue
            except ValueError:
                print('INVALID Location: Please enter row(number) follow by column(letter)')
                continue
                          

            self.orientation = input('Place the ship [V]ertical or [H]orizontal?: ').lower()

            if self.orientation not in 'vh':
                print('Enter only[V] for Vertical Placement [H] for Horizontal Placement!')
                continue
            if self.orientation == 'v':
                if int(answer_x) + (self.length-1) > 10:
                    print('Out of table!, Your {} is too long for that position. It require {} block!'.format(self.ship_type, self.length))
                    continue
            if self.orientation == 'h':
                if game.columns.index(answer_y) + (self.length-1) > 9:
                    print('Out of table!, Your {} is too long for that position. It require {} block!'.format(self.ship_type, self.length))
                    continue
                
            original_answer = answer
            temp_position = []
            temp_index = []
            collide = False
            
            for i in range(self.length):
                
                if self.orientation== 'v':
                    temp_position.append(str(answer_x) + answer_y)
                    answer_x += 1
                else:
                    temp_position.append(str(answer_x) + answer_y)
                    temp_index = game.columns.index(answer_y)
                    if temp_index < 9:
                        answer_y = game.columns[temp_index + 1]

            for position in temp_position:
                if position in player.ship_placement_location:
                    print('Some part of your ship location are alredy occipied by other ship!')
                    collide = True
                    break
                
            if collide == False:
                for position in temp_position:
                    self.location.append(position)
                    player.ship_placement_location.append(position)
                    
                valid_position = True
                        
                            

                    
                
            
        
        



            





#Main fucntion
    # PREP GAME
        # draw empty board
        # ask for player1 name
        # ask first player to place all ship/Validate
        # ask for player2 name
        # ask second plater to place all ship/ Validate
    
    
    # START GAME
        # Allow players to take turn, ask name and press enter when ready
        # ask for guess input
        # validate guess input
        # draw updated table
        # announce result str
        # check for winner
    

game = Table()
player_1 = Player()
player_2 = Player()
game.draw_screen()

print('WELCOME TO BATTLESHIP GAME. YOU ARE PLAYER 1 ')
player_1.get_name()
for ship in player_1.fleet:
    game.draw_screen()
    ship.ship_placement(player_1)
game.draw_screen()
input('Press Enter to finish your ship placement...')
game.turn = []
game.draw_screen()
    
print('WELCOME TO BATTLESHIP GAME. YOU ARE PLAYER 2 ')
player_2.get_name()
for ship in player_2.fleet:
    game.draw_screen()
    ship.ship_placement(player_2)
game.draw_screen()
input('Press Enter to finish your ship placement...')

game.turn = []
game.draw_screen()
print('BATTLESHIP GAME HAS BEGUN')
input('Press Enter to Begin the Battle! {} will take first turn'.format(player_1.name))
    
turn_count = 1

while True:
    print('TURN {}'.format(turn_count))
    player_1.turn()
    player_2.turn()
    turn_count += 1





