import PySimpleGUI as sg
import sqlite3
import time

killer_list = ['Trapper', 'Wraith', 'Hillbilly', 'Nurse', 'Shape', 'Hag', 'Doctor', 'Huntress', 'Cannibal', 'Nightmare', 'Pig', 'Clown', 'Spirit', 'Legion', 'Plague', 'Ghost Face', 'Demogorgon', 'Oni', 'Deathslinger', 'Executioner', 'Blight', 'Twins', 'Trickster', 'Nemesis', 'Cenobite', 'Artist', 'Onryo', 'Dredge', 'Mastermind', 'Knight']

conn = sqlite3.connect('game_data.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS game_data (
                GameID INTEGER PRIMARY KEY,
                Killer TEXT NOT NULL,
                Time REAL NOT NULL,
                Kills INTEGER NOT NULL,
                Result TEXT NOT NULL
            )''')

conn.commit()

conn.close()

font_size = 25
font_family = 'Fredoka One'

sg.theme_element_text_color('#996888')
sg.theme('Reddit')

def radio():
    
    conn = sqlite3.connect('game_data.db')

    cursor = conn.cursor()

    radio_layout = [
        [sg.Radio(text='0 KILLS', group_id = 'RADIO', key='0', font=(font_family, font_size - 4), enable_events=True)],
        [sg.Radio(text='1 KILL', group_id = 'RADIO', key='1', font=(font_family, font_size - 4), enable_events=True)],
        [sg.Radio(text='2 KILLS', group_id = 'RADIO', key='2', font=(font_family, font_size - 4), enable_events=True)],
        [sg.Radio(text='3 KILLS', group_id = 'RADIO', key='3', font=(font_family, font_size - 4), enable_events=True)],
        [sg.Radio(text='4 KILLS', group_id = 'RADIO', key='4', font=(font_family, font_size - 4), enable_events=True)],
        ]

    button_lay = [[sg.Button(button_text='Done!', size=(0, 5),enable_events=True, font=(font_family, font_size))]]
    radio_end = [[sg.Text(text=' ')],
                [sg.Column(radio_layout, element_justification='left'), sg.Column(button_lay, element_justification='center')]
                ]

    radio_window = sg.Window('How many kills you have?', radio_end, icon='icon.ico' ,keep_on_top=True, size=(310,330))
    while True:
        event, values = radio_window.read()
        if event in (sg.WIN_CLOSED, 'Cancel') or event == 'Done!':
            if values['1'] == True:
                kills = 1
                result = 'LOSE'
            elif values['2'] == True:
                kills = 2
                result = 'LOSE'
            elif values['3'] == True:
                kills = 3
                result = 'WIN'
            elif values['4'] == True:
                kills = 4
                result = 'WIN'
            elif values['0'] == True:
                kills = 0
                result = 'LOSE'
            radio_window.close()
            cursor.execute('INSERT INTO game_data (killer, time, kills, result) VALUES (?, ?, ?, ?)', (killer, timeGame, kills, result))
            conn.commit()
            conn.close()
            main()
            break

def timer():

    Bebebe = True
    start_time = None
    elapsed_time = 0

    start_time = time.time()  
    timer_layout = [
            [sg.Text(text='00:00:00', key='TIMER', font=(font_family, font_size))],
            [sg.Button(button_text='Stop', key='STOP', enable_events=True, font=(font_family, font_size - 2))]
            ]
    timer_window = sg.Window('...', timer_layout, location=(-2,0), icon='icon.ico' ,keep_on_top=Bebebe, element_justification='center' ,size=(180,150))
    while True:
        event, values = timer_window.read(timeout=100)
        if event == 'STOP' or event == sg.WIN_CLOSED:
            elapsed_time = time.time() - start_time 
            global timeGame
            timeGame = elapsed_time
            timer_window.close()
            radio()
            break      
        else:
            Bebebe = True
            elapsed_seconds = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed_seconds, 60)
            timer_window['TIMER'].update('{:02d}:{:02d}'.format(minutes, seconds))

def main():
    layout = [
        [sg.Text(' ')],
        [sg.Text(text="Dead by Daylight Base", font=(font_family, font_size))],
        [sg.Text(' ')],
        [sg.Combo(values=killer_list, size=(12,12) ,key='KILLER' ,default_value=killer_list[0], readonly=True, font=(font_family, font_size))],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button(button_text='Base', size=(13,10),key='BASE' , enable_events=True, font=(font_family, font_size)), sg.Button(button_text='Start!', size=(30,10) ,key='START' , enable_events=True, font=(font_family, font_size))]
    ]

    window = sg.Window('DeadbyDaylight Base', layout ,element_justification='center', icon='icon.ico',size=(600,300))

    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT killer FROM game_data")
    info = cursor.fetchall()

    while True:
        event, values = window.read()
        if event == 'START':
            global killer
            killer = values["KILLER"]
            window.close()
            time.sleep(0.3)
            timer()
        if event == 'BASE' and len(info) <= 0:
            print('Error!')
        if event == 'BASE' and len(info) > 0:
            conn.close()
            window.close()
            base()
        elif event in (sg.WIN_CLOSED, 'Cancel'):
            break
        
    window.close()

def base():

    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    #last game
    cursor.execute("SELECT killer FROM game_data ORDER BY killer DESC LIMIT 5")
    killer_base5 = cursor.fetchone()

    cursor.execute("SELECT time FROM game_data ORDER BY time DESC LIMIT 5")
    timeOfGame5 = cursor.fetchone()

    cursor.execute("SELECT kills FROM game_data ORDER BY kills DESC LIMIT 5")
    killsGame5 = cursor.fetchone()

    #sum games
    cursor.execute('SELECT GameID FROM game_data ORDER BY GameID DESC LIMIT 1;')
    games = cursor.fetchone()

    #popular killer
    cursor.execute('SELECT Killer, COUNT(Killer) AS KillerCount FROM game_data GROUP BY Killer ORDER BY KillerCount DESC LIMIT 1')
    popularKiller = cursor.fetchone()

    #average time
    cursor.execute('SELECT AVG(Time) FROM game_data')
    averageTime = cursor.fetchone()

    #sumtime
    cursor.execute('SELECT SUM(time) FROM game_data')
    sum_time = cursor.fetchone()

    total_minutes = int(sum_time[0]) / 60

    hours2 = int(total_minutes / 60)
    minutes2 = int(total_minutes % 60)
    seconds = int(int(sum_time[0]) % 60)

    sumTime = "{:02d}:{:02d}:{:02d}".format(hours2, minutes2, seconds)

    #average kills
    cursor.execute("SELECT SUM(Kills) FROM game_data")
    total_kills = cursor.fetchone()[0]

    # Get the number of rows in the table
    cursor.execute("SELECT COUNT(*) FROM game_data")
    num_rows = cursor.fetchone()[0]

    # Calculate the average kills
    average_kills = total_kills / num_rows

    #winrate
    cursor.execute('''
    SELECT Result, COUNT(Result)
    FROM game_data
    GROUP BY Result
                    ''')
    
    winrate = cursor.fetchall()

    wins = 0
    cursor.execute("SELECT COUNT(*) FROM game_data WHERE Result='WIN'",)
    wins = cursor.fetchone()[0]

    minutes, seconds = divmod(int(averageTime[0]), 60)
    averageTimeShow = '{:02d}:{:02d}'.format(minutes, seconds)

    for result in winrate:
        if result[0] == 'WIN':
            wins = result[1]
        elif result[0] == 'LOSE':
            losses = result[1]

    name_column = [
                   [sg.Text(text='Statistics', font=(font_family, font_size + 4))]
                  ]

    general_column = [ 
                [sg.Text(' ', size=(30,0))],
                [sg.Text(text='General' ,font=(font_family, font_size + 2))],
                [sg.Text(text=f'Played games: {games[0]}', font=(font_family, font_size - 8))],
                [sg.Text(text=f'Popular killer: {popularKiller[0]}', font=(font_family, font_size - 8))],
                [sg.Text(text=f'Time in game: {sumTime}', font=(font_family, font_size - 8))],
                     ]
    
    average_cloumn = [ 
                [sg.Text(' ', size=(30,0))],
                [sg.Text(text='Average value' ,font=(font_family, font_size + 2))],
                [sg.Text(text=f'Game time: {averageTimeShow}', font=(font_family, font_size - 8))],
                [sg.Text(text=f'Kills: {average_kills:.0f}', font=(font_family, font_size - 8))],
                [sg.Text(text=f'Win rate: {(wins/games[0])*100:.0f}%', font=(font_family, font_size - 8))],
                     ]

    each_killer = [
                  [sg.Text(' ', size=(30,2))],
                  [sg.Text(text=f'Games: 0', font=(font_family, font_size - 8), key = 'KILLER_GAMES', enable_events=True)],
                  [sg.Text(text=f'Win rate: 0%', font=(font_family, font_size - 8), key='WINRATE')],
                  [sg.Text(text=f'Average kills: 0 ', font=(font_family, font_size - 8), key='AVGKILL')],
                  [sg.Text(text=f'Average time: 00:00', font=(font_family, font_size - 8), key='AVGTIME')]
                  ]

    comboKiller = [ [sg.Text(' ', size=(10,0))],
                    [sg.Text('Killer',font=(font_family, font_size + 2))],
                    [sg.Text(text=' ', size=(20, 0))],
                    [sg.Text(text='Choosen killer: ', font=(font_family, font_size - 8))],[sg.Combo(values=killer_list, default_value='...', readonly=True, enable_events=True, key='KILLER_STAT', font=(font_family, font_size - 8))]]
 

    base_layout = [[sg.Column(name_column, element_justification='center')],
                  [sg.Column(general_column, element_justification='left'), sg.Column(average_cloumn, element_justification='left')],
                  [sg.Column(comboKiller, element_justification='left'), sg.Column(each_killer, element_justification='left') ],
                  [sg.Button(button_text='Menu', size=(13,0),key='MENU' , enable_events=True, font=(font_family, font_size - 4)),sg.Button(button_text='Last', size=(13,0),key='LAST' , enable_events=True, font=(font_family, font_size - 4)) ,sg.Button(button_text='Remove All', size=(17,2),key='REMOVE' , enable_events=True, font=(font_family, font_size - 12))]
                  ]

    base_window = sg.Window('Statistics', base_layout, size=(640,530), icon='icon.ico', finalize=True)

    base_window['KILLER_GAMES'].update(value=f'Games: ?')
    base_window['WINRATE'].update(value=f'Win rate: ?%')
    base_window['AVGKILL'].update(value=f'Average kills: ?')
    base_window['AVGTIME'].update(value=f'Average time: ?')


    while True:
        event, values = base_window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'LAST':
            conn = sqlite3.connect('game_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM game_data ORDER BY GameID DESC LIMIT 1")
            row = cursor.fetchone()
            sg.popup(f' Last game: \n Killer: {row[1]} \n Time: {int(int(row[2])/60)}:{int(row[2])} \n Result: {row[3]}, {row[4]}', grab_anywhere=True, font=(font_family, font_size - 4), title='Last game')
        if event == 'KILLER_STAT':
            selected_killer = values['KILLER_STAT']
            cursor.execute("SELECT COUNT(*) FROM game_data WHERE Killer=?", (selected_killer,))
            games_played = cursor.fetchone()[0]
            if games_played is None:
                base_window['KILLER_GAMES'].update(value=f'Games: 0')
            else:
                base_window['KILLER_GAMES'].update(value=f'Games: {games_played}')
            cursor.execute("SELECT COUNT(*) FROM game_data WHERE Killer=? AND Result='WIN'", (selected_killer,))
            wins = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM game_data WHERE Killer=? AND Result='LOSE'", (selected_killer,))
            losses = cursor.fetchone()[0]
            if wins + losses == 0:
                base_window['WINRATE'].update(value=f'Win rate: 0%')
            else:
                winrate = (wins / (wins + losses)) * 100
                base_window['WINRATE'].update(value=f'Win rate: {winrate}%')
            cursor.execute("SELECT SUM(Kills) FROM game_data WHERE Killer=?", (selected_killer,))
            total_kills = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM game_data WHERE Killer=?", (selected_killer,))
            num_rows = cursor.fetchone()[0]
            if num_rows is None or total_kills is None or num_rows is None and total_kills is None:
                base_window['AVGKILL'].update(value=f'Average kills: 0')
            else:
                average_kills = total_kills / num_rows
                if int(average_kills) == 0:
                    base_window['AVGKILL'].update(value=f'Average kills: 0')
                else:
                    base_window['AVGKILL'].update(value=f'Average kills: {int(average_kills)}')
            cursor.execute("SELECT AVG(Time) FROM game_data WHERE Killer=?", (selected_killer,))
            avg_timeKiller = cursor.fetchone()[0]
            if avg_timeKiller is None:
                base_window['AVGTIME'].update(value=f'Average time: 00:00')
            else:
                minutes2, seconds2 = divmod(int(avg_timeKiller), 60)
                averageTimeShow2 = '{:02d}:{:02d}'.format(minutes2, seconds2)
                base_window['AVGTIME'].update(value=f'Average time: {averageTimeShow2}')
        if event == 'MENU':
            base_window.close()
            main()
        if event == 'REMOVE':
            base_window.close()
            conn = sqlite3.connect('game_data.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM game_data")
            conn.commit()
            conn.close()
            main()

    
    base_window.close()
    cursor.close()
    conn.close()

main()
