""""
path_Pioneer.py

This class present the PID controller implementation on the mobile robot follower path, this class present five functions
the first function called init, make the initialization of the variables, the connect_Pioneer present the connection with
the coppeliaSim, Speed_Pioneer calculated the wheels speeds based on the robot topology (in this case is a differential robot),
PID_Controller_phi implement the PID based on the phi error (see video of the georgia tech course in this link:
https://www.youtube.com/watch?v=Lgy92yXiyqQ&list=PLp8ijpvp8iCvFDYdcXqqYU5Ibl_aOqwjr&index=14) finally, Robot_Pioneer is the 
principal function in this class.


Author:

    Mario Andres  Pastrana Triana (mario.pastrana@ieee.org)
    Matheus de Sousa Luiz (luiz.matheus@aluno.unb.br)
    Thalita Coelho Aguiar (222030324@aluno.unb.br)
    EVA/MARIA PROJECT - University of Brasilia-(FGA)


Release Date:
    JUN 19, 2024

Finally comment:
    Querido lector por ahora, la correcta implementación de este código lo sabe Mario, Dios, la Virgen Maria y los santos
    esperemos que futuramente Mario continue sabiendo como ejecutar el código o inclusive que más personas se unan para
    que el conocimiento aqui depositado se pueda expandir de la mejor manera.
    Let's go started =)
"""""

import math
import sim
import numpy as np
import math as mat
import time
import csv


class Pioneer():
    """"
    Corobeu class is the principal class to controller the EVA positions robots.
        __init___                   = Function to inicializate the global variables
        connect_Pioneer             = Present the connection with the coppeliaSim
        Speed_Pioneer               = Calculated the wheels speeds based on the robot topology (in this case is a differential robot)
        PID_Controller_phi          = Implement the PID based on the phi error
        Robot_Pioneer               = The principal function in this class.
    """""

    def __init__(self):

        """"
            Initializations global variables
            self.y_out    (float list) = Out position robot in the y axis
            self.x_out    (Float list) = Out position robot in the x axis
            self.phi      (Float)   = phi robot value
            self.v_max    (Integer) = max speed for the robot
            self.v_min    (Integer) = min speed for the robot
            self.posError (Float list) = phi error
        """""

        self.y_out = []
        self.x_out = []
        self.phi = 0
        self.v_max_wheels = 15
        self.v_min_wheels = -15
        self.v_linear = 0.1
        self.posError = []
        self.Min_error_distance = 0.1

    def connect_Pioneer(self, port):
        """""
        Function used to communicate with CoppeliaSim
            argument :
                Port (Integer) = used to CoppeliaSim (same CoppeliaSim)

            outputs : 
                clientID (Integer)  = Client number
                robot    (Integer)  = objecto robot
                MotorE   (Integer)  = Object motor left
                MotorD   (Integer)  = Object motor right
                ball     (Integer)  = Object ball on the scene
        """""

        ### Connect to coppeliaSim ###

        sim.simxFinish(-1)
        clientID = sim.simxStart('127.0.0.1', port, True, True, 2000, 5)
        if clientID == 0:
            print("Connect to", port)
        else:
            print("Can not connect to", port)

        ### Return the objects ###

        returnCode, robot = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx',
                                                    sim.simx_opmode_blocking)  # Obteniendo el objeto "Pioneer_p3dx" de v - rep(Robot Movil)
        returnCode, MotorE = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor',
                                                     sim.simx_opmode_blocking)  # Obteniendo el objeto "Pioneer_p3dx_leftmotor" de v-rep (motor izquierdo)
        returnCode, MotorD = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor',
                                                     sim.simx_opmode_blocking)  # Obteniendo el objeto "Pioneer_p3dx_rightMotor" de v - rep(motor derecho)
        returnCode, ball = sim.simxGetObjectHandle(clientID, 'ball', sim.simx_opmode_blocking)

        return clientID, robot, MotorE, MotorD, ball

    def Speed_Pioneer(self, U, omega, lock_stop_simulation, signed, error_phi):

        """""
        Function used to calculate the speed for each wheel based on the topology robot
            argument :
                U              (Integer) = Max linear speed
                omega          (Float)   = Angular speed
                error_distance (Float)   = Error between the robot and the final point

            outputs : 
                vl (Float)   = Left speed
                vd (Float)   = right speed
                a  (Integer) = condition to simulate
        """""

        ### Calculate the speed based on the topology robot ###

        # L = 381  # Distance between the wheels
        # R = 95  # Wheel radio
        L = 0.381
        R = 0.095

        ### Calculate the speed based on the topology robot ###

        vd = ((2 * (U) + omega * L) / (2 * R))
        vl = ((2 * (U) - omega * L) / (2 * R))
        a = 1
        # print(f'vl === {vl} vd == {vd}')
        # print(f' omega == {omega}')
        ### the first time #####

        Max_Speed = self.v_max_wheels
        Min_Speed = self.v_min_wheels

        # Max_Speed = self.v_max
        # Min_Speed = self.v_min

        ### Saturation speed upper ###

        if vd >= Max_Speed:
            vd = Max_Speed
        if vd <= Min_Speed:
            vd = Min_Speed

        ### Saturation speed Lower ###

        if vl >= Max_Speed:
            vl = Max_Speed
        if vl <= Min_Speed:
            vl = Min_Speed

        ### When arrive to the goal ###

        if lock_stop_simulation == 1 and error_phi <= 0.08:
            a = 0
            vl = 0
            vd = 0

        ### Return values ###

        return vl, vd, a


    def Robot_Pioneer_Primitivas(self, primitiva, duracao=1.0):
        clientID, robot, motorE, motorD, _ = self.connect_Pioneer(19999)

        if sim.simxGetConnectionId(clientID) != -1:
            # Inicialização
            sim.simxSetJointTargetVelocity(clientID, motorE, 0, sim.simx_opmode_blocking)
            sim.simxSetJointTargetVelocity(clientID, motorD, 0, sim.simx_opmode_blocking)

            # Define velocidade linear e angular
            controller_Linear = self.v_linear
            lock_stop_simulation = 0

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

            # Calcula velocidades
            vl, vd, _ = self.Speed_Pioneer(controller_Linear, omega, lock_stop_simulation, 1, 0)

            # Aplica velocidades
            sim.simxSetJointTargetVelocity(clientID, motorE, vl, sim.simx_opmode_blocking)
            sim.simxSetJointTargetVelocity(clientID, motorD, vd, sim.simx_opmode_blocking)
            
            # Espera pelo tempo de execução desejado
            time.sleep(duracao)

            # Para o robô
            sim.simxSetJointTargetVelocity(clientID, motorE, 0, sim.simx_opmode_blocking)
            sim.simxSetJointTargetVelocity(clientID, motorD, 0, sim.simx_opmode_blocking)

    def executar_movimento_com_primitivas(self, x, y, v_linear):
        L = 0.381
        radio_ideal = 0.5
        self.v_linear = v_linear  
        
        # Posição inicial
        clientID, robot, _, _, _ = self.connect_Pioneer(19999)
        _, pos_inicial = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_blocking)
              
        if y != 0 and x != 0:
            
            tempo_y = abs((y - radio_ideal) / v_linear)
            print(f"Andando {y}m no eixo Y")
            self.Robot_Pioneer_Primitivas(1, tempo_y)
                
            fator=1.04 #FATOR DE CORREÇÃO: 1.04 para as condiçoes coppelia e para v= 0.1m/s
            tempo_giro = fator*(math.pi / 2) * (L / v_linear)
            print("Girando 90° para a direita")
            self.Robot_Pioneer_Primitivas(3, tempo_giro)  # primitiva 3: giro à direita

            tempo_x = abs((x - radio_ideal) / v_linear) 
            print(f"Andando {x}m no eixo X")
            self.Robot_Pioneer_Primitivas(1, tempo_x)
        
        elif x == 0 and y != 0:
            
            tempo_y = abs((y) / v_linear)
            print(f"Andando {y}m no eixo Y")
            self.Robot_Pioneer_Primitivas(1, tempo_y)
        
        elif y == 0 and x != 0:
            
            fator=1.04 #FATOR DE CORREÇÃO: 1.04 para as condiçoes coppelia e para v= 0.1m/s
            tempo_giro = fator*(math.pi / 2) * (L / v_linear)
            print("Girando 90° para a direita")
            self.Robot_Pioneer_Primitivas(3, tempo_giro)  # primitiva 3: giro à direita

            tempo_x = abs((x - 2*radio_ideal) / v_linear) #tempo_x = abs(x / v_linear) #tempo_x = abs(x / v_linear)
            print(f"Andando {x}m no eixo X")
            self.Robot_Pioneer_Primitivas(1, tempo_x)
            
            fator=1.04 #FATOR DE CORREÇÃO: 1.04 para as condiçoes coppelia e para v= 0.1m/s
            tempo_giro = fator*(math.pi / 2) * (L / v_linear)
            print("Girando 90° para a direita")
            self.Robot_Pioneer_Primitivas(3, tempo_giro)  # primitiva 3: giro à direita
            
        # Posição final
        _, pos_final = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_blocking)

        print("\nTrajetória geral:")
        print(f"Inicial: {pos_inicial[0]:.4f}, {pos_inicial[1]:.4f}")
        print(f"Final:   {pos_final[0]:.4f}, {pos_final[1]:.4f}")
        print(f"Distância percorrida:   Δx = {abs(pos_inicial[0] - pos_final[0]):.4f}, Δy = {abs(pos_inicial[1] - pos_final[1]):.4f}")


if __name__ == "__main__":
    crb01 = Pioneer()
    x = 1.5      # deslocamento no eixo X (após o giro)
    y = 2    # deslocamento inicial no eixo Y
    v = 0.1      # velocidade linear (m/s)

    crb01.executar_movimento_com_primitivas(x, y, v)
