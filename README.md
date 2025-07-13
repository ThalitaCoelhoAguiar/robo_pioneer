🤖 Controle de Robô Pioneer no CoppeliaSim
Trabalho realizado pelas alunas Thalita Coelho Aguiar - 222030324 e Aline de Carvalho Rodrigues - 180096923
Projeto desenvolvido no contexto do grupo EVA/MARIA da Universidade de Brasília (FGA).

📂 Estrutura do Repositório
graphql
Copiar
Editar
├── path_pioneer_M_questao2_trab1.py       # Controle com PID e waypoints
├── Primitivas_Pioneer_questao1_trab1.py   # Controle com primitivas (reta + curva)
├── Pioneer_experiment.csv                 # Dados de saída (posição do robô)
└── README.md                              # Este arquivo
🧠 Visão Geral
Este repositório apresenta dois métodos distintos de controle para o robô móvel Pioneer no simulador CoppeliaSim:

PID com Waypoints
O robô percorre uma sequência de pontos predefinidos usando controle PID.

Primitivas de Movimento
O robô executa trajetórias compostas por segmentos retos e curvas de 90° (como letras "L" e "M").

⚙️ Requisitos
Python 3.x

CoppeliaSim (com o servidor remoto ativo na porta padrão 19999)

Biblioteca sim.py (fornecida com o CoppeliaSim)

Pacotes Python:

numpy

math

csv

▶️ Como Usar
1. Inicie o CoppeliaSim
Certifique-se de que o servidor remoto está ativo (porta 19999).

Carregue a cena com o robô Pioneer_p3dx (e opcionalmente a bola).

Acione o Real-time (ícone de relógio).

2. Execute um dos scripts
➤ Controle com Waypoints (PID)
bash
Copiar
Editar
python path_pioneer_M_questao2_trab1.py
Edite os waypoints diretamente no código:

python
Copiar
Editar
waypoints = [
    [-1.75, -0.75],
    [-0.9625, -1.4125],
    [-0.175, -0.75],
    [-0.175, -2.05],
]
➤ Controle com Primitivas de Movimento
bash
Copiar
Editar
python Primitivas_Pioneer_questao1_trab1.py
Modifique os parâmetros no main para definir o trajeto:

python
Copiar
Editar
x = 1.5    # Deslocamento no eixo X (após o giro)
y = 2      # Deslocamento no eixo Y
v = 0.1    # Velocidade linear (m/s)
📚 Base Teórica
Ambas as abordagens usam um robô diferencial com duas rodas. As velocidades das rodas determinam o comportamento do robô:

makefile
Copiar
Editar
v = (v_R + v_L) / 2  
ω = (v_R - v_L) / L
🧪 Abordagens
✅ PID com Waypoints (path_Pioneer)
O robô calcula a distância até o próximo ponto e ajusta a orientação com base no erro angular (phid):

python
Copiar
Editar
phid = math.atan2(ballPos[1] - positiona[1], ballPos[0] - positiona[0])
controller_Linear = self.v_linear * error_distance
A simulação segue enquanto o erro de distância for maior que o valor mínimo definido.

✅ Controle com Primitivas (Primitivas_Pioneer)
Três movimentos principais foram definidos:

python
Copiar
Editar
1 → Reto
2 → Curva à esquerda
3 → Curva à direita
Exemplo de implementação:

python
Copiar
Editar
if primitiva == 1:
    omega = 0
elif primitiva == 2:
    radio_ideal = 0.5
    omega = -v_linear / -radio_ideal
elif primitiva == 3:
    radio_ideal = 0.5
    omega = -v_linear / radio_ideal
else:
    omega = 0
O tempo de cada movimento é calculado com:

python
Copiar
Editar
tempo_x = abs((x - radio_ideal) / v_linear)
tempo_y = abs((y - radio_ideal) / v_linear)
tempo_giro = (math.pi / 2) * (L / v_linear)
Na trajetória em linha reta, o tempo de giro foi calculado com base na distância programada no main, subtraída do raio da trajetória.
Isso ocorre porque, ao realizar a curva, o robô se desloca horizontal e verticalmente pelo valor do raio, sendo necessário ajustar a distância reta restante para manter a precisão no trajeto.

A movimentação do robô é baseada no tempo de execução. Para correlacionar com a distância informada, a seguinte relação foi utilizada:

ini
Copiar
Editar
tempo = distância / velocidade_linear
Por fim, o movimento do robô é calculado de forma iterativa, até que o erro de orientação seja pequeno o suficiente:

python
Copiar
Editar
if lock_stop_simulation == 1 and error_phi <= 0.08:
    a = 0
    vl = 0
    vd = 0
🎯 Conclusão
Este projeto demonstra diferentes estratégias de controle para um robô móvel, comparando controle por feedback (PID) e controle baseado em sequência de ações (primitivas). Ambas as abordagens permitem desenvolver habilidades importantes em robótica móvel, controle e simulação.





