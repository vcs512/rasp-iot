Macbee
======

# Raspberry Pi pin LEDs

Use GPIOs 18, 23, 24 and 25 for LED1, LED2, LED3 and LED4, respectively.
# Banco de Dados

## Para criar o banco de dados

```bash
export FLASK_APP=macbee.py
flask db init
flask db migrate
flask db upgrade
flask shell
```

Dentro do shell:

```python
Role.insert_roles()
```

## Usuários

### Adicionar

Para adicionar um usuário, primeiramente, iremos acessar os diferentes 'roles', criados anteriormente:

```python
role_user = Role.query.filter_by(name='User').first()
role_moderator = Role.query.filter_by(name='Moderator').first()
role_admin = Role.query.filter_by(name='Administrator').first()
```

Agora, para adicionar um usuário com privelégios de administrador:

```python
u = User(name='John Admin', username='john_admin', password='password_of_admin', email='john_admin@site.com', confirmed=True, role=role_admin)
```

Para adicionar um usuário comum:

```python
u = User(name='John Doe', username='john_doe', password='password_of_john_doe', email='john_doe@site.com', confirmed=True, role=role_user)
```

E, finalmente, para adicionar um usuário com privilégio de moderador:

```python
u = User(name='John Smith', username='john_smith', password='password_of_john_smith', email='john_smith@site.com', confirmed=True, role=role_moderator)
```


> Os comandos acima já indicam a senha e que o e-mail do usuário é válido. O suporte a e-mails foi desativado nessa versão inicial, mas pode ser ativado para o caso de ser necessário confirmar os e-mails dos usuários.

Finalmente é necessário acrescentar o usuário criado ao DB e atualizar as alterações:

```python
db.session.add(u)
db.session.commit()
```

### Alterar Campos

Para alterar a senha de um usuário, precisamos primeiramente a referência para o objeto do usuário e alterar o campo senha. O mesmo para os outros campos:

```python
u = User.query.filter_by(username='john_doe').first()
u.password = 'x'
```

Depois é só atualiazar o DB:

```python
db.session.commit()
```

Caso se queira testar a senha:

```python
u.verify_password('x')
```

### Apagar usuário

```python
User.query.filter(User.username == 'john_doe').delete()
```
Não esquecer de atualizar o DB com commit.


# Referências

## Flask e organização de projeto
GRINBERG, Miguel. **Flask web development: developing web applications with python**. " O'Reilly Media, Inc.", 2018.

## Base inicial de projeto
https://github.com/jordeam/macbee

https://github.com/miguelgrinberg/flasky-first-edition

https://github.com/miguelgrinberg/flasky

## Streaming de camera
https://towardsdatascience.com/camera-app-with-flask-and-opencv-bd147f6c0eec

https://github.com/hemanth-nag/Camera_Flask_App

## Detecção de movimento
https://automaticaddison.com/motion-detection-using-opencv-on-raspberry-pi-4/

## Detecção de face
https://github.com/informramiz/Face-Detection-OpenCV

## Requerimentos OpenCV
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


## pigpio
        sudo apt-get install python3-pigpio
        sudo pigpiod
