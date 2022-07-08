vigiSEL
======

# Iniciar servidor
```bash
export FLASK_APP=vigisel.py
flask run --host 0.0.0.0
```

# Banco de Dados

## Criar e atualizar o banco de dados

```bash
flask db init
flask db migrate
flask db upgrade
```

Abrir shell:

```python
flask shell
```

## Roles

Carregar Roles do schema:
```python
Role.insert_roles()
```

Variáveis dos roles:
```python
role_user = Role.query.filter_by(name='User').first()
role_moderator = Role.query.filter_by(name='Moderator').first()
role_admin = Role.query.filter_by(name='Administrator').first()
```
Procuram a tabela de Roles por nome e encontram sua chave primária.

## Usuários

### Adicionar

Adicionar um usuário com role de administrador:

```python
u = User(email='vigisel@gmail.com', password='vigiSEL', username='vigiSEL_ADMIN', confirmed=True, role=role_admin)
```

A cada operação no banco de dados é necessário atualizar as alterações:

```python
db.session.add(u)
db.session.commit()
```

### Alterar Campos

Obter a referência para o objeto do usuário e alterar o campo desejado:
```python
u = User.query.filter_by(email='vigisel@gmail.com').first()
u.role = role_moderator
db.session.commit()
```


### Apagar usuário

Procurar e apagar o usuário:
```python
User.query.filter(User.email == 'vigisel@gmail.com').delete()
db.session.commit()
```

## Start on boot

Colocar os seguintes comandos em /etc/rc.local
```bash
## Change MAC
ip link set eth0 down
ip link set eth0 address 00:01:02:03:04:05
ip link set eth0 up
## Start virtualenv
. /home/sel/Code/venv/bin/activate
export FLASK_APP=/home/sel/Code/rasp-iot/vigisel.py
## Start GPIO daemon
pigpiod
## Start server
flask run --host 0.0.0.0
```
reiniciar a rasp em seguida: 
```
sudo reboot
```

# Arquitetura do projeto
```bash
.
└── rasp-iot
    ├── app
    │   ├── auth
    │   │   ├── forms.py
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── camera
    │   │   ├── forms.py
    │   │   ├── __init__.py
    │   │   ├── servo
    │   │   │   ├── __init__.py
    │   │   │   └── Servo_Control.py
    │   │   ├── views.py
    │   │   └── visao
    │   │       ├── detect_face.py
    │   │       ├── __init__.py
    │   │       ├── motion.py
    │   ├── decorators.py
    │   ├── __init__.py
    │   ├── main
    │   │   ├── errors.py
    │   │   ├── forms.py
    │   │   ├── __init__.py
    │   │   └── views.py
    │   ├── models.py
    │   ├── mqtt_func
    │   │   ├── __init__.py
    │   │   ├── mqtt_func.py
    │   ├── static
    │   │   ├── favicon.ico
    │   │   └── styles.css
    │   └── templates
    │       ├── 403.html
    │       ├── 404.html
    │       ├── 500.html
    │       ├── auth
    │       │   ├── change_password.html
    │       │   ├── login.html
    │       │   └── register.html
    │       ├── base.html
    │       ├── camera
    │       │   ├── cam-cv-face.html
    │       │   ├── cam-cv.html
    │       │   ├── cam-cv-motion.html
    │       │   ├── camera.html
    │       │   ├── cam-servos.html
    │       │   └── files.html
    │       ├── exclude_number.html
    │       ├── index.html
    │       ├── moderate.html
    │       ├── moderate_number.html
    │       └── project_info.html
    ├── cliente
    │   └── cliente_mqtt.py
    ├── config.py
    ├── data-dev.sqlite
    ├── LICENSE
    ├── log.txt
    ├── migrations
    │   ├── alembic.ini
    │   ├── env.py
    ├── README.md
    ├── requirements.txt
    ├── saved_model
    │   ├── deploy.prototxt.txt
    │   ├── haarcascade_frontalface_alt.xml
    │   ├── haarcascade_frontalface_default.xml
    │   ├── lbpcascade_frontalface.xml
    │   └── res10_300x300_ssd_iter_140000.caffemodel
    ├── shots
    ├── videos
    ├── vigisel.py
    └── vigiSEL.service

28 directories, 89 files
```


# Referências

## Flask e organização de projeto
GRINBERG, Miguel. **Flask web development: developing web applications with python**. " O'Reilly Media, Inc.", 2018.

## Base e organização de projeto
https://github.com/jordeam/macbee

https://github.com/miguelgrinberg/flasky-first-edition

https://github.com/miguelgrinberg/flasky



## Visão computacional
### Requerimentos OpenCV
https://stackoverflow.com/questions/53347759/importerror-libcblas-so-3-cannot-open-shared-object-file-no-such-file-or-dire

```bash
pip3 install opencv-python 
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
```


### Streaming de camera
https://towardsdatascience.com/camera-app-with-flask-and-opencv-bd147f6c0eec

https://github.com/hemanth-nag/Camera_Flask_App

### Detecção de movimento
https://automaticaddison.com/motion-detection-using-opencv-on-raspberry-pi-4/

### Detecção de face
https://github.com/informramiz/Face-Detection-OpenCV



## Controle de servos
### pigpio
```bash
sudo apt-get install python3-pigpio
sudo pigpiod
```


## MQTT
https://flask-mqtt.readthedocs.io/en/latest/usage.html#connect-to-a-broker

https://github.com/SinaHBN/IoT

### instalar o Mosquitto:
```bash
sudo apt install mosquitto
```

## rodar o mosquitto
```bash
sudo systemctl start mosquitto.service
```

### rodar o cliente simples externo:
```bash
cd cliente
python cliente_mqtt.py
```