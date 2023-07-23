-- Table for user
CREATE TABLE users(
usr_id VARCHAR(9) PRIMARY KEY,--NÚMERO DE DOCUMENTO
usr_tip_doc	VARCHAR(3),--DNI O CE O LOC
usr_nom	VARCHAR(40),--NOMBRE O NOMBRES
usr_ape_pat	VARCHAR(50),--APELLIDO PATERNO
usr_ape_mat	VARCHAR(50),--APELLIDO MATERNO
usr_emp	VARCHAR(30),--EMPRESA EN LA QUE LABORA
usr_tel_cel	VARCHAR(9),--NÚMERO DE TELÉFONO
usr_dir	VARCHAR(100),--DIRECCIÓN DE VIVIENDA DEL USUARIO
usr_cor_ele	VARCHAR(50),--CORREO ELECTRÓNICO
usr_sta VARCHAR(8), --INACTIVO O ACTIVO (BORRADO)
usr_sta_mod VARCHAR(9), --PERSONA QUE LO HA CREADO
usr_sta_fec TIMESTAMP --FECHA Y HORA EN QUE LO HAN MODIFICADO  
);


-- Table for vehicles
CREATE TABLE vehicles(
veh_lic_pla VARCHAR(9) PRIMARY KEY,--PLACA
veh_usg VARCHAR(10),--USO PERSONAL O EMPRESA
veh_mar VARCHAR(25),--MARCA DEL VEHÍCULO
veh_mod VARCHAR(50),--MODELO DEL VEHÍCULO
veh_yea INT,--AÑO DEL VEHÍCULO
veh_col VARCHAR(30),--COLOR DEL VEHÍCULO
veh_prop_snp VARCHAR(80),--NOMBRE O NOMBRES DE LOS PROPIETARIOS SUNARP
veh_usr_id VARCHAR(9),--DNI O CE DEL USUARIO CONDUCTOR
veh_gps VARCHAR(2),--TIENE O NO TIENE GPS(SI O NO)
veh_rev_tec DATE,--FECHA DE LA ÚLTIMA REVISIÓN TÉCNICA
veh_soa_seg DATE,--FECHA DEL ÚLTIMO SOAT 
veh_seg_ctr VARCHAR(50),--NOMBRE DEL CONTRATANTE DE SEGURO
veh_seg_bro VARCHAR(15),--NOMBRE DEL BROKER DE SEGURO
veh_seg_nro VARCHAR(10),--NÚMERO DEL SEGURO
veh_seg_ini DATE,--FECHA DEL ÚLTIMO SEGURO
veh_sta VARCHAR(8), --INACTIVO O ACTIVO (BORRADO)
veh_sta_mod VARCHAR(9), --PERSONA QUE LO HA CREADO
veh_sta_fec TIMESTAMP, --FECHA Y HORA EN QUE LO HAN MODIFICADO
CONSTRAINT fk_users
FOREIGN KEY(veh_usr_id)
REFERENCES users(usr_id)
);

-- Table for editors
CREATE TABLE editors(
    edt_usr_id VARCHAR(9) PRIMARY KEY, --DNI O CE DEL EDITOR
    edt_usr_pwd VARCHAR(130) NOT NULL, --PASSWORD DEL EDITOR
    edt_nom	VARCHAR(40),--NOMBRE O NOMBRES
    edt_ape_pat	VARCHAR(50),--APELLIDO PATERNO
    edt_ape_mat	VARCHAR(50),--APELLIDO MATERNO
    edt_sta VARCHAR(8) NOT NULL, --INACTIVO O ACTIVO (BORRADO)
    edt_sta_mod VARCHAR(9) NOT NULL, --PERSONA QUE LO HA CREADO
    edt_sta_fec TIMESTAMP NOT NULL--FECHA Y HORA EN QUE LO HAN MODIFICADO
);

-- Table for vehicle records
CREATE TABLE records(
    rec_id SERIAL PRIMARY KEY, -- SERIADO AUTOINCREMENTAL
    rec_dat DATE NOT NULL, -- FECHA DEL REGISTRO
    rec_veh_pla VARCHAR(9) NOT NULL, -- PLACA VEHICULAR
    rec_veh_mix VARCHAR(30), -- MIX DE MARCA Y MODELO
    rec_usr_id VARCHAR(9) NOT NULL, -- DNI O CE DEL CONDUCTOR
    rec_usr_mix VARCHAR(30), -- MIX DE NOMBRE Y APELLIDO PATERNO
    rec_veh_loc VARCHAR(40), -- UBICACION
    rec_veh_des TEXT, -- ANOTACION EXTRA DE USO GENERAL
    rec_sta VARCHAR(8) NOT NULL, -- INACTIVO O ACTIVO (BORRADO)
    rec_sta_mod VARCHAR(9) NOT NULL, -- PERSONA QUE LO HA CREADO
    rec_sta_fec TIMESTAMP NOT NULL -- FECHA Y HORA EN QUE LO HAN MODIFICADO
)