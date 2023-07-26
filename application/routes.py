from application import db, app
from application.models import Vehicles, Users, Editors
from flask import render_template, request, json, jsonify, Response
from flask import redirect, url_for, flash, session
from application.forms import LoginForm, RegisterForm
from application.models import Users, Vehicles, Records
from application.models import UserSchema, VehicleSchema, RecordSchema
from datetime import datetime

########################### WEB SECTION ################################

@app.route('/', methods=['GET','POST']) # You have to put the methods
@app.route('/login', methods=['GET','POST']) # on all routes
def login():
    if session.get('edt_nom'):
        return redirect(url_for('inicio'))

    form = LoginForm()

    if form.validate_on_submit():
        editor_id   = form.editor.data
        password    = form.password.data

        editor = Editors.query.filter_by(edt_usr_id=editor_id).first()
        if editor and editor.get_password(password):
            flash(f"{editor.edt_nom}, te logeaste con éxito!", "success")
            session['edt_usr_id'] = editor.edt_usr_id
            session['edt_nom'] = editor.edt_nom
            return redirect("/inicio")
        else:
            flash("No pudimos hacer login. Revise su contraseña","danger")
    return render_template("login.html", 
                           title="Login", 
                           form=form, 
                           login=True )

@app.route('/inicio')
def inicio():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    return render_template('inicio.html', inicio=True)

@app.route('/flota')
def flota():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    flota = Vehicles.query.filter_by(veh_sta='ACTIVO').order_by("veh_usg")
    db.session.commit()
    return render_template('flota.html', 
                           flotaTable=flota, 
                           flota=True)

@app.route('/usuarios')
def usuarios():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    usuarios = Users.query.filter_by(usr_sta='ACTIVO').order_by("usr_id")
    db.session.commit()
    return render_template('usuarios.html', 
                           usuariosTable=usuarios, 
                           usuarios=True)

@app.route('/movimiento')
def movimiento():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    records = Records.query.filter_by(rec_sta='ACTIVO').order_by("rec_dat")
    db.session.commit()
    return render_template('movimiento.html', 
                           recordsTable=records, 
                           records=True)

@app.route("/logout")
def logout():
    session['edt_usr_id']=False
    session.pop('edt_nom',None)
    return redirect(url_for('login'))

@app.route("/registro", methods=['POST','GET'])
def registro():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    form = RegisterForm()

    if form.validate_on_submit():
        editor_id   = form.editor.data
        password    = form.password.data
        first_name  = form.first_name.data
        pat_name    = form.pat_name.data
        mat_name    = form.mat_name.data
        now_dt      = datetime.now()

        editor = Editors(edt_usr_id=editor_id, 
                         edt_nom=first_name, 
                         edt_ape_pat=pat_name,
                         edt_ape_mat=mat_name,
                         edt_sta='ACTIVO',
                         edt_sta_mod='ADM',
                         edt_sta_fec=now_dt)
        
        editor.set_password(password)
        db.session.add(editor)
        db.session.commit()
        flash("Usted se registro exitosamente!","success")
        return redirect(url_for('inicio'))
    return render_template("registro.html", 
                           title="Registro", 
                           form=form, registro=True)

############################ API SECTION ###############################

user_schema = UserSchema()
users_schema = UserSchema(many=True)
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

# Users
@app.route('/apiadduser', methods=['POST'])
def apiadduser():
    if session.get('edt_nom') and request.method=='POST':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt      = datetime.now()
        # Retrieve form info
        id      = request.form.get('usr_id')
        docum   = request.form.get('usr_tip_doc')
        nombre  = request.form.get('usr_nom')
        apepat  = request.form.get('usr_ape_pat')
        apemat  = request.form.get('usr_ape_mat')
        empresa = request.form.get('usr_emp')
        telef   = request.form.get('usr_tel_cel')
        direc   = request.form.get('usr_dir') 
        email   = request.form.get('usr_cor_ele')

        # Check if user id is only numbers
        if not id.isdigit():
            flash("Código de usuario debe ser sólo números","Danger")
            return redirect(url_for("usuarios"))

        # Detect user
        user_rs = Users.query.filter_by(usr_id=id).first()

        # In case the user exists, exit, otherwise proceed
        if user_rs:
            user_ck = Users.query.filter_by(usr_id=id,usr_sta='ACTIVO').first()
            if user_ck:
                flash("Usuario ya existe","danger")
                return redirect(url_for('usuarios'))
            else:
                Users.query.filter_by(usr_id=id).update(dict(
                    usr_tip_doc = docum.upper(),
                    usr_nom     = nombre.upper(),
                    usr_ape_pat = apepat.upper(),
                    usr_ape_mat = apemat.upper(),
                    usr_emp     = empresa.upper(),
                    usr_tel_cel = telef,
                    usr_dir     = direc.upper(), 
                    usr_cor_ele = email.upper(),
                    usr_sta     = 'ACTIVO',
                    usr_sta_mod = curr_editor.upper(),
                    usr_sta_fec = now_dt))
                db.session.commit()
                flash("Usuario añadido con éxito","success")
                return redirect(url_for('usuarios'))           
        else:
            user = Users(
                usr_id      = id,
                usr_tip_doc = docum.upper(),
                usr_nom     = nombre.upper(),
                usr_ape_pat = apepat.upper(),
                usr_ape_mat = apemat.upper(),
                usr_emp     = empresa.upper(),
                usr_tel_cel = telef,
                usr_dir     = direc.upper(), 
                usr_cor_ele = email.upper(),
                usr_sta     ='ACTIVO',
                usr_sta_mod =curr_editor.upper(),
                usr_sta_fec =now_dt)
            db.session.add(user)
            db.session.commit()
            flash("Usuario añadido con éxito", "success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

@app.route('/apiedituser', methods=['POST'])
def apiedituser():
    if session.get('edt_nom') and request.method=='POST':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt      = datetime.now()
        # Retrieve form info
        id      = request.form.get('usr_id')
        docum   = request.form.get('usr_tip_doc')
        nombre  = request.form.get('usr_nom')
        apepat  = request.form.get('usr_ape_pat')
        apemat  = request.form.get('usr_ape_mat')
        empresa = request.form.get('usr_emp')
        telef   = request.form.get('usr_tel_cel')
        direc   = request.form.get('usr_dir') 
        email   = request.form.get('usr_cor_ele')

        # Detect user
        user_rs = Users.query.filter_by(usr_id=id,usr_sta='ACTIVO').first()
        db.session.commit()
        if not user_rs:
            flash("No se pudo actualizar","danger")
            return redirect(url_for('usuarios'))
        else:
            Users.query.filter_by(usr_id=id).update(dict(
                usr_tip_doc = docum.upper(),
                usr_nom     = nombre.upper(),
                usr_ape_pat = apepat.upper(),
                usr_ape_mat = apemat.upper(),
                usr_emp     = empresa.upper(),
                usr_tel_cel = telef,
                usr_dir     = direc.upper(), 
                usr_cor_ele = email.upper(),
                usr_sta     = 'ACTIVO',
                usr_sta_mod = curr_editor.upper(),
                usr_sta_fec = now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

@app.route('/apideactivateuser/<string:id>', methods=['GET'])
def apideactivateuser(id):
    if session.get('edt_nom') and request.method=='GET':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt      = datetime.now()

        # Verify if user exists
        user_rs = Users.query.filter_by(usr_id=id,usr_sta='ACTIVO').first()
        if not user_rs:
            flash("No se pudo borrar","danger")
            return redirect(url_for('usuarios'))
        else:
            Users.query.filter_by(usr_id=id).update(dict(
                usr_sta     = 'INACTIVO',
                usr_sta_mod = curr_editor.upper(),
                usr_sta_fec = now_dt))
            db.session.commit()
            flash("Usuario eliminado","success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

# Vehicles
@app.route('/apiaddvehicle', methods=['POST'])
def apiaddvehicle():
    if session.get('edt_nom') and request.method=='POST':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt      = datetime.now()
        # Retrieve form info
        id      = request.form.get('veh_lic_pla')
        usage   = request.form.get('veh_usg')
        marca   = request.form.get('veh_mar')
        modelo  = request.form.get('veh_mod')
        anio    = request.form.get('veh_yea')
        vcolor  = request.form.get('veh_col')
        vprop   = request.form.get('veh_prop_snp')
        usuario = request.form.get('veh_usr_id')
        vgps    = request.form.get('veh_gps')
        revtec  = request.form.get('veh_rev_tec',None)
        soatseg = request.form.get('veh_soa_seg')
        segctr  = request.form.get('veh_seg_ctr',None)
        segbro  = request.form.get('veh_seg_bro',None)
        segnro  = request.form.get('veh_seg_nro',None)
        segini  = request.form.get('veh_seg_ini',None)

        # Ensure there is data there
        if request.form['veh_rev_tec'] =='' or request.form['veh_rev_tec'] is None:
            revtec = None
        else:
            revtec = request.form['veh_rev_tec']
        if request.form['veh_seg_ini'] =='' or request.form['veh_seg_ini'] is None:
            segini = None
        else:
            segini = request.form['veh_seg_ini']

        # Detect vehicle and user
        usr_rs = Users.query.filter_by(usr_id=usuario,usr_sta='ACTIVO').first()
        veh_rs = Vehicles.query.filter_by(veh_lic_pla=id.upper()).first()
        # Reroute if user doesn't exist
        if not usr_rs:
            flash("Usuario no existe","danger")
            return redirect(url_for('flota'))
        # Detect vehicle, then if vehicle is active to proceed
        if veh_rs:
            veh_ck = Vehicles.query.filter_by(veh_lic_pla=id.upper(),veh_sta='ACTIVO').first()
            if veh_ck:
                flash("Vehiculo ya existe","danger")
                return redirect(url_for('flota'))
            else:
                Vehicles.query.filter_by(veh_lic_pla=id.upper()).update(dict(
                    veh_usg     = usage.upper(),
                    veh_mar     = marca.upper(),
                    veh_mod     = modelo.upper(),
                    veh_yea     = anio,
                    veh_col     = vcolor.upper(),
                    veh_prop_snp= vprop.upper(),
                    veh_usr_id  = usuario, 
                    veh_gps     = vgps.upper(),
                    veh_rev_tec = revtec,
                    veh_soa_seg = soatseg,
                    veh_seg_ctr = segctr.upper(),
                    veh_seg_bro = segbro.upper(),
                    veh_seg_nro = segnro,
                    veh_seg_ini = segini,
                    veh_sta     = 'ACTIVO',
                    veh_sta_mod = curr_editor.upper(),
                    veh_sta_fec = now_dt))
                db.session.commit()
                flash("Vehiculo añadido con éxito","success")
                return redirect(url_for('flota'))
        else:
            vehicle = Vehicles(
                veh_lic_pla = id.upper(),
                veh_usg     = usage.upper(),
                veh_mar     = marca.upper(),
                veh_mod     = modelo.upper(),
                veh_yea     = anio,
                veh_col     = vcolor.upper(),
                veh_prop_snp= vprop.upper(),
                veh_usr_id  = usuario, 
                veh_gps     = vgps.upper(),
                veh_rev_tec = revtec,
                veh_soa_seg = soatseg,
                veh_seg_ctr = segctr.upper(),
                veh_seg_bro = segbro.upper(),
                veh_seg_nro = segnro,
                veh_seg_ini = segini,
                veh_sta     = 'ACTIVO',
                veh_sta_mod = curr_editor.upper(),
                veh_sta_fec = now_dt)
            db.session.add(vehicle)
            db.session.commit()
            flash("Vehículo añadido con éxito", "success")
            return redirect(url_for('flota'))
    else:
        redirect(url_for('login'))

@app.route('/apieditvehicle', methods=['POST'])
def apieditvehicle():
    if session.get('edt_nom') and request.method=='POST':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt      = datetime.now()
        # Retrieve form info
        id      = request.form.get('veh_lic_pla')
        usage   = request.form.get('veh_usg')
        marca   = request.form.get('veh_mar')
        modelo  = request.form.get('veh_mod')
        anio    = request.form.get('veh_yea')
        vcolor  = request.form.get('veh_col')
        vprop   = request.form.get('veh_prop_snp')
        usuario = request.form.get('veh_usr_id')
        vgps    = request.form.get('veh_gps')
        revtec  = request.form.get('veh_rev_tec',None)
        soatseg = request.form.get('veh_soa_seg')
        segctr  = request.form.get('veh_seg_ctr',None)
        segbro  = request.form.get('veh_seg_bro',None)
        segnro  = request.form.get('veh_seg_nro',None)
        segini  = request.form.get('veh_seg_ini',None)

        # Ensure there is data there
        if request.form['veh_rev_tec'] =='' or request.form['veh_rev_tec'] is None:
            revtec = None
        else:
            revtec = request.form['veh_rev_tec']
        if request.form['veh_seg_ini'] =='' or request.form['veh_seg_ini'] is None:
            segini = None
        else:
            segini = request.form['veh_seg_ini']
        
        # Detect vehicle and user
        usr_rs = Users.query.filter_by(usr_id=usuario,usr_sta='ACTIVO').first()
        veh_rs = Vehicles.query.filter_by(veh_lic_pla=id.upper(),veh_sta='ACTIVO').first()
        # Reroute if user doesn't exist
        if not usr_rs:
            flash("Usuario no existe","danger")
            return redirect(url_for('flota'))
        if not veh_rs:
            flash("No se pudo actualizar","danger")
            return redirect(url_for('flota'))
        else:
            Vehicles.query.filter_by(veh_lic_pla=id.upper()).update(dict(
                veh_usg     = usage.upper(),
                veh_mar     = marca.upper(),
                veh_mod     = modelo.upper(),
                veh_yea     = anio,
                veh_col     = vcolor.upper(),
                veh_prop_snp= vprop.upper(),
                veh_usr_id  = usuario, 
                veh_gps     = vgps.upper(),
                veh_rev_tec = revtec,
                veh_soa_seg = soatseg,
                veh_seg_ctr = segctr.upper(),
                veh_seg_bro = segbro.upper(),
                veh_seg_nro = segnro,
                veh_seg_ini = segini,
                veh_sta     = 'ACTIVO',
                veh_sta_mod = curr_editor.upper(),
                veh_sta_fec = now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('flota'))
    else:
        redirect(url_for('login'))

@app.route('/apideactivatevehicle/<string:id>', methods=['GET'])
def apideactivatevehicle(id):
    if session.get('edt_nom') and request.method=='GET':
        # Basic data
        now_dt      = datetime.now()
        curr_editor = session['edt_nom']
        # Filter only active data
        user_rs = Vehicles.query.filter_by(veh_lic_pla=id,veh_sta='ACTIVO').first()
        # Exit or proceed with deletion
        if not user_rs:
            flash("No se pudo borrar","danger")
            return redirect(url_for('flota'))
        else:
            Vehicles.query.filter_by(veh_lic_pla=id).update(dict(
                veh_sta     = 'INACTIVO',
                veh_sta_mod = curr_editor.upper(),
                veh_sta_fec = now_dt))
            db.session.commit()
            flash("Vehiculo eliminado","success")
            return redirect(url_for('flota'))
    else:
        redirect(url_for('login'))

# Records
@app.route('/apiaddrecord', methods=['POST'])
def apiaddrecord():
    if session.get('edt_nom') and request.method=='POST':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt  = datetime.now()
        # Retrieve form info
        placa   = request.form.get('rec_veh_pla')
        usuario = request.form.get('rec_usr_id')
        notas   = request.form.get('rec_veh_des')
        ubi     = request.form.get('rec_veh_loc')
        rdate   = request.form.get('rec_dat',None)
        # Detect vehicle and user
        veh_rs = Vehicles.query.filter_by(veh_lic_pla=placa.upper()).first()
        usr_rs = Users.query.filter_by(usr_id=usuario).first()
        
        if not veh_rs:
            flash("Vehiculo no existe","danger")
            return redirect(url_for('movimiento'))
        if not usr_rs:
            flash("Usuario no existe","danger")
            return redirect(url_for("movimiento"))
        # Return mix data
        veh_mix = veh_rs.veh_mar + " " + veh_rs.veh_mod
        usr_mix = usr_rs.usr_nom + " " + usr_rs.usr_ape_pat
        # Save record
        record = Records(
            rec_dat     =rdate,
            rec_veh_pla =placa.upper(),
            rec_veh_mix =veh_mix,
            rec_usr_id  =usuario,
            rec_usr_mix =usr_mix,
            rec_veh_loc =ubi.upper(),
            rec_veh_des =notas.upper(),
            rec_sta     ='ACTIVO',
            rec_sta_mod =curr_editor.upper(),
            rec_sta_fec =now_dt)
        db.session.add(record)
        db.session.commit()
        flash("Registro añadido con éxito", "success")
        return redirect(url_for('movimiento'))
    else:
        redirect(url_for('login'))

@app.route('/apieditrecord', methods=['POST'])
def apieditrecord():
    if session.get('edt_nom') and request.method=='POST':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt  = datetime.now()
        # Retrieve form info
        id      = request.form.get('rec_id')
        placa   = request.form.get('rec_veh_pla')
        usuario = request.form.get('rec_usr_id')
        ubi     = request.form.get('rec_veh_loc')
        notas   = request.form.get('rec_veh_des')
        # Detect record, vehicle and user
        rec_rs = Records.query.filter_by(rec_id=id,rec_sta='ACTIVO').first()
        veh_rs = Vehicles.query.filter_by(veh_lic_pla=placa.upper(),veh_sta='ACTIVO').first()
        usr_rs = Users.query.filter_by(usr_id=usuario,usr_sta='ACTIVO').first()
       
        if not veh_rs:
            flash("Vehiculo no existe","danger")
            return redirect(url_for('movimiento'))
        if not usr_rs:
            flash("Usuario no existe","danger")
            return redirect(url_for("movimiento"))
        # Return mix data
        veh_mix = veh_rs.veh_mar + " " + veh_rs.veh_mod
        usr_mix = usr_rs.usr_nom + " " + usr_rs.usr_ape_pat
        
        # Detect record id, exit or update the field
        if not rec_rs:
            flash("No se pudo actualizar","danger")
            return redirect(url_for('movimiento'))
        else:
            Records.query.filter_by(rec_id=id).update(dict(
                rec_dat     =request.form['rec_dat'],
                rec_veh_pla =placa.upper(),
                rec_veh_mix =veh_mix,
                rec_usr_id  =usuario,
                rec_usr_mix =usr_mix,
                rec_veh_loc =ubi.upper(),
                rec_veh_des =notas.upper(),
                rec_sta     ='ACTIVO',
                rec_sta_mod =curr_editor.upper(),
                rec_sta_fec =now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('movimiento'))
    else:
        redirect(url_for('login'))

@app.route('/apideactivaterecord/<string:id>/', methods=['GET'])
def apideactivaterecord(id):
    if session.get('edt_nom') and request.method=='GET':
        # Basic data
        curr_editor = session['edt_nom']
        now_dt      = datetime.now()
        # Filter only active data
        rec_rs = Records.query.filter_by(rec_id=id,rec_sta='ACTIVO').first()
        # Redirect or proceed to put record as inactive
        if not rec_rs:
            flash("No se pudo borrar","danger")
            return redirect(url_for('movimiento'))
        else:
            Records.query.filter_by(rec_id=id).update(dict(
                rec_sta    ='INACTIVO',
                rec_sta_mod=curr_editor.upper(),
                rec_sta_fec=now_dt))
            db.session.commit()
            flash("Registro eliminado","success")
            return redirect(url_for('movimiento'))
    else:
        redirect(url_for('login'))
