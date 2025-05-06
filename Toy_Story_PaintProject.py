from random import *
from pygame import *
from math import *
from time import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.colorchooser import askcolor

root = Tk()
root.withdraw()
mixer.init() #initializes music module within pygame
font.init() 
screen=display.set_mode((1200,865))
display.set_caption('Toy Story Paint') #before anything is saved, the initial caption title is 'Toy Story Paint'

# background image-------------------------
background= image.load("images/toy story.jpg")
screen.blit(background,(0,0))  

#songs-------------------------------------
songs=["songs/01 - opening.mp3","songs/02 - title screen.mp3","songs/04 - red alert.mp3","songs/07 - andy's neighborhood.mp3","songs/08 - revenge of the toys.mp3","songs/09 - run rex, run.mp3", 'songs/11 - alleys and gullies.mp3',"songs/14 - the claw.mp3",'songs/16 - elevator hop.mp3'] #playlist
shuffle(songs)
song_end= USEREVENT+1 #creates an event when a song is finished
mixer.music.set_endevent(song_end)  #sets that variable as the endevent
opening=mixer.music.load(songs[0]) #first song that will be played after shuffled
mixer.music.play()
song_pos=1 #will determine which song will be played next by the position of a list

# title------------------------------------
title = image.load("images/title.png")
title2=transform.scale(title,(485,160))
screen.blit(title2,(500,3))                    

# lighter split----------------------------
split= Surface((290,900),SRCALPHA)
draw.rect(split,(180,241,225,50),(0,0,270,900))
screen.blit(split,(0,0)) #blits a transparent panel

# more colours panel----------------------------
tab_col_Rect= Rect(9,627,32,32)
palette=image.load("tools/paint.png")
screen.blit(palette,(9,627))

#normal colour choosing-----    
rainbow=image.load("images/colours.jpg")
rainbow2=transform.scale(rainbow,(240,175))
screen.blit(rainbow2,(15,680))
colour_outline_Rect= Rect(13,678,243,177)

#Rects that the mouse can collide with=================
canvasRect,clearRect,undoRect,redoRect,saveRect,loadRect,pencilRect,eraserRect,brushRect,sprayRect,markerRect,lineRect,ellipseRect,rectRect,polygonRect,dropperRect,colouringRect,stampRect,arrow_back,arrow_forward,colour_picker_Rect,size_stamp1,size_stamp2,size_stamp3,Rect1,Rect2,Rect3,Rect4=Rect(310,170,855,535),Rect(30,10,200,45),Rect(325,116,80,45), Rect(430,116,80,45), Rect(280,10,80,65), Rect(380,10,80,65), Rect(40,80,77,77), Rect(142,80,77,77), Rect(40,182,77,77), Rect(142,182,77,77), Rect(40,284,77,77), Rect(142,284,77,77), Rect(40,386,77,77), Rect(142,386,77,77), Rect(40,488,77,77), Rect(142,488,77,77),Rect(282,715,100,65),Rect(282,790,100,65),Rect(409,749,40,70),Rect(1065,749,40,70),Rect(15,670,240,175),Rect(985,116,45,45),Rect(1050,116,45,45),Rect(1115,116,45,45),Rect(474,736,113,95),Rect(627,736,113,95),Rect(779,736,113,95),Rect(932,736,113,95)
musicRect=Rect(1010,22,63,57)
draw.rect(screen,(0),musicRect,1)
#intial tool sizes---------------------
size_pencil,size_eraser,size_brush,size_spray,size_marker,size_line,size_rect,size_ellipse,size_stamp= 1,1,5,1,1,1,1,1,'1'

click=0 #progam starts off with user clicking the arrows for stamps 0 times
tool='pencil'
other='undo'
sticker='1' 
panel='1' #the first panel for stickers
page='' #a colouring page isn't autonmatically added when program opens
option_stamp='colouring' #program starts with the colouring option
shape_option='unfill' 
music='on' #the music is 
pause=None              
undo_list=[] #list that will contain images of canvas every time an action occurs
redo_list=[] #list that will contain images of canvas that were undo-ed
poly=[] #list of all the positions clicked when user uses the polygon tool
COLOUR=(0,0,0,0) #the intial colour is set as black
running=True
draw.rect(screen,(255,255,255),canvasRect) #canvas
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==song_end:
            mixer.music.load(songs[song_pos]) #loads the song at the position
            mixer.music.play() #plays it
            song_pos+=1 # Updates song position to play next song
            if song_pos==9:
                song_pos=0 #once all the songs are played it restarts
        if evt.type == MOUSEBUTTONDOWN:
            lx,ly = evt.pos
            if evt.button == 1:
                start = evt.pos
                if tool!='dropper' and canvasRect.collidepoint(mx,my):
                    canvas_copy=screen.subsurface(canvasRect).copy() #a copy of the canvas will be taken 
                    screen.blit(canvas_copy,(310,170))
                    undo_list.append(canvas_copy) # the canvas copy is added to the undo list

                if len(undo_list)>=1 and undoRect.collidepoint(mx,my):
                    screen.blit(undo_list[-1],(310,170)) #the last canvas copy from the undo list is shown
                    redo_list.append(undo_list[-1]) #the last canvas copy from the undo list is added to the redo list
                    x=undo_list.pop() #last copy of canvas from undo list is deleted so that the same image isn't shown everytime the undo button is pressed
                   
                if len(redo_list)>=1 and redoRect.collidepoint(mx,my):
                    screen.blit(redo_list[-1],(310,170)) #the last undo copy is shown
                    undo_list.append(redo_list[-1]) #the redo image is added to the undo list so that the user can go back and fourth
                    x=redo_list.pop() #the casy redo image is deleted 

            elif evt.button == 4: #conditions for all the drawing tools and the max thickness the tool sizes can be when user scrolls up
                if tool=='eraser':
                    if size_eraser!=20:
                        size_eraser+= 1
                elif tool=='pencil':
                    if size_pencil<5:
                        size_pencil+=1
                elif tool=='brush':
                    if size_brush!=25:
                        size_brush+=1
                elif tool=='spray':
                    if size_spray!=30:
                        size_spray+=1
                elif tool=='marker':
                    if size_marker!=30:
                        size_marker+=1
                elif tool=='line':
                    if size_line!=25:
                        size_line+=1
                elif tool=='rect':
                    if size_rect!=25:
                        size_rect+=1
                elif tool=='ellipse':
                    if size_ellipse!=10:
                        size_ellipse+=1
            elif evt.button == 5: #conditions for all the drawing tools and the min thickness the tool sizes have be when user scrolls down
                if tool=='eraser':
                    if size_eraser!=1:
                        size_eraser -= 1
                elif tool=='pencil':
                    if size_pencil >1:
                        size_pencil-=1
                elif tool=='brush':
                    if size_brush!=5:
                        size_brush-=1
                elif tool =='spray':
                    if size_spray>1:
                        size_spray-=1
                elif tool=='marker':
                    if size_marker>1:
                        size_marker-=1
                elif tool=='line':
                    if size_line>1:
                        size_line-=1
                elif tool=='rect':
                    if size_rect>1:
                        size_rect-=1
                elif tool=='ellipse':
                    if size_ellipse>1:
                        size_ellipse-=1
            
        elif evt.type==MOUSEBUTTONUP:
            umx,umy=evt.pos
            if evt.button!=4 and evt.button!=5:
                
#UNDO REDO=============================================
                if tool!='dropper' and canvasRect.collidepoint(mx,my):
                    canvas_copy=screen.subsurface(canvasRect).copy() 
                    screen.blit(canvas_copy,(310,170)) 
                    undo_list.append(canvas_copy) #when the user clicks up, the copied canvas will add into the undo list
                #same process is done as if mouse was pressed down but now, the last item drawn on canvas will be added to undo list
                if len(undo_list)>=1 and undoRect.collidepoint(mx,my):
                    screen.blit(undo_list[-1],(310,170))
                    redo_list.append(undo_list[-1])
                    x=undo_list.pop()
                if len(redo_list)>=1 and redoRect.collidepoint(mx,my):  
                    screen.blit(redo_list[-1],(310,170))
                    undo_list.append(redo_list[-1])
                    x=redo_list.pop()
#SAVE OPTION============================================
                if saveRect.collidepoint(mx,my):
                    try: #it is tried so that the program doesn't crash if the user cancels when saving
                        tool='save' #the tool is temporarily put as save so there's something to put for the except
                        new_file=asksaveasfilename(defaultextension='.png') #the document will be saved as a png file
                        image.save(screen.subsurface(canvasRect),new_file)
                        name=new_file.rfind('/')
                        dot=new_file.rfind('.')    
                        display.set_caption(new_file[name+1:dot]) #the new caption is what the user saved the file
                        tool='pencil'
                    except:
                        tool='pencil'
#LOAD OPTION===========================================
                if loadRect.collidepoint(mx,my):
                    result = askopenfilename(filetypes=[("Picture files", "*.png;*.jpg")])
                    try: #it is tried so that the program doesn't crash if the user cancels when loading
                        tool='load' #the tool is temperarily put on load
                        screen.set_clip(canvasRect) #so the image is cut to fit the canvas
                        load_result=image.load(result)
                        screen.blit(load_result,(310,170)) 
                        tool='pencil'
                    except:
                        tool='pencil'        
#MUSIC//ON OR OFF=======================================
            if musicRect.collidepoint(umx,umy):
                if music=='on':
                    mixer.music.set_volume(0.0) #if the music is already on and the music button is pressed, the volume for the music will turn to zero acting as if the music is off
                    music='off'
                elif music=='off': 
                    mixer.music.set_volume(1.0) # if the music is already off, then the volume will return back on
                    music='on'
#STICKER QUADRANTS=====================================
            if option_stamp=='stamp':
                if arrow_forward.collidepoint(umx,umy):
                    if click<3:
                        click+=1 #everytime the user clicks on the arrows for the stamps, the program adds a click until 3 and each click corresponds to a different panel
                if arrow_back.collidepoint(umx,umy):
                    if click>0:
                        click-=1
                if click==0:
                    panel='1'
                if click==1:
                    panel='2'
                if click==2:
                    panel='3'
        #tool after dropper-----------------------------
            if tool=='dropper' and canvasRect.collidepoint(umx,umy):
                tool='pencil' #once the dropper gets the desired colour value it will automatically go to the pencil tool

            if option_stamp=='colouring': # a colouring page is blitted accordding to the quadrant the user clicks in while in the 'colouring' stamp option 
                if Rect1.collidepoint(umx,umy):
                    page_1=image.load("tools/pics4_on.jpg")
                    screen.blit(page_1,(310,170))
                if Rect2.collidepoint(umx,umy):
                    page_2=image.load("tools/pic2_on.png")
                    screen.blit(page_2,(310,170))
                if Rect3.collidepoint(umx,umy):
                    page_3=image.load("tools/pic3_on.jpg")
                    screen.blit(page_3,(310,170))
                if Rect4.collidepoint(umx,umy):
                    page_4=image.load("tools/pic5_on.gif")
                    screen.blit(page_4,(310,170))
# MORE COLOURS TAB=========================================
            if tab_col_Rect.collidepoint(umx,umy):
                recentcols=[COLOUR]
                COLOUR,COLOURAsString=askcolor(title="Geri's Paint Palette" )
                if COLOUR==None:
                    COLOUR=recentcols[-1]#Will just make current colour the colour that it was before opening the dialog box, preventing a crash
                else: #if user doesn't pick a colour, so the program doesn't crash
                    recentcols.append(COLOUR) #That colour will be only item in recentcols list
                    COLOUR=recentcols[-1] #current colour will be last(only) item in recentcols list
#CLEAR============================================================  
            if clearRect.collidepoint(umx,umy):
                page=''
                draw.rect(screen,(255,255,255),canvasRect)
#--------------------------------------------------------------------------
            if tool=='poly' and canvasRect.collidepoint(mx,my) and evt.button!=3:
                poly.append((mx,my))
            if tool=='poly' and evt.button==3:
                poly.clear() #if the right mouse button is clicked, the list is cleared
    #----------------------------------------------------------------------
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    #cordinates+fonts------------------------------------------------------
    cordFont = font.Font("Lemon Juice.otf",27)
    coordRect= Rect(332,78,195,35)
    draw.rect(screen,(85,165,202),coordRect)
    cord=cordFont.render(('Coordinates ('+str(mx)+','+str(my)+')'),False,(0,0,128))
    screen.blit(cord,(329,82))
    
    #icon pictures---------------------------------------------------------
    icon=["tools/pages.png","tools/stamp.png","tools/pencil.png","tools/eraser.png","tools/brush.png","tools/marker.png","tools/spray.png","tools/line.png","tools/rectangle.png","tools/circle.png","tools/poly.png","tools/dropper.png","tools/undo.png","tools/redo.png","tools/clear.png","tools/save.png",'tools/load.png']
    icon_pos=[(282,715),(282,790),(40,80),(141,80),(40,182),(40,284),(141,182),(141,284),(141,386),(40,386),(40,488),(141,488),(330,116),(430,116),(30,10),(280,10),(380,10)]
    for w in range(17):
        icon_image=image.load(icon[w])
        screen.blit(icon_image,icon_pos[w])
    if option_stamp=='stamp':
        arrow_f=image.load("tools/arrow_forward.png")
        screen.blit(arrow_f,(1065,749))
        arrow_b=image.load("tools/arrow_back.png")
        screen.blit(arrow_b,(409,749))
    icon_rect=[pencilRect,eraserRect,brushRect,sprayRect,lineRect,rectRect,ellipseRect,markerRect,polygonRect,dropperRect]
    for x in range(10):
        draw.rect(screen,(21,77,145),icon_rect[x],3) #for tool borders
    #clear---------------------------------------
    if clearRect.collidepoint(mx,my):
        clear=image.load("tools/clear_on.png")
        screen.blit(clear,(30,10))
    #music---------------------------------------
    if music=='on':
        music_on=image.load("tools/music_on.png")
        screen.blit(music_on,(1010,22))
    elif music=='off':
        music_off=image.load("tools/music_off.png")
        screen.blit(music_off,(1010,22))
    #pencil-------------------------------------
    draw.rect(screen,(83,165,203),(960 ,90,210,80))# drawn to show different sizes of tools
    if pencilRect.collidepoint(mx,my):
        pen = image.load("tools/pencil_on.png")
        screen.blit(pen,(40,80))
        if mb[0]==1:
            tool='pencil'
    if tool =='pencil':
        pen = image.load("tools/pencil_on.png")
        screen.blit(pen,(40,80))
        des=image.load("tools/des_pen.png") #description of tool
        screen.blit(des,(21,576))
        draw.circle(screen,COLOUR,(1130,125),size_pencil) #to show tool size
        acc_size=cordFont.render(('SIZE: '+str(size_pencil)),False,(0,0,128))
    # eraser--------------------------------------    
    if eraserRect.collidepoint(mx,my):
        eraser = image.load("tools/eraser_on.png")
        screen.blit(eraser,(141,80))
        if mb[0]==1:
            tool='eraser'
    if tool=='eraser':
        eraser = image.load("tools/eraser_on.png")
        screen.blit(eraser,(141,80))
        des=image.load("tools/des_erase.png")
        screen.blit(des,(21,576)) #description of tool
        draw.circle(screen,(255,255,255),(1130,125),size_eraser) #to show tool size
        acc_size=cordFont.render(('SIZE: '+str(size_eraser)),False,(0,0,128))
    # brush----------------------------------------    
    if brushRect.collidepoint(mx,my):
        brush=image.load("tools/brush_on.png")
        screen.blit(brush,(40,182))
        if mb[0]==1:
            tool='brush'
    if tool=='brush':
        brush=image.load("tools/brush_on.png")
        screen.blit(brush,(40,182))
        des_brush=image.load("tools/des_brush.png") #description of tool
        screen.blit(des_brush,(21,576))
        draw.circle(screen,COLOUR,(1130,125),size_brush) #to show tool size
        acc_size=cordFont.render(('SIZE: '+str(size_brush)),False,(0,0,128))
    # spray-----------------------------------------
    if sprayRect.collidepoint(mx,my):
        spray = image.load("tools/spray_on.png")
        screen.blit(spray,(141,182))
        if mb[0]==1:
            tool='spray'
    if tool=='spray':
        spray = image.load("tools/spray_on.png")
        screen.blit(spray,(141,182))
        des=image.load("tools/des_spray.png")
        screen.blit(des,(21,576))
        draw.circle(screen,COLOUR,(1130,125),size_spray,1) #to show tool size
        acc_size=cordFont.render(('SIZE: '+str(size_spray)),False,(0,0,128))
    # MARKER-----------------------------------------------
    if markerRect.collidepoint(mx,my):
        marker=image.load("tools/marker_on.png")
        screen.blit(marker,(40,284))
        if mb[0]==1:
            tool='marker'
    if tool=='marker':
        marker=image.load("tools/marker_on.png")
        screen.blit(marker,(40,284))
        des=image.load("tools/des_marker.png") #description of tool
        screen.blit(des,(21,576))
        draw.circle(screen,COLOUR,(1130,125),size_marker) #to show tool size
        acc_size=cordFont.render(('SIZE: '+str(size_marker)),False,(0,0,128))
    #line--------------------------------------------
    if lineRect.collidepoint (mx,my):
        line=image.load("tools/line_on.png")
        screen.blit(line,(141,284))
        if mb[0]==1:
            tool='line'
    if tool=='line':
        line=image.load("tools/line_on.png")
        screen.blit(line,(141,284))
        des=image.load("tools/des_line.png") #description of tool
        screen.blit(des,(21,576))
        draw.line(screen,COLOUR,(1130,100),(1130,145),size_line) #to show tool size
        acc_size=cordFont.render(('SIZE: '+str(size_line)),False,(0,0,128))
    #size---------------------------------------------
    if tool=='pencil'or tool=='eraser'or tool=='brush' or tool== 'line' or tool== 'spray' or tool=='marker':
        sizeRect= Rect(975,115,115,35)
        draw.rect(screen,(85,165,202),sizeRect)
        screen.blit(acc_size,(1019,115)) #to get each tool's size when it's typed out
    #fill/unfill------------------------------------
    if tool=='rect' or tool=='ellipse':
        sizeRect= Rect(1000,80,195,35)
        draw.rect(screen,(85,165,202),sizeRect)
        unfill_shape_rect= Rect(975,116,80,45)
        fill_shape_rect= Rect(1070,116,80,45)
        unfill_option=image.load("tools/unfill_option.png")
        screen.blit(unfill_option,(975,116))
        fill_option=image.load("tools/fill_option.png")
        screen.blit(fill_option,(1070,116))

        if unfill_shape_rect.collidepoint(mx,my):
            unfill_option=image.load("tools/unfill_option_on.png")
            screen.blit(unfill_option,(975,116))
            if mb[0]==1:
                shape_option='unfill'
        if shape_option=='unfill':
            screen.blit(acc_size,(1035,85))
            unfill_option=image.load("tools/unfill_option_on.png")
            screen.blit(unfill_option,(975,116)) #unfill image is on
            
        if fill_shape_rect.collidepoint(mx,my):
            fill_option=image.load("tools/fill_option_on.png")
            screen.blit(fill_option,(1070,116))
            if mb[0]==1:
                shape_option='fill'
        if shape_option=='fill':
            fill_option=image.load("tools/fill_option_on.png")
            screen.blit(fill_option,(1070,116))
            
    #rect--------------------------------------------
    if rectRect.collidepoint(mx,my):
        rect=image.load("tools/rectangle_on.png")
        screen.blit(rect,(141,386))
        if mb[0]==1:
            tool='rect'
    if tool=='rect':
        rect=image.load("tools/rectangle_on.png")
        screen.blit(rect,(141,386))
        des=image.load("tools/des_rect.png") #description of tool
        screen.blit(des,(21,576))
        if shape_option=='unfill':
            acc_size=cordFont.render(('SIZE: '+str(size_rect)),False,(0,0,128)) #the size is only shown if the shape oopion is unfilled
    #ellipse------------------------------------------
    if ellipseRect.collidepoint(mx,my):
        ellipse= image.load("tools/circle_on.png")
        screen.blit(ellipse,(40,386))
        if mb[0]==1:
            tool='ellipse'
    if tool=='ellipse':
        ellipse= image.load("tools/circle_on.png")
        screen.blit(ellipse,(40,386))
        des=image.load("tools/des_circle.png") #description of tool
        screen.blit(des,(21,576))
        if shape_option=='unfill':
              acc_size=cordFont.render(('SIZE: '+str(size_ellipse)),False,(0,0,128))
              
    #polygon tool---------------------------------------------
    if polygonRect.collidepoint(mx,my):
        polygon= image.load("tools/poly_on.png")
        screen.blit(polygon,(40,488))
        if mb[0]==1:
            tool='poly'
    if tool=='poly':
        polygon= image.load("tools/poly_on.png")
        screen.blit(polygon,(40,488))
        des=image.load("tools/des_poly.png")
        screen.blit(des,(21,576))
        if canvasRect.collidepoint(mx,my) and len(poly)>=1:
            if mb[0]==1:
                screen.blit(canvas_copy,(310,170)) 
                draw.line(screen,COLOUR,poly[-1],(mx,my),1) #a line is drawn from the previous mousebuttonup posiiton to the cursor
            if mb[2]==1:
                screen.blit(canvas_copy,(310,170))
                draw.line(screen,COLOUR,poly[0],poly[-1],1) #a line is draw from the first polygon point position to the most recent one, to close the shape made
                
            
    # eye dropper------------------------------------------
    if dropperRect.collidepoint(mx,my):
        dropper=image.load("tools/dropper_on.png")
        screen.blit(dropper,(141,488))
        if mb[0]==1:
            tool='dropper'
    if tool=='dropper':
        dropper=image.load("tools/dropper_on.png")
        screen.blit(dropper,(141,488))
        des=image.load("tools/des_dropper.png")
        screen.blit(des,(21,576))
    #colouring /stamp------------------------------------

    if Rect1.collidepoint(mx,my) and mb[0]==1:
        if option_stamp=='stamp': #if the the stamp option is on and the user clicks one of the stickers at anytime, the tool will change to stamp
            sticker='1'
            tool='stamp'
        elif option_stamp=='colouring':
            page='1'
    if Rect2.collidepoint(mx,my) and mb[0]==1:
        if option_stamp=='stamp':
            sticker='2'
            tool='stamp'
        elif option_stamp=='colouring':
            page='2'
    if Rect3.collidepoint(mx,my) and mb[0]==1:
        if option_stamp=='stamp':
            sticker='3'
            tool='stamp'
        elif option_stamp=='colouring':
            page='3'

    if Rect4.collidepoint(mx,my) and mb[0]==1:
        if option_stamp=='stamp':
            sticker='4'
            tool='stamp'
        elif option_stamp=='colouring':
            page='4'
   #colouring-----------------------------------------------
            
    if colouringRect.collidepoint(mx,my):
        colouring=image.load("tools/pages_on.png")
        screen.blit(colouring,(282,715))
        if mb[0]==1:
            option_stamp='colouring'
    if option_stamp=='colouring':
       # depending on what quadrant is pressed, the border of the panel will change     
        if page=='1':
            panel_back=image.load("images/rect_1.jpg")
            screen.blit(panel_back,(457,729))
        if page=='2':
            panel_back=image.load("images/rect_2.jpg")
            screen.blit(panel_back,(457,729))
        if page=='3':
            panel_back=image.load("images/rect_3.jpg")
            screen.blit(panel_back,(457,729))
        if page=='4':
            panel_back=image.load("images/rect_4.jpg")
            screen.blit(panel_back,(457,729))
        if page=='':
            stamp= image.load("images/rect_none.jpg") # if none of the colouring pages are selected, it will indicate so 
            screen.blit(stamp,(457,729))
        colouring=image.load("tools/pages_on.png")
        screen.blit(colouring,(282,715))

#colouring pages blitted so user can pick which one they want
        pics_load=["images/left_piece.jpg","images/right_piece.jpg","tools/pics4.jpg","tools/pic2.jpg","tools/pic3.jpg","tools/pic5.gif"]
        pics_pos=[(390,733),(1054,735),(478,741),(630,743),(783,740),(938,740)]
        for i in range(6):
            pics=image.load(pics_load[i])
            screen.blit(pics,pics_pos[i])
    #----stamp=============

    if stampRect.collidepoint(mx,my) or tool=='clear':
        stamp=image.load("tools/stamp_on.png")
        screen.blit(stamp,(282,790))
        if mb[0]==1:
            option_stamp='stamp'
    if option_stamp=='stamp':
        stamp=image.load("tools/stamp_on.png")
        screen.blit(stamp,(282,790))
# depending on what quadrant is pressed, the border of the panel will change 
        if sticker=='1':
            panel_back=image.load("images/rect_1.jpg")
            screen.blit(panel_back,(457,729))
        if sticker=='2':
            panel_back=image.load("images/rect_2.jpg")
            screen.blit(panel_back,(457,729))
        if sticker=='3':
            panel_back=image.load("images/rect_3.jpg")
            screen.blit(panel_back,(457,729))
        if sticker=='4':
            panel_back=image.load("images/rect_4.jpg")
            screen.blit(panel_back,(457,729))        
        if tool!='stamp':
            stamp= image.load("images/rect_none.jpg") #if the tool is not stickers, there will not be a border on it
            screen.blit(stamp,(457,729))
            stamp=image.load("tools/stamp_on.png")
            screen.blit(stamp,(282,790))

        if tool=='stamp':
            des=image.load("tools/des.png") #description of what to do to get out of stickers
            screen.blit(des,(21,576))
        #different sizes for stickers (buttons) are blitted
            size_1= image.load("tools/size_1.png")
            screen.blit(size_1,(985,116))
            size_2= image.load("tools/size_2.png")
            screen.blit(size_2,(1050,116))
            size_3= image.load("tools/size_3.png")
            screen.blit(size_3,(1115,116))
        #to indicate what size the user has picked for the stickers
            if size_stamp1.collidepoint(mx,my):
                size_1= image.load("tools/size_1_on.png")
                screen.blit(size_1,(985,116))
                if mb[0]==1:
                    size_stamp='1'
            if size_stamp2.collidepoint(mx,my):
                size_2= image.load("tools/size_2_on.png")
                screen.blit(size_2,(1050,116))
                if mb[0]==1:
                    size_stamp='2'
            if size_stamp3.collidepoint(mx,my):
                size_3= image.load("tools/size_3_on.png")
                screen.blit(size_3,(1115,116))
                if mb[0]==1:
                    size_stamp='3'
            if size_stamp=='1':
                size_1= image.load("tools/size_1_on.png")
                screen.blit(size_1,(985,116))
            if size_stamp=='2':
                size_2= image.load("tools/size_2_on.png")
                screen.blit(size_2,(1050,116))
            if size_stamp=='3':
                size_3= image.load("tools/size_3_on.png")
                screen.blit(size_3,(1115,116))
        
        if arrow_back.collidepoint(mx,my):
            if panel=='2' or panel=='3':
                arrow_b= image.load("tools/arrow_back_on.png")
                screen.blit(arrow_b,(409,749))# so the user knows they can still click back
        if arrow_forward.collidepoint(mx,my):
            if panel=='1' or panel=='2':
                arrow_f= image.load("tools/arrow_forward_on.png")
                screen.blit(arrow_f,(1065,749))#so the user knows they can still click the forwaard arrow

        #------------to show the user that their clicks won't do anything ------------------
        if panel=='3':
            arrow_f= image.load("tools/arrow_forward_none.png")
            screen.blit(arrow_f,(1065,749))
        if panel=='1':
            arrow_b= image.load("tools/arrow_back_none.png")
            screen.blit(arrow_b,(409,749))
#ALL STICKERS BLITED FOR EACH SEPERATE PANEL==================        
    if panel=='1' and option_stamp=='stamp':
        S1=image.load("tools/S1.png")
        screen.blit(S1,(475,732))
        S2= image.load("tools/S2.png")
        screen.blit(S2,(636,737))
        S3= image.load("tools/S3.png")
        screen.blit(S3,(782,737))
        S4= image.load("tools/S4.png")
        screen.blit(S4,(963,736))
    elif panel=='2' and option_stamp=='stamp':
        S5 = image.load("tools/S5.png")
        screen.blit(S5,(481,730))
        S7 = image.load("tools/S7.png")
        screen.blit(S7,(628,747))
        S6= image.load("tools/S6.png")
        screen.blit(S6,(779,730))
        S8 = image.load("tools/S8.png")
        screen.blit(S8,(940,733))
    elif panel=='3' and option_stamp=='stamp':
        S9= image.load("tools/S9.png")
        screen.blit(S9,(477,738 ))
        S10 = image.load("tools/S10.png")
        screen.blit(S10,(630,740))
        S11= image.load("tools/S11.png")
        screen.blit(S11,(787,737))
        S12 = image.load("tools/S12.png")
        screen.blit(S12,(940,738))
    #undo-----------------------------------------------
        
    if len(undo_list)==0:
        undo=image.load("tools/undo_none.png") # when the undo list is empty a grey undo button will blit indicating that nothing can be undoed        
        screen.blit(undo,(330,116))
    if undoRect.collidepoint(mx,my):
        if len(undo_list)>=1:
            undo=image.load("tools/undo_on.png") #if the undo list is greater than 0 it will turn green
            screen.blit(undo,(330,116))
    #redo-----------------------------------------------
    if len(redo_list)==0:
        redo=image.load("tools/redo_none.png") # when the redo list is empty a grey undo button will blit indicating that nothing can be undoed
        screen.blit(redo,(430,116))

    if redoRect.collidepoint(mx,my):
        if len(redo_list)>=1:
            redo=image.load("tools/redo_on.png") #if the redo list is greater than 0 it will turn green
            screen.blit(redo,(430,116))
    #colour----------------------------------------
    colour_display_Rect=(15,665,240,8) 
    colour_diplayborder_Rect=draw.rect(screen,(255,255,255),(14,664,242,9),3)
    draw.rect(screen,COLOUR,colour_display_Rect) #so the user knows what colour is picked
    draw.rect(screen,(255,255,255),colour_outline_Rect,2)
    
    if colour_picker_Rect.collidepoint(mx,my):
        draw.rect(screen,(0,0,255),colour_outline_Rect,2)
        if mb[0]==1:
            screen.set_clip(colour_outline_Rect)
            screen.blit(rainbow2,(15,680))
            draw.circle(screen,(255,255,255),(mx,my),5,1)
            COLOUR = screen.get_at ((mx,my)) # gets the colour value depending where the user has clicked on the rainbow image
        
    # possibilities of mouse touching canvas---------
    if mb[0]==1 and canvasRect.collidepoint(mx,my) and tool!='save' and tool!='load': 
        if tool!='dropper':
            mouse.set_visible(False) # so the mouse is only seen when the dropper tool is in use
            screen.set_clip(canvasRect)
        if tool=='pencil':
            draw.line(screen,COLOUR,(omx,omy),(mx,my),size_pencil)
        if tool=='eraser':
            # to connect the circles when the user draws
            slopex=int(mx-omx)
            slopey=int(my-omy)
            d=max(abs(slopex),abs(slopey))
            for i in range(d):
                ex=int((omx)+float(i)/d*slopex)
                ey=int((omy)+float(i)/d*slopey)
                draw.circle(screen,(255,255,255),(ex,ey),size_eraser)

        if tool=='brush':
            slopex=int(mx-omx)
            slopey=int(my-omy)
            d=max(abs(slopex),abs(slopey))
            for i in range(d):
                bx=int((omx)+float(i)/d*slopex)
                by=int((omy)+float(i)/d*slopey)
                draw.circle(screen,COLOUR,(bx,by),size_brush)

        if tool=='spray':
            for i in range(size_spray+10):
                dotx=randint(-size_spray,size_spray)
                doty=randint(-size_spray,size_spray)
                distance=abs(((mx-(dotx+mx))**2+(my-(doty+my))**2)**.5) #distance of the random dot to the cursor
                if distance<=size_spray:
                    draw.line(screen,COLOUR,(mx+dotx,my+doty),(mx+dotx,my+doty),1)
        
        if tool=='marker':
            markerHead= Surface((60,60),SRCALPHA) #to make blank surface
            slopex=int(mx-omx)
            slopey=int(my-omy)
            d= max(abs(slopex),abs(slopey))
            for i in range(d):
                rx=int((omx)+float(i)/d*slopex)
                ry=int((omy)+float(i)/d*slopey)
                draw.circle(markerHead,(COLOUR[0],COLOUR[1],COLOUR[2],3),(30,30),size_marker) #drawing using alpha so it is more transparent
                if mx!=omx or my!=omy:
                    screen.blit(markerHead,(rx-30,ry-30))

        if tool=='line':
            screen.blit(canvas_copy,(310,170))
            draw.line(screen,COLOUR,(lx,ly),(mx,my),size_line)

        if tool=='dropper':
            COLOUR = screen.get_at((mx,my))
            
        if tool=='rect':
            screen.blit(canvas_copy,(310,170))
            length=(mx-lx)
            width=(my-ly)
            length_2=lx-mx
            width_2=ly-my

            if shape_option=='unfill':
                if size_rect<4:
                    draw.rect(screen,COLOUR,(lx,ly,length,width),size_rect)
                #4 seperate rectangles were made depending on which direction the user moves the mouse
                else:
                    if mx>lx or my>ly: # this checks if the rectangle is in the 1st,3rd, or 4th quadrant  
                        draw.rect(screen,COLOUR,(lx,ly,length,size_rect)) #horizonal
                        draw.rect(screen,COLOUR,(lx,ly,size_rect,width)) #vertical
                        draw.rect(screen,COLOUR,(lx,ly+width-size_rect,length,size_rect)) #draws the bottom rectangle side/line but decreases y value so corners overlap                   
                        draw.rect(screen,COLOUR,(lx+length-size_rect,ly,size_rect,width)) # draws the right rectangle side/line but decreases the x value so the corners overlap
                    elif mx<lx and my<ly: #if rectangle is dragged into 2nd quadrant
                        draw.rect(screen,COLOUR,(mx,my,length_2,size_rect)) #horizontal
                        draw.rect(screen,COLOUR,(mx,my,size_rect,width_2)) #vertical
                        draw.rect(screen,COLOUR,(mx,my+width_2-size_rect,length_2,size_rect))                   
                        draw.rect(screen,COLOUR,(mx+length_2-size_rect,my,size_rect,width_2))
            if shape_option=='fill':
                draw.rect(screen,COLOUR,(lx,ly,length,width)) #draws normal filled rectangle
        if tool=='ellipse':
            screen.blit(canvas_copy,(310,170))
            length=abs(mx-lx)
            width=abs(my-ly)
            area=Rect(lx,ly,mx-lx,my-ly)
            area.normalize() #normalizes because ellipse is picky with numbers
            if shape_option=='unfill':
                if length>size_ellipse*2 and width>size_ellipse*2: #to make sure it can fit
                    draw.ellipse(screen,COLOUR,area,size_ellipse)
                else:
                    draw.ellipse(screen,COLOUR,area,0)
            elif shape_option=='fill':
                draw.ellipse(screen,COLOUR,area,0)

        #DIFFERENT POSSIBILITIES OF PICKING DIFFERENT STAMPS=======================
        if tool=='stamp' and option_stamp=='stamp':
            screen.blit(canvas_copy,(310,170))
            if size_stamp=='1':
                if panel=='1':
                    if sticker=='1':
                        S1_on=image.load("tools/S1_1.png")
                        screen.blit(S1_on,(mx-39 ,my-50))
                    if sticker=='2':
                        S2_on=image.load("tools/S2_1.png") 
                        screen.blit(S2_on,(mx-48 ,my-50))
                    if sticker=='3':
                        S3_on=image.load("tools/S3_1.png")
                        screen.blit(S3_on,(mx-42 ,my-50))
                    if sticker=='4':
                        S4_on=image.load("tools/S4_1.png")
                        screen.blit(S4_on,(mx-22 ,my-50))
                if panel=='2':
                    if sticker=='1':
                        S5_on=image.load("tools/S5_1.png")
                        screen.blit(S5_on,(mx-34 ,my-50))
                    if sticker=='2':
                        S7_on=image.load("tools/S6_1.png")
                        screen.blit(S7_on,(mx-45 ,my-55))
                    if sticker=='3':
                        S6_on=image.load("tools/S7_1.png")
                        screen.blit(S6_on,(mx-52 ,my-60))
                    if sticker=='4':
                        S8_on=image.load("tools/S8_1.png")
                        screen.blit(S8_on,(mx-50 ,my-50))
                if panel=='3':
                    if sticker=='1':
                        S9_on=image.load("tools/S9_1.png")
                        screen.blit(S9_on,(mx-50 ,my-50))
                    if sticker=='2':
                        S10_on=image.load("tools/S10_1.png")
                        screen.blit(S10_on,(mx-50 ,my-50))
                    if sticker=='3':
                        S11_on=image.load("tools/S11_1.png")
                        screen.blit(S11_on,(mx-35 ,my-50))
                    if sticker=='4':
                        S12_on=image.load("tools/S12_1.png")
                        screen.blit(S12_on,(mx-45 ,my-50))   
            if size_stamp=='2':
                if panel=='1':
                    if sticker=='1':
                        S1_on=image.load("tools/S1_2.png")
                        screen.blit(S1_on,(mx-70 ,my-100))
                    if sticker=='2':
                        S2_on=image.load("tools/S2_2.png")
                        screen.blit(S2_on,(mx-85 ,my-100))
                    if sticker=='3':
                        S3_on=image.load("tools/S3_2.png")
                        screen.blit(S3_on,(mx-84 ,my-100))
                    if sticker=='4':
                        S4_on=image.load("tools/S4_2.png")
                        screen.blit(S4_on,(mx-38 ,my-100))
                if panel=='2':
                    if sticker=='1':
                        S5_on=image.load("tools/S5_2.png")
                        screen.blit(S5_on,(mx-67 ,my-100))
                    if sticker=='2':
                        S7_on=image.load("tools/S6_2.png")
                        screen.blit(S7_on,(mx-95 ,my-115))
                    if sticker=='3':
                        S6_on=image.load("tools/S7_2.png")
                        screen.blit(S6_on,(mx-103 ,my-115))
                    if sticker=='4':
                        S8_on=image.load("tools/S8_2.png")
                        screen.blit(S8_on,(mx-100 ,my-100))
                if panel=='3':
                    if sticker=='1':
                        S9_on=image.load("tools/S9_2.png")
                        screen.blit(S9_on,(mx-100 ,my-100))
                    if sticker=='2':
                        S10_on=image.load("tools/S10_2.png")
                        screen.blit(S10_on,(mx-100 ,my-100))
                    if sticker=='3':
                        S11_on=image.load("tools/S11_2.png")
                        screen.blit(S11_on,(mx-75 ,my-100))
                    if sticker=='4':
                        S12_on=image.load("tools/S12_2.png")
                        screen.blit(S12_on,(mx-95 ,my-100)) 
            if size_stamp=='3':
                if panel=='1':
                    if sticker=='1':
                        S1_on=image.load("tools/S1_3.png")
                        screen.blit(S1_on,(mx-98 ,my-150))
                    if sticker=='2':
                        S2_on=image.load("tools/S2_3.png")
                        screen.blit(S2_on,(mx-136 ,my-150))
                    if sticker=='3':
                        S3_on=image.load("tools/S3_3.png")
                        screen.blit(S3_on,(mx-125 ,my-150))
                    if sticker=='4':
                        S4_on=image.load("tools/S4_3.png")
                        screen.blit(S4_on,(mx-60 ,my-150))
                if panel=='2':
                    if sticker=='1':
                        S5_on=image.load("tools/S5_3.png")
                        screen.blit(S5_on,(mx-100 ,my-150))
                    if sticker=='2':
                        S7_on=image.load("tools/S6_3.png")
                        screen.blit(S7_on,(mx-140 ,my-170))
                    if sticker=='3':
                        S6_on=image.load("tools/S7_3.png")
                        screen.blit(S6_on,(mx-155 ,my-170))                
                    if sticker=='4':
                        S8_on=image.load("tools/S8_3.png")
                        screen.blit(S8_on,(mx-150 ,my-150))
                if panel=='3':
                    if sticker=='1':
                        S9_on=image.load("tools/S9_3.png")
                        screen.blit(S9_on,(mx-150 ,my-150))
                    if sticker=='2':
                        S10_on=image.load("tools/S10_3.png")
                        screen.blit(S10_on,(mx-150 ,my-150))
                    if sticker=='3':
                        S11_on=image.load("tools/S11_3.png")
                        screen.blit(S11_on,(mx-125 ,my-150))
                    if sticker=='4':
                        S12_on=image.load("tools/S12_3.png")
                        screen.blit(S12_on,(mx-145,my-150))
    else :
        mouse.set_visible(True) # if the mouse isn't pressed down in the canvas, it will be visible
    screen.set_clip(None)
    omx,omy=mx,my
    #-------------------------

    display.flip()
quit()

