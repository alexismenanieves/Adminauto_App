from application import db, app
from application.models import Vehicles, Users, Editors
from flask import render_template, request, json, jsonify, Response
from flask import redirect, url_for, flash, session
from application.forms import LoginForm, RegisterForm
from application.models import Users, Vehicles, Records
from application.models import UserSchema, VehicleSchema
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
    flota = Vehicles.query.order_by("veh_usg")
    return render_template('flota.html', 
                           flotaTable=flota, 
                           flota=True)

@app.route('/usuarios')
def usuarios():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    usuarios = Users.query.order_by("usr_id")
    return render_template('usuarios.html', 
                           usuariosTable=usuarios, 
                           usuarios=True)

@app.route('/movimiento')
def movimiento():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    records = Records.query.order_by("rec_dat")
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

# Users
@app.route('/apiadduser', methods=['POST'])
def apiadduser():
    if session.get('edt_nom') and request.method=='POST':
        curr_editor = session['edt_nom']
        now_dt  = datetime.now()
        id = request.form['usr_id']
        user_rs = Users.query.filter_by(usr_id=id).first()
        if user_rs:
            user_ck = Users.query.filter_by(usr_id=id,usr_sta='ACTIVO').first()
            if user_ck:
                flash("Usuario ya existe","danger")
                return redirect(url_for('usuarios'))
            else:
                Users.query.filter_by(usr_id=id).update(dict(
                    usr_tip_doc=request.form['usr_tip_doc'],
                    usr_nom    =request.form['usr_nom'],
                    usr_ape_pat=request.form['usr_ape_pat'],
                    usr_ape_mat=request.form['usr_ape_mat'],
                    usr_emp    =request.form['usr_emp'],
                    usr_tel_cel=request.form['usr_tel_cel'],
                    usr_dir    =request.form['usr_dir'], 
                    usr_cor_ele=request.form['usr_cor_ele'],
                    usr_sta    ='ACTIVO',
                    usr_sta_mod=curr_editor.upper(),
                    usr_sta_fec=now_dt))
                db.session.commit()
                flash("Usuario añadido con éxito","success")
                return redirect(url_for('usuarios'))
            
        else:
            user = Users(
                usr_id     =request.form['usr_id'],
                usr_tip_doc=request.form['usr_tip_doc'],
                usr_nom     =request.form['usr_nom'],
                usr_ape_pat =request.form['usr_ape_pat'],
                usr_ape_mat =request.form['usr_ape_mat'],
                usr_emp     =request.form['usr_emp'],
                usr_tel_cel =request.form['usr_tel_cel'],
                usr_dir     =request.form['usr_dir'], 
                usr_cor_ele =request.form['usr_cor_ele'],
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
        now_dt = datetime.now()
        id = request.form['usr_id']
        curr_editor = session['edt_nom']
        user_rs = Users.query.filter_by(usr_id=id,usr_sta='ACTIVO').first()
        if not user_rs:
            flash("No se pudo actualizar","danger")
            return redirect(url_for('usuarios'))
        else:
            Users.query.filter_by(usr_id=id).update(dict(
            #user_rs.update(dict(
                usr_tip_doc=request.form['usr_tip_doc'],
                usr_nom    =request.form['usr_nom'],
                usr_ape_pat=request.form['usr_ape_pat'],
                usr_ape_mat=request.form['usr_ape_mat'],
                usr_emp    =request.form['usr_emp'],
                usr_tel_cel=request.form['usr_tel_cel'],
                usr_dir    =request.form['usr_dir'], 
                usr_cor_ele=request.form['usr_cor_ele'],
                usr_sta    ='ACTIVO',
                usr_sta_mod=curr_editor.upper(),
                usr_sta_fec=now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

@app.route('/apideactivateuser', methods=['POST'])
def apideactivateuser():
    if session.get('edt_nom') and request.method=='POST':
        now_dt = datetime.now()
        id = request.form['usr_id']
        curr_editor = session['edt_nom']
        user_rs = Users.query.filter_by(usr_id=id,usr_sta='ACTIVO').first()
        if not user_rs:
            flash("No se pudo borrar","danger")
            return redirect(url_for('usuarios'))
        else:
            Users.query.filter_by(usr_id=id).update(dict(
                usr_sta    ='INACTIVO',
                usr_sta_mod=curr_editor.upper(),
                usr_sta_fec=now_dt))
            db.session.commit()
            flash("Usuario eliminado","success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

# Vehicles
@app.route('/apiaddvehicle', methods=['POST'])
def apiaddvehicle():
    if session.get('edt_nom') and request.method=='POST':
        curr_editor = session['edt_nom']
        now_dt  = datetime.now()
        id = request.form['veh_lic_pla']
        # Ensure there is data there
        if request.form['veh_rev_tec'] =='' or request.form['veh_rev_tec'] is None:
            rev_tec_date = None
        else:
            rev_tec_date = request.form['veh_rev_tec']
        if request.form['veh_seg_ini'] =='' or request.form['veh_seg_ini'] is None:
            veh_seg_date = None
        else:
            veh_seg_date = request.form['veh_seg_ini']

        veh_rs = Vehicles.query.filter_by(veh_lic_pla=id).first()
        if veh_rs:
            veh_ck = Users.query.filter_by(veh_lic_pla=id,veh_sta='ACTIVO').first()
            if veh_ck:
                flash("Vehiculo ya existe","danger")
                return redirect(url_for('flota'))
            else:
                Vehicles.query.filter_by(veh_lic_pla=id).update(dict(
                    veh_usg     =request.form['veh_usg'],
                    veh_mar     =request.form['veh_mar'],
                    veh_mod     =request.form['veh_mod'],
                    veh_yea     =request.form['veh_yea'],
                    veh_col     =request.form['veh_col'],
                    veh_prop_snp=request.form['veh_prop_snp'],
                    veh_usr_id  =request.form['veh_usr_id'], 
                    veh_gps     =request.form['veh_gps'],
                    veh_rev_tec =rev_tec_date,
                    veh_soa_seg =request.form['veh_soa_seg'],
                    veh_seg_ctr =request.form['veh_seg_ctr'],
                    veh_seg_bro =request.form['veh_seg_bro'],
                    veh_seg_nro =request.form['veh_seg_nro'],
                    veh_seg_ini =veh_seg_date,
                    veh_sta     ='ACTIVO',
                    veh_sta_mod=curr_editor.upper(),
                    veh_sta_fec=now_dt))
                db.session.commit()
                flash("Vehiculo añadido con éxito","success")
                return redirect(url_for('flota'))
        else:
            vehicle = Vehicles(
                veh_lic_pla =request.form['veh_lic_pla'], 
                veh_usg     =request.form['veh_usg'],
                veh_mar     =request.form['veh_mar'],
                veh_mod     =request.form['veh_mod'],
                veh_yea     =request.form['veh_yea'],
                veh_col     =request.form['veh_col'],
                veh_prop_snp=request.form['veh_prop_snp'],
                veh_usr_id  =request.form['veh_usr_id'], 
                veh_gps     =request.form['veh_gps'],
                veh_rev_tec =rev_tec_date,
                veh_soa_seg =request.form['veh_soa_seg'],
                veh_seg_ctr =request.form['veh_seg_ctr'],
                veh_seg_bro =request.form['veh_seg_bro'],
                veh_seg_nro =request.form['veh_seg_nro'],
                veh_seg_ini =veh_seg_date,
                veh_sta     ='ACTIVO',
                veh_sta_mod=curr_editor.upper(),
                veh_sta_fec=now_dt)
            db.session.add(vehicle)
            db.session.commit()
            flash("Vehículo añadido con éxito", "success")
            return redirect(url_for('flota'))
    else:
        redirect(url_for('login'))

@app.route('/apieditvehicle', methods=['POST'])
def apieditvehicle():
    if session.get('edt_nom') and request.method=='POST':
        now_dt = datetime.now()
        id = request.form['veh_lic_pla']
        curr_editor = session['edt_nom']
        user_rs = Vehicles.query.filter_by(veh_lic_pla=id).first()
        if not user_rs:
            flash("No se pudo actualizar","danger")
            return redirect(url_for('flota'))
        else:
            Vehicles.query.filter_by(veh_lic_pla=id).update(dict(
                veh_usg     =request.form['veh_usg'],
                veh_mar     =request.form['veh_mar'],
                veh_mod     =request.form['veh_mod'],
                veh_yea     =request.form['veh_yea'],
                veh_col     =request.form['veh_col'],
                veh_prop_snp=request.form['veh_prop_snp'],
                veh_usr_id  =request.form['veh_usr_id'], 
                veh_gps     =request.form['veh_gps'],
                veh_rev_tec =request.form['veh_rev_tec'],
                veh_soa_seg =request.form['veh_soa_seg'],
                veh_seg_ctr =request.form['veh_seg_ctr'],
                veh_seg_bro =request.form['veh_seg_bro'],
                veh_seg_nro =request.form['veh_seg_nro'],
                veh_seg_ini =request.form['veh_seg_ini'],
                veh_sta    ='ACTIVO',
                veh_sta_mod=curr_editor.upper(),
                veh_sta_fec=now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

@app.route('/apideactivatevehicle', methods=['POST'])
def apideactivatevehicle():
    if session.get('edt_nom') and request.method=='POST':
        now_dt = datetime.now()
        id = request.form['veh_lic_pla']
        curr_editor = session['edt_nom']
        user_rs = Vehicles.query.filter_by(veh_lic_pla=id,veh_sta='ACTIVO').first()
        if not user_rs:
            flash("No se pudo borrar","danger")
            return redirect(url_for('usuarios'))
        else:
            Vehicles.query.filter_by(usr_id=id).update(dict(
                veh_sta    ='INACTIVO',
                veh_sta_mod=curr_editor.upper(),
                veh_sta_fec=now_dt))
            db.session.commit()
            flash("Usuario eliminado","success")
            return redirect(url_for('flota'))
    else:
        redirect(url_for('login'))

# Records
@app.route('/apiaddrecord', methods=['POST'])
def apiaddrecord():
    if session.get('edt_nom') and request.method=='POST':
        curr_editor = session['edt_nom']
        veh_rs = Vehicles.query.filter_by(veh_lic_pla=request.form['rec_veh_pla']).first()
        usr_rs = Users.query.filter_by(usr_id=request.form['rec_usr_id']).first()
        if not veh_rs:
            flash("Vehiculo no existe","danger")
            return redirect(url_for('movimiento'))
        if not usr_rs:
            flash("Usuario no existe","danger")
            return redirect(url_for("movimiento"))
        
        veh_mix = veh_rs['veh_mar'] + " " + veh_rs['veh_mod']
        usr_mix = usr_rs['usr_nom'] + " " + usr_rs['usr_ape_pat']

        now_dt  = datetime.now()
        record = Records(
            rec_dat     =request.form['rec_dat'],
            rec_veh_pla =request.form['rec_veh_pla'],
            rec_veh_mix =veh_mix,
            rec_usr_id  =request.form['rec_usr_id'],
            rec_usr_mix = usr_mix,
            rec_veh_loc =request.form['rec_veh_loc'],
            rec_veh_des =request.form['rec_veh_des'],
            usr_tel_cel =request.form['usr_tel_cel'],
            usr_sta     ='ACTIVO',
            usr_sta_mod =curr_editor.upper(),
            usr_sta_fec =now_dt)
        db.session.add(record)
        db.session.commit()
        flash("Registro añadido con éxito", "success")
        return redirect(url_for('movimiento'))
    else:
        redirect(url_for('login'))

@app.route('/apieditrecord', methods=['POST'])
def apieditrecord():
    if session.get('edt_nom') and request.method=='POST':
        now_dt = datetime.now()
        id = request.form['rec_id']
        curr_editor = session['edt_nom']
        veh_rs = Vehicles.query.filter_by(veh_lic_pla=request.form['rec_veh_pla']).first()
        usr_rs = Users.query.filter_by(usr_id=request.form['rec_usr_id']).first()
        rec_rs = Records.query.filter_by(rec_id=id).first()
        if not veh_rs:
            flash("Vehiculo no existe","danger")
            return redirect(url_for('movimiento'))
        if not usr_rs:
            flash("Usuario no existe","danger")
            return redirect(url_for("movimiento"))
        
        veh_mix = veh_rs['veh_mar'] + " " + veh_rs['veh_mod']
        usr_mix = usr_rs['usr_nom'] + " " + usr_rs['usr_ape_pat']

        if not rec_rs:
            flash("No se pudo actualizar","danger")
            return redirect(url_for('movimiento'))
        else:
            Records.query.filter_by(rec_id=id).update(dict(
                rec_dat     =request.form['rec_dat'],
                rec_veh_pla =request.form['rec_veh_pla'],
                rec_veh_mix =veh_mix,
                rec_usr_id  =request.form['rec_usr_id'],
                rec_usr_mix =usr_mix,
                rec_veh_loc =request.form['rec_veh_loc'],
                rec_veh_des =request.form['rec_veh_des'],
                usr_tel_cel =request.form['usr_tel_cel'],
                rec_sta     ='ACTIVO',
                rec_sta_mod =curr_editor.upper(),
                rec_sta_fec =now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('movimiento'))
    else:
        redirect(url_for('login'))

@app.route('/apideactivaterecord', methods=['POST'])
def apideactivaterecord():
    if session.get('edt_nom') and request.method=='POST':
        now_dt = datetime.now()
        id = request.form['rec_id']
        curr_editor = session['edt_nom']
        rec_rs = Records.query.filter_by(rec_id=id,rec_sta='ACTIVO').first()
        if not rec_rs:
            flash("No se pudo borrar","danger")
            return redirect(url_for('movimiento'))
        else:
            Users.query.filter_by(rec_id=id).update(dict(
                rec_sta    ='INACTIVO',
                rec_sta_mod=curr_editor.upper(),
                rec_sta_fec=now_dt))
            db.session.commit()
            flash("Registro eliminado","success")
            return redirect(url_for('movimiento'))
    else:
        redirect(url_for('login'))
