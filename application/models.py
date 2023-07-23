import flask
from application import db
from sqlalchemy import Column, Integer, String, Date, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from application import ma

class Users(db.Model):
    __tablename__ = "users"
    usr_id      = db.Column(String, primary_key=True) # DOC NUMBER
    usr_tip_doc	= db.Column(String) # DNI O CE O LOC
    usr_nom	    = db.Column(String) # NAME OR NAMES
    usr_ape_pat	= db.Column(String) # SURNAME
    usr_ape_mat	= db.Column(String) # MATERNAL SURNAME
    usr_emp	    = db.Column(String) # PARENT COMPANY
    usr_tel_cel	= db.Column(String) # PHONE NUMBER
    usr_dir	    = db.Column(String) # ADDRESS
    usr_cor_ele	= db.Column(String) # EMAIL
    usr_sta     = db.Column(String) # ACTIVITY STATUS
    usr_sta_mod = db.Column(String) # MODIFIER
    usr_sta_fec = db.Column(DateTime) # TIMESTAMP

    def __repr__(self):
        return self.toJSON()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(usr_id=id).first()
    
    def toDICT(self):
        cls_dict                = {}
        cls_dict['usr_id']      = self.usr_id
        cls_dict['usr_tip_doc'] = self.usr_tip_doc
        cls_dict['usr_nom']     = self.usr_nom
        cls_dict['usr_ape_pat'] = self.usr_ape_pat
        cls_dict['usr_emp']     = self.usr_emp
        cls_dict['usr_tel_cel'] = self.usr_tel_cel
        cls_dict['usr_dir']     = self.usr_dir
        cls_dict['usr_cor_ele'] = self.usr_cor_ele
        cls_dict['usr_sta']     = self.usr_sta
        cls_dict['usr_sta_mod'] = self.usr_sta_mod
        cls_dict['sta_fec']     = self.sta_fec
        # datetime.utcfromtimestamp(self.sa_fec).strftime('%Y-%m-%d')
        return cls_dict

    def toJSON(self):
        return self.toDICT()


class Vehicles(db.Model):
    __tablename__ = "vehicles"
    veh_lic_pla     = db.Column(String, primary_key=True) # LICENSE PLATE
    veh_usg         = db.Column(String) # USAGE TYPE
    veh_mar         = db.Column(String) # VEHICLE MAKE
    veh_mod         = db.Column(String) # VEHICLE MODEL 
    veh_yea         = db.Column(Integer) # VEHICLE YEAR OF FABRICATION
    veh_col         = db.Column(String) # VEHICLE COLOR
    veh_prop_snp    = db.Column(String) # VEHICLE OWNERS
    veh_usr_id      = db.Column(String) # DOCUMENT NUMBER
    veh_gps         = db.Column(String) # GPS AVAILABILITY
    veh_rev_tec     = db.Column(Date) # LAST TECHNICAL INSPECTION DATE
    veh_soa_seg     = db.Column(Date) # LAST SOAT INSURANCE DATE
    veh_seg_ctr     = db.Column(String) # INSURANCE EMITER NAME
    veh_seg_bro     = db.Column(String) # INSURANCE BROKER NAME
    veh_seg_nro     = db.Column(String) # INSURANCE POLICY NUMBER
    veh_seg_ini     = db.Column(Date) # LAST INSURANCE PAYMENT
    veh_sta         = db.Column(String) # ACTIVITY STATUS
    veh_sta_mod     = db.Column(String) # MODIFIER
    veh_sta_fec     = db.Column(DateTime) # TIMESTAMP

    def __repr__(self):
        return self.toJSON()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(veh_lic_pla=id).first()
    
    def toDICT(self):
        cls_dict                = {}
        cls_dict['veh_lic_pla'] = self.veh_lic_pla
        cls_dict['veh_usg']     = self.veh_usg
        cls_dict['veh_mar']     = self.veh_mar
        cls_dict['veh_mod']     = self.veh_mod
        cls_dict['veh_yea']     = self.veh_yea 
        cls_dict['veh_col']     = self.veh_col
        cls_dict['veh_prop_snp']= self.veh_prop_snp
        cls_dict['veh_usr_id']  = self.veh_usr_id
        cls_dict['veh_gps']     = self.veh_gps
        cls_dict['veh_rev_tec'] = self.veh_rev_tec
        cls_dict['veh_soa_seg'] = self.veh_soa_seg
        cls_dict['veh_seg_ctr'] = self.veh_seg_ctr
        cls_dict['veh_seg_bro'] = self.veh_seg_bro
        cls_dict['veh_seg_nro'] = self.veg_seg_nro
        cls_dict['veh_seg_ini'] = self.veh_seg_ini
        cls_dict['veh_sta']     = self.veh_sta
        cls_dict['veh_sta_mod'] = self.veh_sta_mod
        cls_dict['veh_sta_fec'] = self.veh_sta_fec
        # datetime.utcfromtimestamp(self.sa_fec).strftime('%Y-%m-%d')
        return cls_dict

    def toJSON(self):
        return self.toDICT()


class Editors(db.Model):
    __tablename__ = "editors"
    edt_usr_id  = db.Column(String, primary_key=True) # DOC NUMBER
    edt_usr_pwd = db.Column(String) # EDITOR'S PASSWORD
    edt_nom	    = db.Column(String) # NAME OR NAMES
    edt_ape_pat	= db.Column(String) # SURNAME
    edt_ape_mat	= db.Column(String) # MATERNAL SURNAME
    edt_sta     = db.Column(String) # ACTIVITY STATUS
    edt_sta_mod = db.Column(String) # MODIFIER
    edt_sta_fec = db.Column(DateTime) # TIMESTAMP
    
    def set_password(self, password):
        self.edt_usr_pwd = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.edt_usr_pwd, password)  
    
    def __repr__(self):
        return self.toJSON()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(edt_usr_id=id).first()
    
    def toDICT(self):
        cls_dict                = {}
        cls_dict['edt_usr_id']  = self.edt_usr_id
        cls_dict['edt_nom']     = self.edt_nom
        cls_dict['edt_ape_pat'] = self.edt_ape_pat
        cls_dict['edt_ape_mat'] = self.edt_ape_mat
        cls_dict['edt_sta']     = self.edt_sta
        cls_dict['edt_sta_mod'] = self.edt_sta_mod
        cls_dict['edt_sta_fec'] = self.edt_sta_fec
        return cls_dict

    def toJSON(self):
        return self.toDICT()
    
class Records(db.Model):
    __tablename__ = "records"
    rec_id      = db.Column(Integer, primary_key=True) # SERIAL ID
    rec_dat     = db.Column(Date) #RECORD DATE
    rec_veh_pla = db.Column(String) # LICENSE PLATE
    rec_veh_mix = db.Column(String(30)) # MIX OF MAKE AND MODEL
    rec_usr_id  = db.Column(String) # DOC NUMBER
    rec_usr_mix = db.Column(String) # MIX OF NAME AND PAT NAME
    rec_veh_loc = db.Column(String) # LOCATION
    rec_veh_des = db.Column(String) # COMMENTS FOR THE RECORD

    def __repr__(self):
        return self.toJSON()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def toDICT(self):
        cls_dict                = {}
        cls_dict['rec_dat']     = self.rec_dat
        cls_dict['rec_veh_pla'] = self.rec_veh_pla
        cls_dict['rec_veh_mix'] = self.rec_veh_mix
        cls_dict['rec_usr_id']  = self.rec_usr_id
        cls_dict['rec_usr_mix'] = self.rec_usr_mix
        cls_dict['rec_veh_loc'] = self.rec_veh_loc
        cls_dict['rec_veh_des'] = self.rec_veh_des
        return cls_dict

    def toJSON(self):
        return self.toDICT()
    
##################### Marshmallow objects ##############################
class UserSchema(ma.Schema):
    class Meta:
        fields = ('usr_id','usr_tip_doc','usr_nom','usr_ape_pat',
                  'usr_ape_mat','usr_emp','usr_tel_cel','usr_dir',
                  'usr_cor_ele')
        
class VehicleSchema(ma.Schema):
    class Meta:
        fields = ('veh_lic_pla','veh_usg','veh_mar','veh_mod','veh_yea',
                  'veh_col','veh_prop_snp','veh_usr_id','veh_gps',
                  'veh_rev_tec','veh_soa_seg','veh_seg_ctr',
                  'veh_seg_bro','veh_seg_nro','veh_seg_ini')
