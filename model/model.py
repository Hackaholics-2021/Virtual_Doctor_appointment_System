from sqlalchemy import *
from sqlalchemy.sql import *
from datetime import date
engine=create_engine('mysql://root:admin@127.0.0.1:3306/virtualdoc',echo=True)

class Hackaholics:
    def __init__(self):
        self.meta=MetaData()
        self.doctor=Table("doctor",self.meta,autoload=True,autoload_with=engine)
        self.patient=Table("patient",self.meta,autoload=True,autoload_with=engine)
        self.diagnostics=Table("diagnostics",self.meta,autoload=True,autoload_with=engine)
        self.booking_appointment=Table("booking_appointment",self.meta,autoload=True,autoload_with=engine)
        self.booking_consultation=Table("booking_consultation",self.meta,autoload=True,autoload_with=engine)
        self.prescription=Table("prescription",self.meta,autoload=True,autoload_with=engine)

    def insert_into_patient(self,data):
        res=engine.execute(self.patient.insert(),data)
        if res:
            return res
        else:
            return None

    def insert_into_doctor(self,data):
        res=engine.execute(self.doctor.insert(),data)
        if res:
            return res
        else:
            return None

    def insert_into_diagnostics(self,id):
        res=engine.execute(self.doctor.insert().values(Id = id))
        if res:
            return res
        else:
            return None

    def insert_into_booking(self,data):
        res=engine.execute(self.booking_appointment.insert(),data)
        if res:
            return res
        else:
            return None

    def insert_prescription_info(self,data):
        res=engine.execute(self.prescription.insert(),data)
        if res:
            return res
        else:
            return None

    def get_email_patient(self,email):
        s=self.patient.select().where(self.patient.c.Email==email)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def get_email_doctor(self,email):
        s=self.doctor.select().where(self.doctor.c.Email==email)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def get_info_patient(self,id):
        s=self.patient.select().where(self.patient.c.Id==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def get_info_doctor(self,id):
        s=self.doctor.select().where(self.doctor.c.Id==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def get_info_appointment(self,id):
        s=self.booking_appointment.select().where(self.booking_appointment.c.AppointmentId==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def get_prescription_info(self,id):
        s=self.prescription.select().where(self.prescription.c.PId==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results
        else:
            return None

    def get_cancelled_appointment_info(self,id):
        s = text("select * from booking_appointment where PId = :x and Status = 'Cancelled'")
        
        res=engine.execute(s,x=id)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def insert_consult_info(self,data):
        res=engine.execute(self.booking_consultation.insert(),data)
        if res:
            return res
        else:
            return None

    def update_consult_status(self,consult_id):
        stmt = self.booking_consultation.update().where(self.booking_consultation.c.ConsultationId == consult_id).values(Status = "Closed")
        res = engine.execute(stmt)
        if res:
            print("UPDATED STATUS")
            return res
        else:
            return None

    def update_doctor_rating(self,rating,doc_id):
        stmt = self.doctor.update().where(self.doctor.c.Id == doc_id).values(Rating = rating)
        res = engine.execute(stmt)
        if res:
            return res
        else:
            return None

    def update_profile_patient(self,id,data):
        stmt = self.patient.update().where(self.patient.c.Id == id).values(data)
        res = engine.execute(stmt)
        if res:
            return res
        else:
            return None

    def update_diagnostics(self,id,data):
        stmt = self.diagnostics.update().where(self.diagnostics.c.Id == id).values(data)
        res = engine.execute(stmt)
        if res:
            return res
        else:
            return None

    def update_booking_info(self,time,date,appointment_id):
        stmt = self.booking_appointment.update().where(self.booking_appointment.c.AppointmentId == appointment_id).values(Time = time,BookingDate = date)
        res = engine.execute(stmt)
        if res:
            return res
        else:
            return None

    def update_appointment_info_status(self,appointment_id):
        stmt = self.booking_appointment.update().where(self.booking_appointment.c.AppointmentId == appointment_id).values(Status = 'Completed')
        res = engine.execute(stmt)
        if res:
            return res
        else:
            return None

    def get_pending_status(self):
        s = text("select ConsultationId from booking_consultation where Status = :x")
        res=engine.execute(s,x="Pending").fetchone()
        if res:
            return res[0]
        else:
            return None

    def get_consult_info(self,id):
        s=self.booking_consultation.select().where(self.booking_consultation.c.PId==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_appointment_info(self,id):
        s=self.booking_appointment.select().where(self.booking_appointment.c.PId==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_info_diagnostics(self,id):
        s=self.diagnostics.select().where(self.diagnostics.c.Id==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results[0]
        else:
            return None

    def get_email_doctor_filter_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            return results
        else:
            return None

    def get_email_doctor_rating_lth_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y order by Rating asc")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            return results
        else:
            return None


    def get_email_doctor_rating_htl_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y order by Rating desc")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            return results
        else:
            return None

    def get_email_doctor_experience_htl_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y order by Experience desc")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            print("Results ",results)
            return results
        else:
            return None
    def get_email_doctor_experience_lth_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y order by Experience asc")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            print("Results ",results)
            return results
        else:
            return None

    def get_email_doctor_male_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and Gender = 'Male'")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            return results
        else:
            return None

    def get_email_doctor_female_consult(self,email_addresses,Language,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and Gender = 'Female'")
        res=engine.execute(s,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        for i in range(len(res)):
            for j in email_addresses:
                if i>=0 and res[i]['Email'] == j and res[i][Language]==1:
                    results.append(res[i])
        if results:
            return results
        else:
            return None

    def get_email_doctor_filter_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :m and District = :l")
        res=engine.execute(s,y=Specialization,m=State,l=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_rating_lth_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :l and District = :m order by Rating asc")
        res=engine.execute(s,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_rating_htl_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :l and District = :m order by Rating desc")
        res=engine.execute(s,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_experience_htl_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :l and District = :m order by Experience desc")
        res=engine.execute(s,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_experience_lth_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :l and District = :m order by Experience asc")
        res=engine.execute(s,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_male_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :l and District = :m and Gender = 'Male'")
        res=engine.execute(s,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_female_booking(self,State,District,Specialization):
        res=[]
        s = text("select * from doctor where  Specialization = :y and State = :l and District = :m and Gender = 'Female'")
        res=engine.execute(s,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results)
            return results
        else:
            return None

    
        
    def update_profile_doctor(self,id,data):
        s=self.doctor.update().where(self.doctor.c.Id==id).values(Name=data['Name'],Degree=data['Degree'],State=data['State'],District=data['District'],Firm=data['Firm'],Age=data['Age'],Experience=data['Experience'],Specialization=data['Specialization'],AboutMe=data['AboutMe'],Email=data['Email'],Password=data['Password'],LinkedIn=data['LinkedIn'],Facebook=data['Facebook'],Tamil=data['Tamil'],Malayalam=data['Malayalam'],Kannada=data['Kannada'],Telugu=data['Telugu'],Hindi=data['Hindi'],English=data['English'],Gender=data['Gender'])
        res=engine.execute(s)
        return res

    def get_patients(self,id):
        s=text("select DISTINCT PId,PName from booking_appointment where DId= :x ")
        res=engine.execute(s,x=id).fetchall()
        results=[dict(r) for r in res] if res else None
        
        if results:
            return results
        else:
            return None

    def get_patient_details(self,PId,DId):
        s1=text("select * from patient where Id= :x")
        res1=engine.execute(s1,x=PId).fetchall()
        result1=[dict(r1) for r1 in res1] if res1 else None

        s2=text("select * from diagnostics where Id= :x")
        res2=engine.execute(s2,x=PId).fetchall()
        result2=[dict(r2) for r2 in res2] if res2 else None

        s3=text("select * from booking_appointment where PId= :x and DId= :y")
        res3=engine.execute(s3,x=PId,y=DId).fetchall()
        result3=[dict(r3) for r3 in res3] if res3 else None
        
        if result1!=None and result2!=None and result3!=None:            
            return result1,result2,result3
        
        else:
            return None,None,None


    def get_new_upcoming_details(self,id):
        today=date.today()
        s=text("select * from booking_appointment where DId= :x and BookingDate >= :y and Status='Pending'")
        res=engine.execute(s,x=id,y=today)
        result=[dict(r) for r in res] if res else None
        if result:
            return result
        else:
            return None

    def get_accepted_upcoming_details(self,id):
        today=date.today()
        s=text("select * from booking_appointment where DId= :x and BookingDate > :y and Status='Accepted'")
        res=engine.execute(s,x=id,y=today)
        result=[dict(r) for r in res] if res else None
        if result:
            return result
        else:
            return None

    def cancel_appointment(self,bid):
        s=text("update booking_appointment set Status='Cancelled' where AppointmentId= :x")
        res=engine.execute(s,x=bid)
        return None

    def get_cancel_patient_email(self,bid):
        mail=text("select PEmail from booking_appointment where AppointmentId= :x")
        email=engine.execute(mail,x=bid)
        result=[dict(r) for r in email] if email else None
        if result:
            return result[0]
        else:
            return None

    def get_appointment(self,bid):
        s=text("select * from booking_appointment where AppointmentId= :x")
        res=engine.execute(s,x=bid)
        result=[dict(r) for r in res] if res else None
        if result:
            return result[0]
        else:
            return None

    def accept_appointment(self,bid):
        s=text("update booking_appointment set Status='Accepted' where AppointmentId= :x")
        res=engine.execute(s,x=bid)
        return None
        

    def get_todays_appointment(self,id):
        today=date.today()
        s=text("select * from booking_appointment where DId= :x and Status='Accepted'and BookingDate= :y ")
        res=engine.execute(s,x=id,y=today)
        no=0
        result=[]
        if res:
            for r in res:
                no=no+1
                result.append(r)
        #result=[dict(r) for r in res] if res else None
        if result!=None:
            print(result)
            return result,no
        else:
            return None

    def get_todays_appointment_patient(self,id):
        today=date.today()
        s=text("select * from booking_appointment where PId= :x and Status='Accepted'and BookingDate= :y ")
        res=engine.execute(s,x=id,y=today)
        result=[]
        if res:
            for r in res:
                result.append(r)
        #result=[dict(r) for r in res] if res else None
        if result!=None:
            print("result",result,today)
            return result
        else:
            return None

    def get_consultations(self,id):
        today=date.today()
        s=text("select * from booking_consultation where DId= :x and Status='Pending' and  ConsultationDate= :y")
        res=engine.execute(s,x=id,y=today)
        no=0
        result=[]
        if res:
            for r in res:
                no=no+1
                result.append(r)
        #result=[dict(r) for r in res] if res else None
        if result!=None:
            print(result,no)
            return result,no
        else:
            return None

    def get_history_appointments(self,id):
        s=text("select * from booking_appointment where DId= :x and Status='Completed' order by BookingDate desc")
        res=engine.execute(s,x=id)
        result=[dict(r) for r in res] if res else None
        if result:
            return result
        else:
            return None

    def get_history_consultations(self,id):
        s=text("select * from booking_consultation where DId= :x and Status='Completed' order by ConsultationDate desc")
        res=engine.execute(s,x=id)
        result=[dict(r) for r in res] if res else None
        if result:
            return result
        else:
            return None

    def get_prescription(self,bid):
        s=text("select * from prescription where BId=:x")
        res=engine.execute(s,x=bid)
        result=[dict(r) for r in res] if res else None
        if result:
            return result
        else:
            return None
