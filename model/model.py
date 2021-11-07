from sqlalchemy import *
from sqlalchemy.sql import *
engine=create_engine('mysql://root:admin@127.0.0.1:3306/virtualdoc',echo=True)

class Hackaholics:
    def __init__(self):
        self.meta=MetaData()
        self.doctor=Table("doctor",self.meta,autoload=True,autoload_with=engine)
        self.patient=Table("patient",self.meta,autoload=True,autoload_with=engine)
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

    def get_profile_doctor(self,id):
        s=self.doctor.select().where(self.doctor.c.Id==id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None
        
    def update_profile_doctor(self,id,data):
        s=self.doctor.update().where(self.doctor.c.Id==id).values(Name=data['Name'],Degree=data['Degree'],State=data['State'],District=data['District'],Firm=data['Firm'],Age=data['Age'],Experience=data['Experience'],Specialization=data['Specialization'],AboutMe=data['AboutMe'],Email=data['Email'],Password=data['Password'],LinkedIn=data['LinkedIn'],Facebook=data['Facebook'],Tamil=data['Tamil'],Malayalam=data['Malayalam'],Kannada=data['Kannada'],Telugu=data['Telugu'],Hindi=data['Hindi'],English=data['English'],Gender=data['Gender'])
        res=engine.execute(s)
        return res

    def get_patients(self,id):
        s=text("select DISTINCT PId,PName from booking_appointment where DId= :x")
        res=engine.execute(s,x=id).fetchall()
        results=[dict(r) for r in res] if res else None
        
        if results:
            for i in results:
                print(i['PId'],i['PName'])
            print(results)
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

        if result1 and result2 and result3:
            return result1,result2,result3


