# Servo_Control
Programa para controle dos servo motores da disciplina de "Projetos de Sistemas Digitais". Feito para uso em Raspberry Pi. Funciona numa Raspberry Pi modelo 3B+.

Primeiro instala-se o pacote para o controle do PWM, é necessário permissão de sudo.

```console
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pigpio
sudo pigpiod
```

Antes de utilizar o código é sempre necessário efetuar o seguinte comando no terminal:

```console
sudo pigpiod
```
O código foi desenvolvivo para uso na disciplina supracitada, o controle dos motores foi realizado via um site, e por isso utilizou-se o flask para enviar mensagens de erro para o site, caso isso não seja necessário pode-se simplesmente comentar as linhas com "flash()" e o import do flask, caso pretenda utilizar o flask é necessário a instalação do mesmo:

```console
sudo apt install flask
```

### Funcões Externas

<details><summary>Clique para Expandir</summary>

<p>

As funções externas disponíveis no código são as seguintes:

- toogle_servo(X) 
	- Desliga-se o PWM sendo enviado aos servos. Útil por questões de controle e segurança.
	- Recebe como argumento **X**, para **X**=1 liga-se os servos e para **X**≠1 desliga-se os servos.

- Angulo_Atual_V()
	- Retorna o ângulo atual referente ao PWM sendo exercido ao Servo_V.

- Angulo_Atual_H()
	- Retorna o ângulo atual referente ao PWM sendo exercido ao Servo_H.

- Controle_Manual(angulo_H,angulo_V,slp)
	- Define a posição onde deve-se posicionar o servo motor, tanto na horizontal quanto na vertical.
	- Recebe como argumentos **angulo_H, angulo_V, slp**, onde **angulo_H** define a posição em ângulo do servo_H, **angulo_V** define a posição do ângulo do servo_V e **slp** define o tempo de espera após a rotação.
Obs: Valores padrão: angulo_H=0,angulo_V=0,slp=1

- Controle_Manual_H(angulo_H,slp)
	- Define a posição onde deve-se posicionar o servo motor na horizontal.
	- Recebe como argumentos **angulo_H, slp**, onde **angulo_H** define a posição em ângulo do servo_H e **slp** define o tempo de espera após a rotação.
Obs: Valores padrão: angulo_H=0,slp=1

- Controle_Manual_V(angulo_V,slp)
	- Define a posição onde deve-se posicionar o servo motor na vertical.
	- Recebe como argumentos **angulo_V, slp**, onde **angulo_H** define a posição em ângulo do servo_V e **slp** define o tempo de espera após a rotação.
Obs: Valores padrão: angulo_V=0,slp=1

- Old_Varredura_Servos(x,passo)
	- Recebe como argumentos **x, passo**, onde **x** define o tempo em segundos da varredura e passo define a quantidade de passos a serem realizados durante a varredura, por exemplo, para uma varredura de 10 segundos e 40 passos, serão realizados 20 movimentos do servo motor em 5 segundos, até um extremo e depois 20 movimentos do servo motor em 5 segundos para a posição original.
Obs: Valores padrão: passo=20. Somente movimenta o servo_H.

- Center_Object(pos_H,pos_V,Resolucao_H,Resolucao_V)
	- A função centraliza na tela, tanto na vertical, quanto na horizontal, um objeto em uma posição qualquer (pos_H,pos_V). 
	- Recebe como argumentos **pos_H, pos_V, Resolucao_H, Resolucao_V**, onde **pos_H** define a posição atual do objeto na horizontal, **pos_V** a posição atual do objeto na vertical, **Resolucao_H** define a resolução da imagem na horizontal e **Resolucao_V** define a resolução da imagem na vertical (quantidade de pixels).
Obs: Valores padrão: pos_H, pos_V, Resolucao_H=640, Resolucao_V=480

- Center_Object_H(pos_H,Resolucao_H)
	- A função centraliza no eixo horizontal da tela um objeto em uma posição qualquer (pos_H,pos_V). 
	- Recebe como argumentos **pos_H, Resolucao_H**, onde **pos_H** define a posição atual do objeto na horizontal e **Resolucao_H** define a resolução da imagem na horizontal (quantidade de pixels).
Obs: Valores padrão: pos_H, Resolucao_H=640

- Center_Object_V(pos_V,Resolucao_V)
	- A função centraliza no eixo vertical da tela um objeto em uma posição qualquer (pos_H,pos_V).
	- Recebe como argumentos **pos_V, Resolucao_V**, onde **pos_V** define a posição atual do objeto na horizontal e **Resolucao_V** define a resolução da imagem na vertical (quantidade de pixels).
Obs: Valores padrão: pos_H, Resolucao_H=480

- Adendo: As funções Varredura_Servos, teste, comeca_varredura e para_varredura são funções que foram criadas para utilizar uma variável global 'Varre' de forma a possibilitar que a varredura dos servos, uma função que estaria em primero plano e sendo constantemente utilizada por 'x' segundos assim que chamada, pudesse ser utilizada em conjunto com o restante do projeto disponível em "https://github.com/vcs512/rasp-iot". Dessa forma, com a variável global, pode-se monitorar o estado da varredura de forma a poder criar um novo processo na máquina e então finaliza-lo assim que houver o termino da varredura, via o uso da biblioteca "multiprocessing" do Python.

</p>

</details>

### Definições dos Servos
Os servo motores sendo utilizados são controlados via Pulse Width Modulation (PWM) e possuem um eixo de rotação de -90º até 90º, onde as larguras dos pulsos respectivos são: 1ms até 2ms. O período do pulso deve ser de 20ms (50 Hz). É utilizado o modelo SG90 e o seu datasheet pode ser encontrado na pasta de anexos ou um link direto esta disponível na referências.

### Definições da Câmera
Utilizou-se uma camêra para a centralização do objeto na imagem. O modelo utilizado foi o "Camera Module v2". Onde utilizou-se o tamanho de pixel de Sy = Sx = 0.0012 mm (tanto pra largura quanto pro comprimento) e distância focal de f = 3.04 mm. É utilizado o modelo V2 e o seu datasheet pode ser encontrado na pasta de anexos ou um link direto esta disponível na referências.

### Eixo Considerado no Opencv
O eixo a ser considerado no Opencv para a aplicação na função de centralização pode ser observado abaixo. Há porém de se considerar que a origem do eixo (ponto (0,0)) está localizado no canto superior esquerdo, ao invés do centro da imagem.

<p align="center">
  <img src="https://github.com/Eliel-Santo/Servo_Control/blob/main/Anexos/4iFEV.png?raw=true">
</p>

### Centralização de Objeto

Para a centralização de objeto considera-se o eixo previamente discutido, então obtêm-se a sua posição na tela, assim como a resolução da tela. Com base nesses dados busca-se centralizar o objeto na tela, logo pretende-se posiciona-lo no ponto (Resolução_Horizontal/2, Resolução_Vertical/2), portanto utiliza-se esse ponto como referência no cálculo. Dessa forma obtêm-se a distância angular em cada eixo do objeto a ser centralizado, de forma como está demonstrado na imagem abaixo. 

<p align="center">
  <img src="https://github.com/Eliel-Santo/Servo_Control/blob/main/Anexos/Centralizar.png?raw=true">
</p>

Para encontrar os ângulos basta considerar que é um triângulo retângulo e então pode-se aplicar a seguinte equação, levando em consideração os valores da distância focal e do tamanho dos píxeis obtidos no datasheet da câmera.

+ Equações:
	+ Novo_Angulo_X = Angulo_Atual_X + k * atan(1.0 * (Posicao_Atual_X-Resolucao_X/2.0) * Sx)/f
	+ Novo_Angulo_Y = Angulo_Atual_Y + k * atan(1.0 * (Posicao_Atual_Y-Resolucao_Y/2.0) * Sx)/f


Para a definição de 'k' recomenda-se que se realizem alguns testes e então ir adaptando o valor para obter a melhor precisão, para esse experimento o valor 'k = 5.0' funcionou perfeitamente. Há também de se atentar ao sinal empregado ao novo ângulo, nesse caso notou-se que foi necessário o sinal negativo no eixo vertical (Y). Sx e Sy servem para transformar o valor de pixel para milímetros. (atan() é arcotangente())

### Level Shifter

Os servo motores que estão sendo utilizados operam com 5V, tanto para a alimentação, quanto para o controle do PWM. É possível controlar com tensões menores, porém com menos confiabilidade, logo recomenda-se a utilização de 5V para o controle nos pinos do PWM. Como a Raspberry Pi modelo B+ que está sendo utilizada possui o controle de PWM com tensão de 3.3V é necessário um level shifter para o aumento dessa tensão, logo utiliza-se o circuito abaixo, recomenda-se a conexão do pino de terra da Raspberry com o terra da fonte de alimentação de 5V caso não utilize a fonte de 3.3V da Raspberry.

<p align="center">
  <img src="https://github.com/Eliel-Santo/Servo_Control/blob/main/Anexos/Level_Shifter.jpg?raw=true">
</p>

### Tilt dos Servo Motores

O seguinte tilt foi o utilzado para a montagem dos servo motores:

<p align="center">
  <img src="https://github.com/Eliel-Santo/Servo_Control/blob/main/Anexos/Pan%20Tilt%20Kit%20for%20Servo%20Motors%20Tilt%20Camera%20or%20Sensor%20-%20Twins%20Chip%203.jpg?raw=true">
</p>


### Possíveis Erros

É possível que a depender de como sejam utilizadas as funções aqui contidas assim que for utilizar o controle dos servo motores apareça um erro similar a "Error: GPIO not initialized" ou "Error: GPIO not in PWM mode", essencialmente indica que foi tentando obter alguma informação que não é possível pois o GPIO da Raspberry não está no modo PWM. Geralmente ocorre quando tenta-se utilizar uma função que tenta obter o ângulo atual do motor sem que antes tenha definido um ângulo para o mesmo. Por exemplo, caso tente utilizar a função Angulo_Atual_V() sem antes ter definido algum ângulo, como por exemplo "Controle_Manual_V(10,1)". Uma forma simples de circunventar esse erro é definir os motores para uma posição inicial assim que se iniciar o código.

Embora seja definido nesse readme que os motores rotacionam de [-90°,90°] (total de 180°) na realidade eles estão limitados em sua rotação, somente rotacionando um total de 90° [-45°,45°]. Isso é devido a problemas encontrados durante o projeto pois em algumas circunstâncias onde o motor era sujeito a valores próximos de seus extremos havia então um pico de corrente, como limitavamos a corrente da fonte de tensão não sabemos ao certo o valor máximo mas recomenda-se limitar a fonte em no máximo 0,5A, quando alcançava então esse pico de corrente ele então estabilizava nesse valor alto. Para evitar danos aos motores foi então decidido limitar a operação para valores "seguros", foi-se utilizada a seguinte faixa para variação do PWM [1000 µs,20000 µs] considerando uma frequência de 50Hz (período de 20ms).

---
### Referências
                
1. Datasheet dos Servo Motores (SG90): 
https://www.datasheet4u.com/datasheet-pdf/TowerPro/SG90/pdf.php?id=791970
2. Definições da Câmera (Modelo v2):
https://www.raspberrypi.com/documentation/accessories/camera.html
3. Documentação da Biblioteca pigpio:
http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
4. Imagem do eixo do Opencv:
https://stackoverflow.com/questions/9081900/reference-coordinate-system-changes-between-opencv-opengl-and-android-sensor
5. Imagem do Tilt do Servo Motores:
https://www.twinschip.com/Pan-Tilt-Kit-for-Servo-Motors-Tilt-Camera-or-Sensor

                
----

### Links Úteis

+ Edição do Readme.md
	+ https://pandao.github.io/editor.md/en.html
	+ https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
	+ https://github.com/tchapi/markdown-cheatsheet/blob/master/README.md
	+ https://stackoverflow.com/questions/14494747/how-to-add-images-to-readme-md-on-github
	+ https://gist.github.com/DavidWells/7d2e0e1bc78f4ac59a123ddf8b74932d

+ Explicação sucinta do Pigpio
	+ https://ben.akrin.com/raspberry-pi-servo-jitter/

+ Eixos do Opencv 
	+ https://stackoverflow.com/questions/25642532/opencv-pointx-y-represent-column-row-or-row-column
	+ https://stackoverflow.com/questions/9081900/reference-coordinate-system-changes-between-opencv-opengl-and-android-sensor                   
