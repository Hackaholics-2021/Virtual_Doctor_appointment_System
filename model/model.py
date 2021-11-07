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

    def get_pending_status(self):
        s = text("select ConsultationId from booking_consultation where Status = :x")
        res=engine.execute(s,x="Pending").fetchone()
        if res:
            return res[0]
        else:
            return None

    