from tkinter import *
import serial, time
import serial.tools.list_ports
import time

time1 = ''
accvol=0,0,0,0

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
#print("Connected COM ports: " + str(connected))


gui= Tk()
ser=serial.Serial(str(connected[1]))

def apply():
    print('hej')
    
def cancel():
    print('nej')
        

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)


def vattna(slinga):
    
    global accvol
    
    volym=ent_extravol.get()
    tid=ent_extramtd.get()
    
    cmd=str(slinga) + ',' + str(volym) + ',' + str(tid) + '\r'

    #print(cmd)
    
    ser.write(cmd.encode('ascii'))
    
    tstart=time.process_time()
    while True:
        tmp=ser.readline()
        tmp=tmp.decode('ascii')
        tmp=tmp.split(',')
        channel=int(tmp[0])
        volume=int(tmp[1])
        tid=int(tmp[2])
        
        print(channel,tid,volume)

        if channel==-1:         
            break
        
    ent_nutd.delete(0,END)
    ent_nutd.insert(0,tid)
    ent_nuvol.delete(0,END)
    ent_nuvol.insert(0,volume)

         
    
cl_lbl=Label(gui, text="Aktuell tid : ")
cl_lbl.place(x=100,y=10)
clock=Label(gui)
clock.place(x=180,y=10)

btn_apply=Button(gui, text="Applicera", command = apply)
btn_apply.place(x=40, y=200)
btn_apply=Button(gui, text="Ångra", command = cancel)
btn_apply.place(x=120, y=200)

btn_v1=Button(gui, text="Vattna 1", command= lambda: vattna(1))
btn_v1.place(x=500, y=60)
btn_v1=Button(gui, text="Vattna 2", command= lambda: vattna(2))
btn_v1.place(x=500, y=90)
btn_v1=Button(gui, text="Vattna 3", command= lambda: vattna(3))
btn_v1.place(x=500, y=120)
btn_v1=Button(gui, text="Vattna 4", command= lambda: vattna(4))
btn_v1.place(x=500, y=150)





lbl_vol=Label(gui,text="Volym l")
lbl_vol.place(x=100,y=40)
lbl_vol=Label(gui,text="Maxtid s")
lbl_vol.place(x=180,y=40)
lbl_vol=Label(gui,text="Tid hh:mm")
lbl_vol.place(x=260,y=40)
lbl_avl=Label(gui,text="Acc vol dl")
lbl_avl.place(x=340,y=40)

cl_lbl=Label(gui, text="Extra")
cl_lbl.place(x=450,y=25)
lbl_vol=Label(gui,text="Volym dl")
lbl_vol.place(x=500,y=5)
lbl_vol=Label(gui,text="Maxtid s")
lbl_vol.place(x=580,y=5)
ent_extravol=Entry(gui,width=5,justify=RIGHT)
ent_extravol.place(x=500,y=25)
ent_extramtd=Entry(gui,width=5,justify=RIGHT)
ent_extramtd.place(x=580,y=25)


ent_nuvol=Entry(gui,width=5,justify=RIGHT)
ent_nuvol.place(x=500,y=190)
ent_nutd=Entry(gui,width=5,justify=RIGHT)
ent_nutd.place(x=580,y=190)



lbl_s1=Label(gui, text="Slinga 1")
lbl_s1.place(x=40,y=60)
ent_vol1=Entry(gui,width=5,justify=RIGHT)
ent_vol1.place(x=100,y=60)
ent_mtd1=Entry(gui,width=5,justify=RIGHT)
ent_mtd1.place(x=180,y=60)
ent_tid1=Entry(gui,width=6,justify=RIGHT)
ent_tid1.place(x=260,y=60)
ent_avl1=Entry(gui,width=6,justify=RIGHT)
ent_avl1.place(x=340,y=60)


lbl_s2=Label(gui, text="Slinga 2")
lbl_s2.place(x=40,y=90)
ent_vol2=Entry(gui,width=5,justify=RIGHT)
ent_vol2.place(x=100,y=90)
ent_mtd2=Entry(gui,width=5,justify=RIGHT)
ent_mtd2.place(x=180,y=90)
ent_tid2=Entry(gui,width=6,justify=RIGHT)
ent_tid2.place(x=260,y=90)
ent_avl2=Entry(gui,width=6,justify=RIGHT)
ent_avl2.place(x=340,y=90)

lbl_s3=Label(gui, text="Slinga 3")
lbl_s3.place(x=40,y=120)
ent_vol3=Entry(gui,width=5,justify=RIGHT)
ent_vol3.place(x=100,y=120)
ent_mtd3=Entry(gui,width=5,justify=RIGHT)
ent_mtd3.place(x=180,y=120)
ent_tid3=Entry(gui,width=6,justify=RIGHT)
ent_tid3.place(x=260,y=120)
ent_avl3=Entry(gui,width=6,justify=RIGHT)
ent_avl3.place(x=340,y=120)

lbl_s4=Label(gui, text="Slinga 4")
lbl_s4.place(x=40,y=150)
ent_vol4=Entry(gui,width=5,justify=RIGHT)
ent_vol4.place(x=100,y=150)
ent_mtd4=Entry(gui,width=5,justify=RIGHT)
ent_mtd4.place(x=180,y=150)
ent_tid4=Entry(gui,width=6,justify=RIGHT)
ent_tid4.place(x=260,y=150)
ent_avl4=Entry(gui,width=6,justify=RIGHT)
ent_avl4.place(x=340,y=150)



gui.title('Bevattningssystem växthus')
gui.geometry("680x230+50+20")

tick()
gui.mainloop()