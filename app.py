import psycopg2 # for database
from werkzeug import generate_password_hash, check_password_hash    # for saving passwords in hashed form

# connectivity to the database
conn = psycopg2.connect("dbname='hms' user='postgres' host='localhost' password='admin'")
cur = conn.cursor()


class Admin:
	def __init__(self,name,username,password):
		self.name=name
		self.username=username
		self.password=password
		hashed_password=generate_password_hash(self.password)
		val="insert into admin values(\'"+str(self.name)+"\',\'"+str(self.username)+"\',\'"+str(hashed_password)+"\')"
		cur.execute(val)
		conn.commit()


# creating class for student
class Student:
	rollno=130
	roomno=1
	laundryno=100
	batch="E6"
	def __init__(self,name,username,password,address,branch):
		self.name=name
		self.username=username
		self.password=password
		self.address=address
		self.branch=branch
		roll=Student.rollno
		room=Student.roomno
		laundry=Student.laundryno
		bat=Student.batch
		Student.rollno+=1
		Student.roomno+=1
		Student.laundryno+=1
		hashed_password=generate_password_hash(self.password)
		val="insert into users values(\'"+str(self.name)+"\',\'"+str(self.username)+"\',\'"+str(hashed_password)+"\',"+str(roll)+",\'"+str(self.address)+"\',"+str(room)+","+str(laundry)+",\'"+str(bat)+"\',\'"+str(self.branch)+"\')"
		cur.execute(val)
		conn.commit()
		val="insert into rooms values("+str(room)+",\'"+str(self.name)+"\',\'"+str(self.username)+"\',"+str(roll)+",\'"+str(self.branch)+"\')"
		cur.execute(val)
		conn.commit()

# creating class for Record
class Record:
	def __init__(self):
		pass


	def viewRoomRecord(self):
		print "                <<<<<<<<<----------Our Room Record---------->>>>>>>>>>"
		val="select * from rooms"
		cur.execute(val)
		rows=cur.fetchall()
		if rows==None:
			print "No records found !"
		else:
			print "RoomNo   Name                          Username                       RollNo     Branch"
			print "---------------------------------------------------------------------------------------"	
			for row in rows:
				ct=0
				for i in row:
					ct+=1
					if ct==2 or ct==5:
						print '      ',
					print i,
				print ''


	def viewStudentRecord(self):
		print "        <<<<<<<<----------Our Student Record---------->>>>>>>>>>"
		s=raw_input("Want to view full record (y/n):  ")
		if s=='y' or s=='Y':
			val="select * from users"
			cur.execute(val)
			rows=cur.fetchall()
			if rows==None:
				print "No Records Found !"
			else:
				print "Name                          Username                     rollno address                    roomno   laundryno     batch     branch"
				print "------------------------------------------------------------------------------------------------------------------------------------"	
				for row in rows:
					ct=0
					for i in row:
						ct+=1
						if ct!=3:
							if ct==7 or ct==8:
								print '      ',
							print i,
					print ''
		else:
			while 1:
				username=raw_input("Enter username of the student you want to view:  ")
				val="select * from users where username=\'"+username+"\'"
				cur.execute(val)
				row=cur.fetchone()
				if row==None:
					print "Username you entered doesnot exist!"
				else:
					print "Name                          Username                     rollno address                    roomno   laundryno     batch     branch"
					print "------------------------------------------------------------------------------------------------------------------------------------"	
					ct=0
					for i in row:
						ct+=1
						if ct!=3:
							if ct==7 or ct==8:
								print '      ',
							print i,
					print ''
				rt=raw_input("Press 1 to stop viewing!:  ")
				if rt=='1':
					break
				else:
					print "Enter another username"
					continue
		print "NOTE - If roomno = 0 means room not allocated "



	def deleteStudentRecord(self):
		print "         <<<<<<<<---------Delete Student Record---------->>>>>>>>>>"
		while 1:
			username=raw_input("Enter username you want to delete record !:    ")
			val="select * from users where username=\'"+username+"\'"
			cur.execute(val)
			row=cur.fetchone()
			if row==None:
				print "Username Doesnot exist!"
				break
			val="delete from users where username=\'"+username+"\'"
			cur.execute(val)
			conn.commit()
			val="delete from rooms where username=\'"+username+"\'"
			cur.execute(val)
			conn.commit()
			print "successfully deleted!"
			qw=raw_input("press 1 to delete more!")
			if qw!='1':
				break



	def deleteRoomRecord(self):
		print "         <<<<<<<<---------Delete Room Record---------->>>>>>>>>>"
		while 1:
			username=raw_input("Enter username you want to delete record !")
			val="select * from rooms where username=\'"+username+"\'"
			cur.execute(val)
			row=cur.fetchone()
			if row==None:
				print "Username Doesnot exist!"
				break
			val="delete from rooms where username=\'"+username+"\'"
			cur.execute(val)
			conn.commit()
			val="delete from users where username=\'"+username+"\'"
			cur.execute(val)
			conn.commit()
			print "successfully deleted!"
			qw=raw_input("press 1 to delete more!")
			if qw!='1':
				break



	def updateStudentRecord(self,typ):
		print "         <<<<<<<---------Update student record--------->>>>>>>>"
		if typ==1:
			print "You are admin"
			print "You cannot change - password,username,rollno,laundryno"

		else:
			print "You are student"
			print "You cannot change - username,rollno,laundryno,branch,roomno"
		username=raw_input("Enter username you want to update record !")
		val="select * from users where username=\'"+username+"\'"
		cur.execute(val)
		row=cur.fetchone()
		if row==None:
			print "Username Doesnot exist!"
		else:
			if typ==1:
				room=raw_input("want to change room no(y/n):  ")
				if room=="y" or room=="Y":
					roomno=raw_input("Enter room no:  ")
					roomno=int(roomno)
					val="update users set roomno="+str(roomno)+"where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					val="update rooms set roomno="+str(roomno)+"where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					print "successfully updated!"
				branch=raw_input("want to change branch(y/n):  ")
				if branch=="y" or branch=="Y":
					branch=raw_input("Enter branch:  ")
					val="update users set branch=\'"+str(branch)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					val="update rooms set branch=\'"+str(branch)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					print "successfully updated!"
				name=raw_input("want to change name(y/n):  ")
				if name=="y" or name=="Y":
					name=raw_input("Enter name:  ")
					val="update users set name=\'"+str(name)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					val="update rooms set name=\'"+str(name)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					print "successfully updated!"
			if typ==2:
				address=raw_input("want to change address(y/n):  ")
				if address=="y" or address=="Y":
					address=raw_input("Enter address:  ")
					val="update users set address=\'"+str(address)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					print "successfully updated!"
				name=raw_input("want to change name(y/n):  ")
				if name=="y" or name=="Y":
					name=raw_input("Enter name:  ")
					val="update users set name=\'"+str(name)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					val="update rooms set name=\'"+str(name)+"\' where username=\'"+username+"\'"
					cur.execute(val)
					conn.commit()
					print "successfully updated!"
				password=raw_input("want to change password(y/n):  ")
				if password=="y" or password=="Y":
					while 1:
						newpass1=raw_input("Enter new password:  ")
						newpass2=raw_input("Enter new password again:  ")
						if newpass1==newpass2:
							hashed_password=generate_password_hash(newpass1)
							val="update users set password=\'"+hashed_password+"\' where username=\'"+username+"\'"
							cur.execute(val)
							conn.commit()
							print "passwords successfully updated"
							break
						else:
							print "passwords do not match enter again"



	def updateRoomRecord(self):
		print "        <<<<<<<--------Update Room record--------->>>>>>>>"
		username=raw_input("Enter username you want to update record !")
		val="select * from rooms where username=\'"+username+"\'"
		cur.execute(val)
		row=cur.fetchone()
		if row==None:
			print "Username Doesnot exist!"
		else:
			print "NOTE - Username and rollno cannot be changed!"
			room=raw_input("want to change room no(y/n):  ")
			if room=="y" or room=="Y":
				roomno=raw_input("Enter room no:  ")
				roomno=int(roomno)
				val="update users set roomno="+str(roomno)+"where username=\'"+username+"\'"
				cur.execute(val)
				conn.commit()
				val="update rooms set roomno="+str(roomno)+"where username=\'"+username+"\'"
				cur.execute(val)
				conn.commit()
				print "successfully updated!"
			branch=raw_input("want to change branch(y/n):  ")
			if branch=="y" or branch=="Y":
				branch=raw_input("Enter branch:  ")
				val="update users set branch=\'"+str(branch)+"\' where username=\'"+username+"\'"
				cur.execute(val)
				conn.commit()
				val="update rooms set branch=\'"+str(branch)+"\' where username=\'"+username+"\'"
				cur.execute(val)
				conn.commit()
				print "successfully updated!"
			name=raw_input("want to change name(y/n):  ")
			if name=="y" or name=="Y":
				name=raw_input("Enter name:  ")
				val="update users set name=\'"+str(name)+"\' where username=\'"+username+"\'"
				cur.execute(val)
				conn.commit()
				val="update rooms set name=\'"+str(name)+"\' where username=\'"+username+"\'"
				cur.execute(val)
				conn.commit()
				print "successfully updated!"


def funType(typ):
	if typ==1:
		# admin
		pass
	else:
		# user
		s=raw_input("Already a member(y/n):")
		if s=='n' or s=='N':
			#print "Not Reg user"
			name=raw_input("Enter name:  ")
			username=raw_input("Enter username:  ")
			password=raw_input("Enter password:  ")
			address=raw_input("Enter address:  ")
			branch=raw_input("Enter branch:  ")
			s1=Student(name,username,password,address,branch)
			print "successfully Registered"
		else:
			#print "Reg user"
			flag=0
			username=raw_input("Enter your username:  ")
			val="select password from users where username=\'"+str(username)+"\'"
			cur.execute(val)
			row=cur.fetchone()
			if row==None:
				print "Username doesnot exist ! please Register first !"
			else:
				password=raw_input("Enter your password:  ")
				result=row[0].strip()
				if check_password_hash(result,password):
					flag=1
					print "You are now logged in !"
				else:
					print "Wrong password"
					qw=raw_input("Forgot password ?? Press 1 to update your password")
					if qw=="1":
						while 1:
							newpass1=raw_input("Enter new password:  ")
							newpass2=raw_input("Enter new password again:  ")
							if newpass1==newpass2:
								hashed_password=generate_password_hash(newpass1)
								val="update users set password=\'"+hashed_password+"\' where username=\'"+username+"\'"
								cur.execute(val)
								conn.commit()
								print "passwords successfully updated"
								break
							else:
								print "passwords do not match , enter again."
					else:
						pass



if __name__=='__main__':
	# asking for profession
	print "Welcome To Hostel Management System"
	print "Please enter admin credentials"
	name=raw_input("Enter name :  ")
	username=raw_input("Enter username :   ")
	password=raw_input("Enter password :   ")
	admin_username=username
	ad=Admin(name,username,password)
	while 1:
		print "--------------------------------------------------------------------------------------"
		print "                        <<<<<<<------------Main menu------------>>>>>>>>"
		print "--------------------------------------------------------------------------------------"
		print "1 - Enter Student record"
		print "2 - View Student record"
		print "3 - View Room record"
		print "4 - Delete Student record"
		print "5 - Delete Room record"
		print "6 - Update Student record"
		print "7 - Update Room record"
		print "8 - Exit"
		t=input()
		if t==1:
			while 1:
				print "Enter the type (in integer) of person (2 for Student):" 
				typ=input()
				if typ==2:
					print "You have access to our database to enter records!"
					break
				else:
					print 'You are not student , enter again!'
					continue
			if typ==2:
				funType(2)
		elif t==2:
			rec = Record()
			rec.viewStudentRecord()
		elif t==3:
			rec = Record()
			rec.viewRoomRecord()
		elif t==4:
			while 1:
				print "Enter the type (in integer) of person (1 for Admin):" 
				typ=input()
				if typ==1:
					passw=raw_input("Enter admin password:   ")
					val="select password from admin where username=\'"+admin_username+"\'"
					cur.execute(val)
					row=cur.fetchone()
					admin_pass=row[0].strip()
					if check_password_hash(admin_pass,passw):
						print "You have access to our database to enter records!"
						break
					else:
						print "passwords do not match!"
				else:
					print 'You are not admin , enter again!'
					continue
			if typ==1:
				rec = Record()
				rec.deleteStudentRecord()
		elif t==5:
			while 1:
				print "Enter the type (in integer) of person (1 for Admin):" 
				typ=input()
				if typ==1:
					passw=raw_input("Enter admin password:   ")
					val="select password from admin where username=\'"+admin_username+"\'"
					cur.execute(val)
					row=cur.fetchone()
					admin_pass=row[0].strip()
					if check_password_hash(admin_pass,passw):
						print "You have access to our database to enter records!"
						break
					else:
						print "passwords do not match!"
				else:
					print 'You are not admin , enter again!'
					continue
			if typ==1:
				rec=Record()
				rec.deleteRoomRecord()
		elif t==6:
			while 1:
				print "Enter the type (in integer) of person (1 for Admin) (2 for student):" 
				typ=input()
				if typ==1:
					passw=raw_input("Enter admin password:   ")
					val="select password from admin where username=\'"+admin_username+"\'"
					cur.execute(val)
					row=cur.fetchone()
					admin_pass=row[0].strip()
					if check_password_hash(admin_pass,passw):
						print "You have access to our database to enter records(as Admin)!"
						break
					else:
						print "passwords do not match!"
				if typ==2:
					print "You have access to our database to enter records as Student!"
					break
				else:
					print 'You are not admin or student , enter again!'
					continue
			rec = Record()
			rec.updateStudentRecord(typ)
		elif t==7:
			while 1:
				print "Enter the type (in integer) of person (1 for Admin):" 
				typ=input()
				if typ==1:
					passw=raw_input("Enter admin password:   ")
					val="select password from admin where username=\'"+admin_username+"\'"
					cur.execute(val)
					row=cur.fetchone()
					admin_pass=row[0].strip()
					if check_password_hash(admin_pass,passw):
						print "You have access to our database to enter records as Admin!"
						break
					else:
						print "passwords do not match"
				else:
					print 'You are not admin , enter again!'
					continue
			if typ==1:
				rec=Record()
				rec.updateRoomRecord()
		else:
			print "You are about to exit!"
			break