from sqlalchemy import *
from sqlalchemy.sql import *
engine=create_engine('mysql://root:admin@127.0.0.1:3306/virtualdoc',echo=True)

class Hackaholics:
    def __init__(self):
        self.meta=MetaData()
        self.patient=Table("patient",self.meta,autoload=True,autoload_with=engine)
        self.doctor=Table("doctor",self.meta,autoload=True,autoload_with=engine)
        self.diagnostics=Table("diagnostics",self.meta,autoload=True,autoload_with=engine)
        self.booking_appointment=Table("booking_appointment",self.meta,autoload=True,autoload_with=engine)
        self.booking_consultation=Table("booking_consultation",self.meta,autoload=True,autoload_with=engine)

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

    def update_booking_info(self,time,date,appointment_id):
        stmt = self.booking_appointment.update().where(self.booking_appointment.c.AppointmentId == appointment_id).values(Time = time,BookingDate = date)
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

    def get_email_doctor_filter_consult(self,email_addresses,Language,Specialization):
        s = text("select * from doctor where Email in :x and Specialization = :y")
        res=engine.execute(s,x = email_addresses,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results=[dict(r) for r in res] if res else None
        ans = []
        if results:
            print(results)
            for i in range(len(results)):
                if results[i][Language] == 1:
                    ans.append(results[i])
        if ans:
            return ans
        else:
            return None

    def get_email_doctor_rating_lth_consult(self,email_addresses,Language,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y order by Rating desc")
            res.append(engine.execute(s,x = i,y=Specialization).fetchall())
        print(res,Language,Specialization)
        results = []
        ans=[]
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            print(results)
            for i in range(len(results)):
                if results[i][0][Language] == 1:
                    ans.append(results[i][0])
        
        if ans:
            return ans
        else:
            return None


    def get_email_doctor_rating_htl_consult(self,email_addresses,Language,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y order by Rating desc")
            res.append(engine.execute(s,x = i,y=Specialization).fetchall())
        print(res,Language,Specialization)
        results = []
        ans=[]
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            print(results)
            for i in range(len(results)):
                if results[i][0][Language] == 1:
                    ans.append(results[i][0])
        
        if ans:
            return ans
        else:
            return None

    def get_email_doctor_experience_htl_consult(self,email_addresses,Language,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y order by Experience desc")
            res.append(engine.execute(s,x = i,y=Specialization).fetchall())
        print(res,Language,Specialization)
        results = []
        ans=[]
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            print(results)
            for i in range(len(results)):
                if results[i][0][Language] == 1:
                    ans.append(results[i][0])
        
        if ans:
            return ans
        else:
            return None

    def get_email_doctor_experience_lth_consult(self,email_addresses,Language,Specialization):
        s = text("select * from doctor where Email in :x and Specialization = :y order by Experience asc")
        res = engine.execute(s,x = email_addresses,y=Specialization).fetchall()
        print(res,Language,Specialization)
        results = []
        ans=[]
        results.append([dict(r) for r in res]) if res else None
        if results:
            print(results)
            for i in range(len(results[0])):
                if results[0][i][Language] == 1:
                    ans.append(results[0][i])
        if ans:
            return ans
        else:
            return None

    def get_email_doctor_male_consult(self,email_addresses,Language,Specialization):
        s = text("select * from doctor where Email in :x and Specialization = :y and Gender = :z")
        res=engine.execute(s,x = email_addresses,y=Specialization,z="Male").fetchall()
        print(res,Language,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results[0])
            if results[0][Language] == 1:
                return results[0]
        else:
            return None

    def get_email_doctor_female_consult(self,email_addresses,Language,Specialization):
        s = text("select * from doctor where Email in :x and Specialization = :y and Gender = :z")
        res=engine.execute(s,x = email_addresses,y=Specialization,z="Female").fetchall()
        print(res,Language,Specialization)
        results=[dict(r) for r in res] if res else None
        if results:
            print(results[0])
            if results[0][Language] == 1:
                return results[0]
        else:
            return None

    def get_email_doctor_filter_booking(self,email_addresses,State,District,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y and State = :l and District = :m")
            res.append(engine.execute(s,x = i,y=Specialization,l=State,m=District).fetchall())
        print(res,State,Specialization)
        results = []
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_rating_lth_booking(self,email_addresses,State,District,Specialization):
        s = text("select * from doctor where Email in :x and Specialization = :y and State = :l and District = :m order by cast(Rating as int) asc")
        res = engine.execute(s,x = email_addresses,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results = []
        ans=[]
        results.append([dict(r) for r in res]) if res else None
        if results:
            return results
        else:
            return None

    def get_email_doctor_rating_htl_booking(self,email_addresses,State,District,Specialization):
        s = text("select * from doctor where Email in :x and Specialization = :y and State = :l and District = :m order by cast(Rating as int) desc")
        res = engine.execute(s,x = email_addresses,y=Specialization,l=State,m=District).fetchall()
        print(res,State,Specialization)
        results = []
        ans=[]
        results.append([dict(r) for r in res]) if res else None
        if results:
            return results
        else:
            return None

    def get_email_doctor_experience_htl_booking(self,email_addresses,State,District,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y and State = :l and District = :m order by cast(Experience as int) desc")
            res.append(engine.execute(s,x = i,y=Specialization,l=State,m=District).fetchall())
        print(res,State,Specialization)
        results = []
        ans=[]
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            return results
        else:
            return None

    def get_email_doctor_experience_lth_booking(self,email_addresses,State,District,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y and State = :l and District = :m order by cast(Experience as int) asc")
            res.append(engine.execute(s,x = i,y=Specialization,l=State,m=District).fetchall())
        print(res,State,Specialization)
        results = []
        ans=[]
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            return results
        else:
            return None

    def get_email_doctor_male_booking(self,email_addresses,State,District,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y and Gender = :z and State = :l and District = :m")
            res.append(engine.execute(s,x = i,y=Specialization,z="Male",l=State,m=District).fetchall())
        print(res,State,Specialization)
        results = []
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            print(results)
            return results
        else:
            return None

    def get_email_doctor_female_booking(self,email_addresses,State,District,Specialization):
        res=[]
        for i in email_addresses:
            s = text("select * from doctor where Email = :x and Specialization = :y and Gender = :z and State = :l and District = :m")
            res.append(engine.execute(s,x = i,y=Specialization,z="Female",l=State,m=District).fetchall())
        print(res,State,Specialization)
        results = []
        for i in res:
            if len(i)>0:
                results.append([dict(r) for r in i])
        if results:
            print(results)
            return results
        else:
            return None

    