from datetime import datetime
startime = input("Enter start time in 24h format: ")
endtime = input("Enter end time in 24h format: ")    #preset timings to do hw
inp = open("testfile.txt","r")
y = inp.read().split("\n")    #read file containing all undone hw
y.pop(-1) # get rid of trailing space
hws=[]
for data in y:
    r=data.split()
    ddate,Duration = r[0],r[-1]
    name=""
    for i in range(1,len(r)-1):
        name+=r[i]+" "
    name.strip()
    ddate = int(ddate)
    Duration=int(Duration)
    hws.append([ddate,name,Duration])
inp.close()
print(hws)
#functions
# 1. read hw from file
# 2. ask for hw + times
# 3. sort hw by due date
# 4. plan timetable by tasks in order (e.g. hw due earliest first)
#   a) 10 min break for every hour of work or after end of a task, whichever is longer
#   b) stop early instead of overshooting
#   c) minimise wasted time
# 5. write remaining hw into file, 
print("1. Enter the due date (dd/mm/yyyy)")
print("2. Enter the homework name")
print("3. Time you want to spend on it in minutes")
print("E.g. 30/03/2022")
print("     Physics BSWS 2")
print("     90 ")   #instructions to user

decision="Y"
while decision != "N":
    dd = input("Enter the due date: ")
    name = input("Enter homework name: ")
    duration = input("Enter time to spend on homework in minutes: ")
    dd = int(dd[6:]+dd[3:5]+dd[:2])   # format due date to make sorting easier
    duration = int(duration)
    hws.append([dd,name,duration])
    
    decision = input("Add another homework? [Y/N]: ")  #ask to continue entering hw
    while decision not in "YN":
        decision = input("Add another homework? [Y/N]: ") 
hws.sort() #sort hw by due date
atime = (int(endtime[:2])-int(startime[:2]))*60+(int(endtime[2:])-int(startime[2:])) #total time available based on start and end times
totaltime=0
indexes=[]  # store the index of hw that is added to the timetable, to be removed later
timeWithoutBreak=0  #track how long a student has been studying without break
order=[]    #order of hw being done
for i in range(len(hws)):
    hwtime=hws[i][2]
    if hwtime + totaltime <= atime:   #check if can fit hw into the remaining time
        totaltime+=hwtime
        indexes.append(i)
        order.append(hwtime)
        timeWithoutBreak+=hwtime  
        
    if timeWithoutBreak >= 60:   # if student has studied for more than 1h without break, give 10min break
        order.append("b")
        totaltime+=10
        timeWithoutBreak = 0
intstart=startime
hwcount=0
def addtime(time,add):
    h,m=int(time[:2]),int(time[2:])
    m+=add
    h+=m//60
    m%=60
    h,m=str(h),str(m)
    if len(h)<2:
        h="0"+h
    if len(m)<2:
        m="0"+m
    return h+m
    
for task in order:
    if task == "b":                    #timetable planning
        task=10
        title = "break"
    else:
        title = hws[indexes[hwcount]][1]
        hwcount+=1
    intend = addtime(intstart,task)
    print("{} - {} : {}".format(intstart,intend,title))
    intstart=intend
indexes.sort(reverse=True)
for i in indexes:
    hws.pop(i)

outp = open("testfile.txt","w")

for i in range(len(hws)):
   outp.write(str(hws[i][0])+" "+str(hws[i][1])+" "+str(hws[i][2])) #write the remaining hw back into the file
   outp.write("\n")
outp.close()
