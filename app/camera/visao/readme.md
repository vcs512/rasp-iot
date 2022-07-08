## **Visão Computacional**
### view /camera_cv
Localização: app/camera/views.py

| Role      | Permissões |
| :----- | :-----|
| Usuário  | Sem acesso |
| Moderador     |   Habilita/desabilita detecção de movimento e de faces |
| Administrador      |    Escolha de perfis pré-definidos para detecção|



## **Detecção de movimentos**
Modifica o frame gerado por *gen_frames( )*

### função motion( )
Localização: app/camera/visao/motion.py

https://automaticaddison.com/motion-detection-using-opencv-on-raspberry-pi-4/

- Utiliza o algoritmo *BackgroundSubtractorMOG2*
- O movimento é detectado como a maior área de alteração considerando um número de frames anteriores como histórico aplicando segmentação de fundo gaussiana
- Retorna o frame e as bordas inferior esquerda e superior direita do retângulo que identifica o movimento

### view /camera_cv_fine_motion
Localização: app/camera/views.py

- Apenas acessível para o administrador
  
Ajuste fino para detecção de movimento:
| Parâmetro      | Alteração provocada |
| :----- | :-----|
| Número de frames passados do histórico  | Ajuste de trepidação |
| Tamanho de kernel     |   Mínimo tamanho de objeto movimentando detectável |
| Limiar da binarização    |    Sensibilidade para considerar movimento|



## **Detecção de face**
Modifica o frame gerado por *detect_face( )*

### função gen_frames( )
Localização: app/camera/visao/detect_face.py

https://github.com/informramiz/Face-Detection-OpenCV

- Utiliza técnica de classificação em cascata com LBP
- LBP para gerar vetores de *features*
- *AdaBoost* para aglomerar valores do classificador fraco
- Classificação em cascata para eliminar rejeições já em estágios iniciais e diminuir carga de processamento




### view /camera_cv_fine_face
Localização: app/camera/views.py

- Apenas acessível para o administrador
  
Ajuste fino para detecção de faces:
| Parâmetro      | Alteração provocada |
| :----- | :-----|
| Fator de escala  | Maior valor ignora faces menores |
| Número mínimo de vizinhos positivos   |  Sensibilidade de detecção e falsos positivos |