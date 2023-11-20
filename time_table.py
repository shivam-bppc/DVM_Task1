import pymysql as x

a=input('Enter MySQL username: ')
b=input('Enter MySQL passwd: ')
timetable=x.connect(host='localhost',user=a,passwd=b)

cur=timetable.cursor()

create_database=("create database if not exists TIME_TABLE;")
cur.execute(create_database)

use_database=('use TIME_TABLE;')
cur.execute(use_database)

#adminpass
create_table_adminpass=("create table if not exists adminpass(Admin_name varchar(30) not null primary key,\
                        admin_passwd varchar(20) not null);")
cur.execute(create_table_adminpass)

#subject
create_table_subject=("create table if not exists subject(Subject_name varchar(30) not null primary key,\
                      course_code varchar(10) not null,\
                      exam_date date not null ,\
                      credit int(10));")
cur.execute(create_table_subject)


#subject_timings
create_table_timings=("create table if not exists timings(subject_name varchar(30) not null,\
                    section varchar(10),\
                    days varchar(10) not null,\
                    time_slot varchar(20) not null,\
                    instructor varchar(30));")
cur.execute(create_table_timings)

create_database=("create database if not exists Student_tt;")
cur.execute(create_database)


def admin():
    count=cur.execute("select * from adminpass;")
    if count==0:
        print('create new admin id as no id exists')
        admin_input(count)
        
    else:
        pas=input("Enter password: ")
        count=cur.execute("select * from adminpass;")
        global user2
        user1=[]
        user2=[]
        for i in cur:
            for j in range(0,count):
                username,password=i
                user1.append(i[1])
                user2.append(i[0])
                user2.append(i[1])
        if pas in user1:
            print('correct')
            admin_menu()
        elif pas != password:
            print('incorrect password')


def admin_menu():
    c='y'
    while c=='y' or c=='Y':
        print("1.Add/Remove admin")
        print("2.Subject details")
        print("3.Subject timings")
        print("4.Student Details")
        print("4.Exit")
        val=int(input('Enter choice: '))
        if val==1:
            print("Existing admins are:")
            cur.execute('select admin_name from adminpass;')
            for i in cur:
                print(i)
            print()
            print()            
            print("1. Add admin")
            print("2. Remove admin id")
            print("3. Exit")
            choice=int(input("Enter your choice: "))

            if choice==1:
                count=cur.execute("select * from admin_details;")
                admin_input(count)

            elif choice==2:
                del_input=input('Whose id do you want to remove: ')
                dele=("delete from adminpass where admin_name='"+del_input+"';")
                cur.execute(dele)
                timetable.commit()
                print('ADMIN DELETED!!')
                admin()

            else:
                print()

                

def subject_table():
    print("ENTER INTO Subject!")
    subject_name=input("Enter subject name to be added in the database: ")
    subject_code=input("Enter subject code: ")
    exam_date=input("Enter subject date: ")
    credit=input("Enter subject credits: ")
    use_database=("use time_table;")
    cur.execute(use_database)
    insert_subject=("insert into subject values('"+subject_name+"','"+subject_code+"','"+exam_date+"','"+credit+"');")
    cur.execute(insert_subject)
    timetable.commit()
    print("Subject added to the list!")
    
            
def timings():
    print("ENTER INTO Timings")
    subject_name=input("Enter subject name to be added in the database: ")
    section_name=input("Enter section code: ")
    days=input("Enter days for class(example = M,W,F): ")
    time_slot=input("Enter time slot for class on those days(in 24 hour format) example= 14 to 15: ")
    instructor=input("Enter name of instructor: ")
    insert_timings=("insert into timings values('"+subject_name+"','"+section_name+"','"+days+"','"+time_slot+"','"+instructor+"');")
    cur.execute(insert_timings)
    timetable.commit()
    print("Record added!")
    v=input("Add another section? (y/n): ")
    if v=='Y' or v=='y':
        timings()
    else:
        print()
    

def student_enroll():
    global student_id
    global student_name
    student_name=input("Enter student name: ")
    student_id=input("Enter student id: ")
    
    use_tt=("use student_tt;")
    cur.execute(use_tt)
    create_student=("create table if not exists "+student_id+"_tt(student_id varchar(20) not null primary key, student_name varchar(30) not null, subject_name varchar(20) not null, subject_code varchar(15) not null, section_number varchar(10) not null, days varchar(10) not null, timings varchar(10) not null);")
    cur.execute(create_student)
    print("Student added to the database!")
    enroll_subjects()
    

def admin_input(count):
    admin_name=input("Username: ")
    admin_pass=input("Password: ")
    insert_adminpass=("insert into adminpass values('"+admin_name+"','"+admin_pass+"');")
    cur.execute(insert_adminpass)
    timetable.commit()
    print('ADMIN ADDED!!')

def enroll_subjects():
    use_database=("use time_table;")
    global sub_name
    subcount=cur.execute("select * from timings;")
    k=[]
    print("Subjects you can choose from are: ")
    for i in cur:
        Subject_name,section,days,time_slot,instructor=i        
        print(i[0])
        k.append(i)
    sub_name=input("Enter subject name you want to enroll in: ")

    for i in k:
        sub_name=sub_name.lower()
        z=i[0].lower()        
        if sub_name==z:
            student_id=input("Enter your id: ")
            student_name=input("Enter name: ")    
            enroll(student_id,student_name)     
        else:
            continue
    print("Entered subject doesnt exist")


def enroll(student_id, student_name):
    
    coursecount=cur.execute("select * from subject;")
    k=[]
    for i in cur:
        subject_name,course_code,exam_date,credit=i
        if i[0]==sub_name:
            sub_code=i[1]
            break
        else:
            continue

    sub_sec = input("Enter section number you want to enroll for: ")
    
    subcount=cur.execute("select * from timings;")
    k=[]
    for i in cur:
        subject_name,section,days,time_slot,instructor=i
        if sub_sec==i[1]:
            sub_days=i[2]
            sub_time=i[3]
            break
        else:
            continue

    CheckForClash(student_id,sub_days,sub_time)

def CheckForClash(student_id,sub_days,sub_time):
    use_database=("use student_tt;")
    cur.execute(use_database)
    studcount=cur.execute("select * from "+student_id+"_tt;")
    k=[]
    for i in cur:
        student_id,student_name,subject_name,subject_code,section_number,days,timings=i
        k.append(i)
    s=sub_days.split(',')
    print(s)   


enroll_subjects()














    
