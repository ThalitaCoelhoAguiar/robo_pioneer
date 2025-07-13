# robo_pioneer
Robótica

# Controle de Robô Pioneer no CoppeliaSim

Este repositório contém dois métodos distintos de controle para um robô móvel Pioneer no simulador **CoppeliaSim**, desenvolvidos no contexto do projeto EVA/MARIA da Universidade de Brasília (FGA):

- **`path_pioneer_M_questao2_trab1.py`**: Controle baseado em *waypoints* com orientação por PID.
- **`Primitivas_Pioneer_questao1_trab1.py`**: Controle baseado em primitivas de movimento (reta e giro), usado para formar trajetórias como "L", "M", etc.

## 📁 Estrutura do Repositório

├── path_pioneer_M_questao2_trab1.py # Controle com PID e waypoints
├── Primitivas_Pioneer_questao1_trab1.py # Controle com primitivas (reta + curva)
├── Pioneer_experiment.csv # Dados de saída (posição do robô)
└── README.md # Este arquivo

- Python 3.x
- [CoppeliaSim](https://www.coppeliarobotics.com/)
- Biblioteca `sim.py` (incluída no CoppeliaSim para comunicação remota)
- Pacotes Python:
  - `numpy`
  - `math`
  - `csv`
 
##  Como Usar

### 1. Inicie o CoppeliaSim
- Certifique-se de que o servidor remoto está ativo (porta padrão: `19999`).
- Carregue uma cena com o robô **Pioneer_p3dx** (e opcionalmente a bola, se necessário).
- Acione o Real-time(o relógio no Coppelia)

### 2. Execute um dos scripts

**Controle com Waypoints (PID):**
```bash
python path_Pioneer.py
Controle com Primitivas (reta + curva):


No path_Pioneer.py, edite a lista:

waypoints = [
    [-1.75, -0.75],
    [-0.9625, -1.4125],
    [-0.175, -0.75],
    [-0.175, -2.05],
]

No primitivas.py, você pode editar:

if __name__ == "__main__":
    crb01 = Pioneer()
    x = 1.5      # deslocamento no eixo X (após o giro)
    y = 2    # deslocamento inicial no eixo Y
    v = 0.1      # velocidade linear (m/s)

    crb01.executar_movimento_L_com_primitivas(x, y, v)


1) Uma visão geral da situação

1.1) Para rodar as simulações
Para a simulação:

- Python 3.x
- [CoppeliaSim](https://www.coppeliarobotics.com/)
- Biblioteca `sim.py` (incluída no CoppeliaSim para comunicação remota)
- Pacotes Python:
  - `numpy`
  - `math`
  - `csv`
 
##  Como Usar

### 1. Inicie o CoppeliaSim
- Certifique-se de que o servidor remoto está ativo (porta padrão: `19999`).
- Carregue uma cena com o robô **Pioneer_p3dx** (e opcionalmente a bola, se necessário).
- Acione o Real-time(o relógio no Coppelia)

### 2. Execute um dos scripts

1.2) Base teórica

Em ambas as simulações utiliza-se robô com duas rodas, logo implementa-se o robô com a definição das rodas e a distância entre as rodas. Para que haja a moviementação foi definida a velocidade de cada uma das rodas evidenciadas a seguir:

v = (v_R + v_L) / 2  
ω = (v_R - v_L) / L


2) Uma visão geral de cada abordagem

2.1) Demo 1:

*Fazer com que o robô percorra uma sequência de dois ou mais pontos: "demo1.py".

*Foi utilizado como base o programa path_Pioneer.py

* O movimento do robô segue o ballPos, em que é calculado o erro entre a posição do robô e do ballPos evidenciado, a seguir:

error_distance = math.sqrt((ballPos[1] - positiona[1]) ** 2 + (ballPos[0] - positiona[0]) ** 2)

e se erro for menor do que o definido, há o ajuste do movimento do carro pelo phid, mostrado, a seguir:

if error_distance >= self.Min_error_distance: ### Calculate the phid (see georgia tech course) ###
  phid = math.atan2(ballPos[1] - positiona[1], ballPos[0] - positiona[0])
  controller_Linear = self.v_linear * error_distance
  lock_stop_simulation = 0

2.2) Demo 2:
Fazer com que chegue à um ponto final utilizando uma seuência de primitivas de movimento: andar à frente uma distância "a", curva 90 graus à direita com raio "a", curva 90 graus à esquerda com raio "a".: "demo1.py".

*Utilizando como base o programa "Primitivas_Pioneer.py"

A movimentação do robô foi baseada na execução sequencial dos comandos, a seguir:

Dessa forma, foram definidos 3 tipos de movimentos:
1_Seguir reto
2_Girar para esquerda
3_Girar para direita

A implementação dos 3 movimentos é evidenciada, a seguir:

if primitiva == 1:
  omega = 0

elif primitiva == 2:
  radio_ideal = 0.5
  omega = -self.v_linear / (-radio_ideal)  # curva à esquerda

elif primitiva == 3:
  radio_ideal = 0.5
  omega = -self.v_linear / radio_ideal     # curva à direita

else:
  omega = 0

Para que o robô execute curvas para a direita ou esquerda, foi necessário definir o raio de giro correspondente à trajetória circular que ele percorre durante a rotação. Inicialmente, o robô se desloca em linha reta ao longo do eixo 𝑦 e, em seguida, realiza uma curva de aproximadamente
90 ∘, descrevendo um arco de circunferência, até alinhar-se com o eixo x., com o tempo de execução definido para cada ação.

A movimentação do robô foi baseada no tempo de execução. Para correlacionar o tempo com a distância informada pelo usuário, adotou-se a relação: tempo = distancia / velocidade_linear, onde t é o tempo de execução, d é a distância desejada e 𝑣 é a velocidade linear do robô. Essa relação é implementada diretamente no código, conforme evidenciado na seguinte linha:

tempo_x = abs((x - radio_ideal) / v_linear)
tempo_y = abs((y - radio_ideal) / v_linear)
tempo_giro = (math.pi / 2) * (L / v_linear)

em que na trajetória em linha reta, o tempo de giro foi calculado com base na distância programada no main, subtraída do raio da trajetória.
Isso ocorre porque, ao realizar a curva, o robô desloca-se horizontal e verticalmente pelo valor do raio, sendo necessário ajustar a distância reta restante para manter a precisão no trajeto.

O movimento do robô é calculado de forma iterativa de modo que possua um erro menor do que o implemenado, a seguir:

if lock_stop_simulation == 1 and error_phi <= 0.08:
            a = 0
            vl = 0
            vd = 0


