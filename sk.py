#! /usr/bin/python
 #--------------------
# WCL Scorekeeper 0.7
# By Erik N8MJK
#--------------------

import curses
import random
import signal
import time

# Import settings and globals
from caravans import *

# Display splash screen
def splash(win):
    win.clear()
    print "\n\r                      .A.                             mMm\n\r                     .MMM.                         .m.MMM.m.\n\r                    ,MMMMM.                        MMMMMMMLM\n\r                    'm\"I\"m'                         '\"TIT\"'\n\r                      .L.                             .L.\n\r\n\r                    \"TMMF  ,m   TMMF\"    nM\"M.T    TMMF\n\r                      TM   MM    TM'    iM' 'WM     MM\n\r                      IM. ,N'M  .IN    .MI   MM     nM\n\r                      'Mi M' M. iM'    iMl          MM\n\r                       TMiM   MiMT     'MI          Mm   I\n\r                       'Mi'   'NM'      lM. .MM     MM.  M\n\r                        MM     MM        'MmMT'    nMMTmMM\n\r\n\r                    .m. .m.                           .A.\n\r                    MMMMMMM                          ,AMA.\n\r                    'MMMMM'                         .AMMMD.\n\r                     'MMM'                           'VMV'\n\r                      'V'                             'V'\n\r"
    time.sleep(2)

# Empty the screen and redraw the top banner
def basic_screen_init(win,mode):
    win.clear()
    win.addstr(0,0,topstring,curses.A_REVERSE)
    if mode == 1:
        for y in range(c11y,c11y + 15):
            win.addstr(y,c12x - 2,"|")
            win.addstr(y,c13x - 2,"|")
    win.refresh()

# Ask the ref to log in
def login_screen(win):
    reflogin = ""
    refpass = ""
    basic_screen_init(win,0)
    win.addstr(2,0,"REFEREE LOGIN")
    win.addstr(4,1,"Login : ")
    reflogin = win.getstr(4,9,32)
    win.addstr(5,1,"Pass  : ")
    curses.noecho()
    win.nodelay(0)
    refpass = win.getstr(5,9,32)
    curses.echo()
    if refpass != masterpass:
        win.addstr(7,0,"Invalid password, sorry...")    
        win.refresh()
        time.sleep(2)
        return False
    else:
        win.addstr(7,0,"Password accepted, welcome %s!" % reflogin)    
        win.refresh()
        time.sleep(2)
        return True

# Enter players, seat and verify decks
def setup_screen(win):
    activeplayer = 0
    turn1 = 0
    turn2 = 0
    players = ["","Aboo","Baloo"]
    return players
#    players = ["","",""]

    basic_screen_init(win,0)
    curses.echo()
    win.nodelay(0)
    win.addstr(2,0,"SELECT AND SEAT PLAYERS")    
    win.addstr(4,1,"Player Name : ")
    name1 = win.getstr(4,15,32)
    win.addstr(5,1,"Player Name : ")
    name2 = win.getstr(5,15,32)

    prand = random.randint(1,2)
    if prand == 1:
        p1 = name1
        p2 = name2
    else:
        p1 = name2
        p2 = name1

    if name1 == "" or name2 == "":
        win.addstr(6,0,"You seem to have missed a name...")    
        win.refresh()
        time.sleep(2)
        return False
    else:
        win.addstr(7,0,"Please seat %s as Player 1 and %s as Player 2" % (p1,p2))
        win.addstr(8,0,"Verify with Y when Players are seated...")
        win.addstr(10,1,"(Y)es / (C)ancel")
        players[1] = p1
        players[2] = p2
        win.refresh()
        curses.noecho()
        while 1:
            c = win.getkey(10,18)
            if c.upper() == "Y":
               win.addstr(12,1,"Verify that both Players have valid decks...")
               win.addstr(14,1,"(Y)es / (C)ancel")
               while 1:
                   c = win.getkey(14,18)
                   if c.upper() == "Y":
                       return players
                   if c.upper() == "C":
                       return False
            if c.upper() == "C":
                return False

def numcard(card):
    cardt = str(card)
    if len(cardt) < 2:
        return False
    if card[0].isdigit():
        if int(card[0]) >= 0 and int(card[0]) < 10:
            if card[1].upper() == "S" or card[1].upper() == "C" or card[1].upper() == "H" or card[1].upper() == "D":
                return True
    return False

def validcard(card):
    if card.upper() == "JJ":
        return True
    if numcard(card):
        return True
    if card[0].upper() == "J" or card[0].upper() == "Q" or card[0].upper() == "K":
        if card[1].upper() == "S" or card[1].upper() == "C" or card[1].upper() == "H" or card[1].upper() == "D":
            return True 
    return False

def facecard(card):
    if card.upper() == "JJ":
        return True
    if card[0].upper() == "J" or card[0].upper() == "Q" or card[0].upper() == "K":
        if card[1].upper() == "S" or card[1].upper() == "C" or card[1].upper() == "H" or card[1].upper() == "D":
            return True 
    return False

def sum_caravan(caravan):
    csum = 0
    for row in caravan:
        if row[0] == 0:
            break
        rval = 0
        for val in row:
            if val == 0:
                break
            else:
                if val[0].isdigit():
                    if val[0] == "0":
                        rval = 10
                    else:
                        rval = int(val[0])
                if val[0] == "K":
                        rval = rval * 2
        csum = csum + rval
    return csum

def addn_caravan(caravan):
    rown = 0
    for row in caravan:
        if row[0] == 0:
            return rown
        rown = rown + 1

def caravan_sit(caravan):
    row1 = 0
    row2 = 0
    dir = "-"
    suit = "N"
    for row in caravan:
        if row[0] == 0:
            break
        else:
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0].isdigit():
                        row1 = row2
                        if val[0] == "0":
                            row2 = 10
                        else:
                            row2 = val[0]
                        suit = val[1]
    if int(row2) > int(row1):
        dir = "^"
    if int(row2) < int(row1):
        dir = "v"
    if row1 == 0:
        dir = "-"
    out = dir + suit
    return out,row2

def draw_caravans(win):
    c11s,lastcard11 = caravan_sit(c11)
    c21s,lastcard21 = caravan_sit(c21)
    c12s,lastcard12 = caravan_sit(c12)
    c22s,lastcard22 = caravan_sit(c22)
    c13s,lastcard13 = caravan_sit(c13)
    c23s,lastcard23 = caravan_sit(c23)

    sumc11 = str(sum_caravan(c11)).zfill(2)
    sumc21 = str(sum_caravan(c21)).zfill(2)
    sumc12 = str(sum_caravan(c12)).zfill(2)
    sumc22 = str(sum_caravan(c22)).zfill(2)
    sumc13 = str(sum_caravan(c13)).zfill(2)
    sumc23 = str(sum_caravan(c23)).zfill(2)

    diff1 = "="
    win11 = int(sumc11)
    win21 = int(sumc21)
    if win11 > 26:
        win11 = 0 
    if win21 > 26:
        win21 = 0 
    if win11 > win21:
        diff1 = ">"
    if win11 < win21:
        diff1 = "<"

    diff2 = "="
    win12 = int(sumc12)
    win22 = int(sumc22)
    if win12 > 26:
        win12 = 0 
    if win22 > 26:
        win22 = 0 
    if win12 > win22:
        diff2 = ">"
    if win12 < win22:
        diff2 = "<"

    diff3 = "="
    win13 = int(sumc13)
    win23 = int(sumc23)
    if win13 > 26:
        win13 = 0 
    if win23 > 26:
        win23 = 0 
    if win13 > win23:
        diff3 = ">"
    if win13 < win23:
        diff3 = "<"

    win.addstr(c11y - 1,c11x,"P1C1%s %s " % (c11s,lastcard11))
    win.addstr(c11y - 2,c11x + 5,"%s%s" % (sumc11,diff1),curses.A_BOLD)
    win.addstr(c21y - 1,c21x,"P2C1%s %s" % (c21s,lastcard21))
    win.addstr(c21y - 2,c21x - 2,"%s" % sumc21,curses.A_BOLD)
    win.addstr(c12y - 1,c12x,"P1C2%s %s" % (c12s,lastcard12))
    win.addstr(c12y - 2,c12x + 5,"%s%s" % (sumc12,diff2),curses.A_BOLD)
    win.addstr(c22y - 1,c22x,"P2C2%s %s" % (c22s,lastcard22))
    win.addstr(c22y - 2,c22x - 2,"%s" % sumc22,curses.A_BOLD)
    win.addstr(c13y - 1,c13x,"P1C3%s %s" % (c13s,lastcard13))
    win.addstr(c13y - 2,c13x + 5,"%s%s" % (sumc13,diff3),curses.A_BOLD)
    win.addstr(c23y - 1,c23x,"P2C3%s %s" % (c23s,lastcard23))
    win.addstr(c23y - 2,c23x - 2,"%s" % sumc23,curses.A_BOLD)
    for i in range(0,15):
        win.addstr(c11y + i,0,str(i + 1).zfill(2))
        win.addstr(c11y + i,c23x + 10,str(i + 1).zfill(2))
    rown = 0
    valn = 0
    for row in c11:
        if row[0] == 0:
            break
        else:
            rval = row[0]
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0] == "0":
                        win.addstr(c11y + rown,c11x + valn - 1,str(1))
                        win.addstr(str(val))
                    else:
                        win.addstr(c11y + rown,c11x + valn,str(val))                        
                    valn = valn + 2
        rown = rown + 1
        valn = 0

    rown = 0
    valn = 0
    for row in c21:
        if row[0] == 0:
            break
        else:
            rval = row[0]
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0] == "0":
                        win.addstr(c21y + rown,c21x + valn - 1,str(1))
                        win.addstr(str(val))
                    else:
                        win.addstr(c21y + rown,c21x + valn,str(val))                        
                    valn = valn + 2
        rown = rown + 1
        valn = 0

    rown = 0
    valn = 0
    for row in c12:
        if row[0] == 0:
            break
        else:
            rval = row[0]
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0] == "0":
                        win.addstr(c12y + rown,c12x + valn - 1,str(1))
                        win.addstr(str(val))
                    else:
                        win.addstr(c12y + rown,c12x + valn,str(val))                        
                    valn = valn + 2
        rown = rown + 1
        valn = 0

    rown = 0
    valn = 0
    for row in c22:
        if row[0] == 0:
            break
        else:
            rval = row[0]
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0] == "0":
                        win.addstr(c22y + rown,c22x + valn - 1,str(1))
                        win.addstr(str(val))
                    else:
                        win.addstr(c22y + rown,c22x + valn,str(val))                        
                    valn = valn + 2
        rown = rown + 1
        valn = 0

    rown = 0
    valn = 0
    for row in c13:
        if row[0] == 0:
            break
        else:
            rval = row[0]
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0] == "0":
                        win.addstr(c13y + rown,c13x + valn - 1,str(1))
                        win.addstr(str(val))
                    else:
                        win.addstr(c13y + rown,c13x + valn,str(val))                        
                    valn = valn + 2
        rown = rown + 1
        valn = 0

    rown = 0
    valn = 0
    for row in c23:
        if row[0] == 0:
            break
        else:
            rval = row[0]
            for val in row:
                if val == 0:
                    break
                else:
                    if val[0] == "0":
                        win.addstr(c23y + rown,c23x + valn - 1,str(1))
                        win.addstr(str(val))
                    else:
                        win.addstr(c23y + rown,c23x + valn,str(val))
                    valn = valn + 2
        rown = rown + 1
        valn = 0

def clearline(win,line):
    win.move(line,0)
    win.clrtoeol()

def prompt_card(win,pnum,players,turn):
    onum = 1
    if pnum == 1:
        onum = 2
    pname = players[pnum]
    oname = players[onum]
    curses.echo()
    card = False
    while card == False:
        if turn <= 3:
            win.addstr(cprompty,cpromptx,"Player %s (%s)" % (pnum,pname),curses.A_BOLD)
            win.addstr(cprompty + 1,cpromptx,"plays card to Caravan %s:    " % turn,curses.A_BOLD)
            input = win.getstr(cprompty + 1,cpromptx + 25,2)
            card = str(input)
            if card.upper() == "CC": #cancel game
                if promptyn(win,"Verify cancelling ENTIRE GAME...") == 2:
                    card = False
                return card
            if card.upper() == "DD": #discard
                if promptyn(win,"Verify " + pname + " wishes to discard...") == 2:
                    card = False
                return card

            if numcard(card):
                return card
        if turn > 3:
            win.addstr(cprompty,cpromptx,"Player %s (%s)" % (pnum,pname),curses.A_BOLD)
            win.addstr(cprompty + 1,cpromptx,"plays card :    ",curses.A_BOLD)
            input = win.getstr(cprompty + 1,cpromptx + 13,2)
            card = str(input)
            if card == "":
                card = False
                break
            if card.upper() == "C": #cancel
                if promptyn(win,"Verify cancelling " + pname + "'s move and reverting " + oname + "'s...") == 2:
                    card = False
                return card
            if card.upper() == "CC": #cancel game
                if promptyn(win,"Verify cancelling ENTIRE GAME...") == 2:
                    card = False
                return card
            if card[0].upper() == "D": #disband or discard
                if card[1].upper() == "D": #discard
                    if promptyn(win,"Verify " + pname + " wishes to discard...") == 2:
                        card = False
                    return card
                if int(card[1]) <= 3 and int(card[1]) > 0: #disband
                    if promptyn(win,"Verify " + pname + " wishes to disband Caravan " + card[1] + "...") == 2:
                        card = False
                    return card
        if turn > 3:
            if validcard(card):
                return card
    card = False
    return card

def playcard(win,card,cplay,activeplayer):
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    p = int(activeplayer)
    c = int(cplay)
    num = int(card[0])
    suit = card[1].upper()
    if num == 0:
        num = 10
    if p == 1 and c == 1:
        caravan = c11
    if p == 1 and c == 2:
        caravan = c12
    if p == 1 and c == 3:
        caravan = c13
    if p == 2 and c == 1:
        caravan = c21
    if p == 2 and c == 2:
        caravan = c22
    if p == 2 and c == 3:
        caravan = c23
    csit,lastcard = caravan_sit(caravan)
    if lastcard == 0 and numcard(card):
        return True
    if num == int(lastcard):
        return False
    if csit[0] == "-":
        return True
    if csit[0] == "^":
        if num > int(lastcard):
            return True
    if csit[0] == "v":
        if num < int(lastcard):
            return True
    if suit == csit[1].upper():
        return True
    return False

def playpos(player,caravan,pos,card):
    p = int(player)
    c = int(caravan)
    row = int(pos) - 1
    if p == 1 and c == 1:
        caravan = c11
    if p == 1 and c == 2:
        caravan = c12
    if p == 1 and c == 3:
        caravan = c13
    if p == 2 and c == 1:
        caravan = c21
    if p == 2 and c == 2:
        caravan = c22
    if p == 2 and c == 3:
        caravan = c23

    if caravan[row][0] == 0:
        return False
    else:
        numn = 0
        for num in caravan[row]:
            if num == 0:
                caravan[row][numn] = card.upper()
                return caravan
            numn = numn + 1
        return False

def prompt(win,string,val1,val2,val3=0,val4=0):
    outval = 0
    curses.noecho()
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    win.addstr(cprompty,cpromptx,string,curses.A_BOLD)
    win.addstr(cprompty + 1,cpromptx,"(1) %s / (2) %s" % (val1,val2))
    if val3 != 0:
        win.addstr(" / (3) %s" % val3)
    if val4 != 0:
        win.addstr(" / (4) %s" % val4)
    while outval == 0:
       c = win.getkey(cprompty,cpromptx + len(string) + 1)
       if c == "1":
           outval = 1
       if c == "2":
           outval = 2
       if val3 != 0:
           if c == "3":
               outval = 3
       if val4 != 0:
           if c == "4":
               outval = 4
    curses.echo()
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    return outval

def promptn(win,string,vals):
    outval = 0
    curses.noecho()
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    win.addstr(cprompty,cpromptx,string,curses.A_BOLD)
    if vals == 2:
        win.addstr(cprompty + 1,cpromptx,"(1) / (2)")
    if vals == 3:
        win.addstr(cprompty + 1,cpromptx,"(1) / (2) / (3)")
    if vals > 3:
        win.addstr(cprompty + 1,cpromptx,"(1) ... (%s)" % vals)
    while outval == 0:
       c = win.getkey(cprompty,cpromptx + len(string) + 1)
       if c.isdigit():
           if int(c) > 0 and int(c) <= vals:
               outval = c
    curses.echo()
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    return outval

def promptyn(win,string):
    outval = 0
    curses.noecho()
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    win.addstr(cprompty,cpromptx,string,curses.A_BOLD)
    win.addstr(cprompty + 1,cpromptx,"(Y)es / (N)o")
    while outval == 0:
       c = win.getkey(cprompty,cpromptx + len(string) + 1)
       if c.upper() == "Y" or c == "1":
           outval = 1
       if c.upper() == "N" or c == "2":
           outval = 2
    curses.echo()
    clearline(win,cprompty)
    clearline(win,cprompty + 1)
    return outval

def gameloop(win,players):
    outcome = "Incomplete"
    activeplayer = 1   
    turn1 = 0
    turn2 = 0
    cplay = 0

    global c11
    global c12
    global c13
    global c21
    global c22
    global c23

    while outcome == "Incomplete":
        basic_screen_init(win,1)
        draw_caravans(win)
        if activeplayer == 1:
            turn1 = turn1 + 1
            turn = turn1
        else:
            turn2 = turn2 + 1
            turn = turn2
        clearline(win,2)
        win.addstr(1,1,"%s (Player %s) >>> " % (players[activeplayer],str(activeplayer)),curses.A_BOLD)
        win.addstr("Turn %s" % str(turn)) #Display turn and player
        if turn <= 3:
            win.addstr(" - Start Caravans")
        else:
            win.addstr(" - Play Cards")
        win.refresh()
        draw_caravans(win)

        validplay = False
        while validplay == False:
            card = prompt_card(win,activeplayer,players,turn)
            if card != False:
                if card.upper() == "DD":
                    break
                if card[0].upper() == "D" and card[1].isdigit():
                    c = int(card[1])
                    if c > 0 and c <= 3:
                        p = activeplayer
                        if p == 1 and c == 1:
                            c11 = c11_empty
                        if p == 1 and c == 2:
                            c12 = c12_empty
                        if p == 1 and c == 3:
                            c13 = c13_empty
                        if p == 2 and c == 1:
                            c21 = c21_empty
                        if p == 2 and c == 2:
                            c22 = c22_empty
                        if p == 2 and c == 3:
                            c23 = c23_empty
                        break
                if card.upper() == "CC":
                    c11 = c11_empty
                    c12 = c12_empty
                    c13 = c13_empty
                    c21 = c21_empty
                    c22 = c22_empty
                    c23 = c23_empty

                    outcome = "Cancelled"
                    break
                if card.upper() == "C":
                    prevplayer = 1
                    if activeplayer == 1:
                        prevplayer = 2
                    if prevplayer == 1 and prevc == 1:
                        c11[prevrow][0] = 0
                    if prevplayer == 1 and prevc == 2:
                        c12[prevrow][0] = 0
                    if prevplayer == 1 and prevc == 3:
                        c13[prevrow][0] = 0
                    if prevplayer == 2 and prevc == 1:
                        c21[prevrow][0] = 0
                    if prevplayer == 2 and prevc == 2:
                        c22[prevrow][0] = 0
                    if prevplayer == 2 and prevc == 3:
                        c23[prevrow][0] = 0
                    if activeplayer == 1:
                        turn1 = turn1 - 1
                    if activeplayer == 2:
                        turn2 = turn2 - 1
                    break
                if numcard(card):
                    curses.echo()
                    clearline(win,cprompty)
                    clearline(win,cprompty + 1)
                    if turn <= 3:
                        cplay = turn
                    else:
                        cplay = int(promptn(win,"Play " + card.upper() + " on Caravan number...",3))
                    p = activeplayer
                    c = cplay
                    validplay = playcard(win,card,cplay,activeplayer)
                    if validplay == True:
                        if p == 1 and c == 1:
                            addrow = addn_caravan(c11)
                            c11[addrow][0] = card.upper()
                        if p == 1 and c == 2:
                            addrow = addn_caravan(c12)
                            c12[addrow][0] = card.upper()
                        if p == 1 and c == 3:
                            addrow = addn_caravan(c13)
                            c13[addrow][0] = card.upper()
                        if p == 2 and c == 1:
                            addrow = addn_caravan(c21)
                            c21[addrow][0] = card.upper()
                        if p == 2 and c == 2:
                            addrow = addn_caravan(c22)
                            c22[addrow][0] = card.upper()
                        if p == 2 and c == 3:
                            addrow = addn_caravan(c23)
                            c23[addrow][0] = card.upper()
                        prevrow = addrow
                        prevc = c
                    else:
                        win.addstr(cprompty,cpromptx,"Sorry, invalid play...",curses.A_BOLD)
                        win.refresh()
                        time.sleep(2)
                        win.addstr(cprompty,cpromptx,"                      ")

                if facecard(card):
                    pplay = prompt(win,"Play " + card.upper() + " on whose Caravan...",players[1],players[2])
                    cplay = promptn(win,"Play " + card.upper() + " on Caravan number...",3)
                    pcaravan = False
                    p = pplay
                    c = cplay
                    while pcaravan == False:
                        clearline(win,cprompty)
                        clearline(win,cprompty + 1)
                        win.addstr(cprompty,cpromptx,"Play %s on %s's Caravan %s in position : " % (card.upper(),players[p],c),curses.A_BOLD)
                        cardpos = win.getstr(cprompty,cpromptx + 35,2)
                        pcaravan = playpos(p,c,cardpos,card)
                    if p == 1 and c == 1:
                        c11 = pcaravan
                        validplay = True
                    if p == 1 and c == 2:
                        c12 = pcaravan
                        validplay = True
                    if p == 1 and c == 3:
                        c13 = pcaravan
                        validplay = True
                    if p == 2 and c == 1:
                        c21 = pcaravan
                        validplay = True
                    if p == 2 and c == 2:
                        c22 = pcaravan
                        validplay = True
                    if p == 2 and c == 3:
                        c23 = pcaravan
                        validplay = True
#                    
        if activeplayer == 1:
            activeplayer = 2
        else:
            activeplayer = 1
    return outcome

# Main game loop, runs setup loop and game loop in sequence until quit
def mainloop(win,ref):
    while 1:
        players = False
        while players == False:
            players = setup_screen(win)
        outcome = False
        while outcome == False:
            outcome = gameloop(win,players)

# Step through loops
def startup(win):
#    splash(win)
#    ref = False
#    while ref == False:
#        ref = login_screen(win)
    ref = "Erik"
    result = False
    while result == False:
        result = mainloop(win,ref)

if __name__=='__main__':
    try:
        stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, fgcolor, bgcolor)
        stdscr.bkgd(curses.color_pair(1))
#        curses.noecho()
        curses.cbreak()
#        stdscr.nodelay(1)
        stdscr.keypad(1)
        startup(stdscr)
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except:
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


