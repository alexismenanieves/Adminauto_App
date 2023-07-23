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
                           recordsTable=usuarios, 
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

@app.route("/listado")
def listado():
    if not session.get('edt_nom'):
        return redirect(url_for('login'))
    listado = Vehicles.query.order_by("veh_usg")
    return render_template('listado.html', listado=listado)

############################ API SECTION ###############################

user_schema = UserSchema()
users_schema = UserSchema(many=True)
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)

@app.route('/apiadduser', methods=['POST'])
def apiadduser():
    if session.get('edt_nom') and request.method=='POST':
        curr_editor = session['edt_nom']
        now_dt  = datetime.now()
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
            flash("No se pudo desactivar","danger")
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

@app.route('/apiaddvehicle', methods=['POST'])
def apiaddvehicle():
    if session.get('edt_nom') and request.method=='POST':
        curr_editor = session['edt_nom']
        now_dt  = datetime.now()
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
            veh_rev_tec =request.form['veh_rev_tec'],
            veh_soa_seg =request.form['veh_soa_seg'],
            veh_seg_ctr =request.form['veh_seg_ctr'],
            veh_seg_bro =request.form['veh_seg_bro'],
            veh_seg_nro =request.form['veh_seg_nro'],
            veh_seg_ini =request.form['veh_seg_ini'],
            veh_rev_tec =request.form['veh_rev_tec'],
            usr_sta     ='ACTIVO',
            usr_sta_mod=curr_editor.upper(),
            usr_sta_fec=now_dt)
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
            return render_template('listado.html')
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
                usr_sta    ='ACTIVO',
                usr_sta_mod=curr_editor.upper(),
                usr_sta_fec=now_dt))
            db.session.commit()
            flash("Actualización exitosa","success")
            return redirect(url_for('usuarios'))
    else:
        redirect(url_for('login'))

# @api.route('/apication/users','/apication/users/')
# class GetAndPost(Resource):
#     # GET ALL
#     def get(self):
#         users_list = Users.query.all()
#         result = users_schema.dump(users_list)
#         return jsonify(result)
    
#     # POST
#     def post(self):
#         data    = api.payload
#         now_dt  = datetime.now()
#         user = Users(usr_id     =data['usr_id'], 
#                      usr_tip_doc=data['usr_tip_doc'],
#                      usr_nom    =data['usr_nom'],
#                      usr_ape_pat=data['usr_ape_pat'],
#                      usr_ape_mat=data['usr_ape_mat'],
#                      usr_emp    =data['usr_emp'],
#                      usr_tel_cel=data['usr_tel_cel'],
#                      usr_dir    =data['usr_dir'], 
#                      usr_cor_ele=data['usr_cor_ele'],
#                      usr_sta    =data['usr_sta'],
#                      usr_sta_mod=data['usr_sta_mod'],
#                      usr_sta_fec=now_dt)
#         user.save()
#         user_added = Users.query.filter_by(usr_id=data['usr_id']).first()
#         result = user_schema.dump(user_added)
#         return jsonify(result)
    
# @api.route('/apication/user/<string:idx>','/apication/user/<string:idx>/')
# class GetUpdateDelete(Resource):
#     # GET ONE
#     def get(self, idx):
#         user_list = Users.query.filter_by(usr_id=idx).first()
#         result = user_schema.dump(user_list)
#         return jsonify(result)
    
#     # PUT
#     def put(self, idx):
#         data = api.payload
#         now_dt = datetime.now()
#         user_mod = Users.query.filter_by(usr_id=idx).first()
#         if user_mod:
#             Users.query.filter_by(usr_id=idx).update(dict(
#                 usr_tip_doc=data['usr_tip_doc'],
#                 usr_nom    =data['usr_nom'],
#                 usr_ape_pat=data['usr_ape_pat'],
#                 usr_ape_mat=data['usr_ape_mat'],
#                 usr_emp    =data['usr_emp'],
#                 usr_tel_cel=data['usr_tel_cel'],
#                 usr_dir    =data['usr_dir'], 
#                 usr_cor_ele=data['usr_cor_ele'],
#                 usr_sta    =data['usr_sta'],
#                 usr_sta_mod=data['usr_sta_mod'],
#                 usr_sta_fec=now_dt
#             ))
#             db.session.commit()
#             return jsonify(message="Update very succesful")
#         else:
#             return jsonify(message="That user does not exist"),404
    
#     # DELETE (TOO DANGEROUS)
#     #def delete(self, idx):
#     #    Users.objects(user_id=idx).delete()
#     #    return jsonify('User is deleted')

# # Vehicles -------------------------------------------------------------
# @api.route('/apication/vehicles','/apication/vehicles/')
# class GetAndPost(Resource):
#     # GET ALL
#     def get(self):
#         vehicles_list = Vehicles.query.all()
#         result = vehicles_schema.dump(vehicles_list)
#         return jsonify(result)
    
#     # POST
#     def post(self):
#         data = api.payload
#         curr_user = Users.query(usr_id=data['usr_id']).first()
#         if curr_user:
#             vehicle = Vehicles(veh_lic_pla=data['veh_lic_pla'], 
#                                veh_usg=data['veh_usg'],
#                                veh_mar=data['veh_mar'],
#                                veh_mod=data['veh_mod'],
#                                veh_yea=data['veh_yea'],
#                                veh_col=data['veh_col'],
#                                veh_prop_snp=data['veh_prop_snp'],
#                                veh_usr_id=data['veh_usr_id'],
#                                veh_gps=data['veh_gps'],
#                                veh_rev_tec=data['veh_rev_tec'],
#                                veh_soa_seg=data['veh_soa_seg'],
#                                veh_seg_ctr=data['veh_seg_ctr'],
#                                veh_seg_bro=data['veh_seg_bro'],
#                                veh_seg_nro=data['veh_seg_nro'],
#                                veh_seg_ini=data['veh_seg_ini'],
#                                veh_sta=data['veh_sta'],
#                                veh_sta_mod=data['veh_sta_mod'],
#                                veh_sta_fec=data['veh_sta_fec'])
#             vehicle.save()
#             vehicle_added = Vehicles.query.\
#                 filter_by(veh_lic_pla=data['usr_id']).first()
#             result = vehicle_schema.dump(vehicle_added)
#             return jsonify(result)
        
# @api.route('/apication/vehicle/<string:idx>',
#            '/apication/vehicle/<string:idx>/')
# class GetUpdateDelete(Resource):
#     # GET ONE
#     def get(self, idx):
#         vehicle_list = Vehicles.query.filter_by(veh_lic_pla=idx).first()
#         result = vehicle_schema.dump(vehicle_list)
#         return jsonify(result)
    
#     # PUT
#     def put(self, idx):
#         data = api.payload
#         Vehicles.query.filter_by(veh_lic_pla=idx).update(**data)
#         vehicle_list = Vehicles.query.filter_by(veh_lic_pla=idx).first()
#         result = vehicle_schema.dump(vehicle_list)
#         return jsonify(result)
    
#     # DELETE (TOO DANGEROUS)
#     #def delete(self, idx):
#     #    Users.objects(user_id=idx).delete()
#     #    return jsonify('User is deleted')

# # Records --------------------------------------------------------------
# @api.route('/apication/records','/apication/records/')
# class GetAndPost(Resource):
#     # GET ALL
#     def get(self):
#         return jsonify(Records.query.all())
    
#     # POST
#     def post(self):
#         data = api.payload
#         curr_user   = Users.query.\
#             filter_by(usr_id=data['rec_usr_id']).first()
#         curr_veh    = Vehicles.query.\
#             filter_by(veh_lic_pla=data['rec_veh_pla']).first()
#         if curr_user and curr_veh:
#             user_mix= curr_user['usr_nom'] + ' ' + curr_user['usr_ape_pat']
#             veh_mix = curr_veh['veh_mar'] + ' ' + curr_veh['veh_mod'] 
#             vehicle = Vehicles(rec_dat=data['rec_dat'], 
#                                rec_veh_pla=data['rec_veh_pla'],
#                                rec_veh_mix=veh_mix,
#                                rec_usr_id=data['rec_usr_id'],
#                                rec_usr_mix=user_mix,
#                                rec_veh_loc=data['rec_veh_loc'],
#                                rec_veh_des=data['rec_veh_des'])
#             vehicle.save()
#             return jsonify(Vehicles.query.order_by('-rec_id').first())
