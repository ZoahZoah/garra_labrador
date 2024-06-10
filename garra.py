import caninos_sdk as k9

class Garra:
    __is_moving = False

    def __load_pwm_engine(self):
        ''' Habilita PWM '''

        time_count = 1

        while time_count <= 4:
            self.labrador.pin32.enable_pwm(                                     # Motor de avanço
                alias="engine_foward", freq=25, duty_cycle=0.1*time_count)
            
            self.labrador.pin36.enable_pwm(                                     # Motor de recuo
                alias="engine_backward", freq=25, duty_cycle=0.1*time_count)
            
            self.labrador.pin28.enable_pwm(                                     # Motor de esticar a garra
                alias="engine_stretch", freq=25, duty_cycle=0.1*time_count)
            
            self.labrador.pin24.enable_pwm(                                     # Motor de retrair a garra
                alias="engine_retract", freq=25, duty_cycle=0.1*time_count)
            
            '''self.labrador.pin31.enable_pwm(                                     # Motor de subir
                alias="engine_uplift", freq=25, duty_cycle=0.1*time_count)
            
            self.labrador.pin29.enable_pwm(                                     # Motor de descer
                alias="engine_lower", freq=25, duty_cycle=0.1*time_count)'''
            
            self.labrador.pin11.enable_pwm(                                     # Motor de girar para a esquerda
                alias="engine_turn_left", freq=25, duty_cycle=0.1*time_count)
            
            self.labrador.pin7.enable_pwm(                                     # Motor de girar para a direita
                alias="engine_turn_right", freq=25, duty_cycle=0.1*time_count)
            
            time_count = time_count+1

    def __load_gpio_engine(self):
        self.labrador.pin26.enable_gpio(                                       # Define o limite de recuo
            k9.Pin.Direction.INPUT, alias="stop_button_x")                     # o "x" corresponde ao eixo de movimentação
        
        self.labrador.pin18.enable_gpio(                                       # Conta as voltas dadas pelo motor
            k9.Pin.Direction.INPUT, alias="count_button_x")                    # o "x" corresponde ao eixo de movimentação
        
        self.labrador.pin21.enable_gpio(                                       # Define o limite de abertura da garra
            k9.Pin.Direction.INPUT, alias="stop_button_claw")                   
        
        self.labrador.pin37.enable_gpio(                                       # Conta as voltas dadas pelo motor
            k9.Pin.Direction.INPUT, alias="count_button_claw")
        
        self.labrador.pin33.enable_gpio(                                       # define o limite de altura
            k9.Pin.Direction.INPUT, alias="stop_button_y")
        
        self.labrador.pin35.enable_gpio(                                       # Botão de contagem ebutido dentro do motor 9v CC encoder
            k9.Pin.Direction.INPUT, alias="encoder_button_y")   

        self.labrador.pin13.enable_gpio(                                       # define o limite da volta
            k9.Pin.Direction.INPUT, alias="stop_button_turn")
        
        self.labrador.pin3.enable_gpio(                                       # Botão de contagem ebutido dentro do motor 9v CC encoder
            k9.Pin.Direction.INPUT, alias="encoder_button_turn")   


    def __init__(self) -> None:
        self.labrador = k9.Labrador()
        self.__load_pwm_engine()
        self.__load_gpio_engine()

    def stretch_claw(self):
        if not self.__is_moving:
            self.labrador.engine_stretch.pwm.start()
            self.labrador.engine_retract.pwm.stop()
            limit = self.labrador.stop_button_claw.read()

            if limit == True:
                self.labrador.engine_stretch.pwm.stop()
                print('Limite atingido')
            else:
                self.__is_moving = True
                print("Abrindo a garra...")

    def retract_claw(self):
        if not self.__is_moving:
            self.labrador.engine_stretch.pwm.stop()
            self.labrador.engine_retract.pwm.start()

            self.__is_moving = True
            print("Fechando a garra...")

    def foward_claw(self):
        if not self.__is_moving:
            self.labrador.engine_foward.pwm.start()
            self.labrador.engine_backward.pwm.stop()

            self.__is_moving = True
            print("Avançando...")

    def backward_claw(self):
        if not self.__is_moving:
            self.labrador.engine_foward.pwm.stop()
            self.labrador.engine_backward.pwm.start()

            limit = self.labrador.stop_button_x.read()
            print(limit)

            if limit == True:
                self.labrador.engine_backward.pwm.stop()
                self.__is_moving = False
                print('limite atingido')
            else:
                self.__is_moving = True
                print("Recuando...")
    

    def uplift(self):
        if not self.__is_moving:
            self.labrador.engine_uplift.pwm.start()
            self.labrador.engine_lower.pwm.stop()
            limit = self.labrador.stop_button_y.read()
            print(limit)

            if limit == True:
                self.labrador.engine_uplift.pwm.stop()
                self.__is_moving = False
                print('limite atingido')
            else:
                self.__is_moving = True
                print("Subindo...")

    def lower(self):
        if not self.__is_moving:
            self.labrador.engine_uplift.pwm.stop()
            self.labrador.engine_lower.pwm.start()

            self.__is_moving = True
            print("Descendo...")

    def turn_right(self):
        if not self.__is_moving:
            self.labrador.engine_turn_right.pwm.start()
            self.labrador.engine_turn_left.pwm.stop()
            limit = self.labrador.stop_button_turn.read()
            print(limit)

            if limit == True:
                self.labrador.engine_turn_right.pwm.stop()
                self.__is_moving = False
                print('limite atingido')
            else:
                self.__is_moving = True
                print("Girando sentido horário...")

    def turn_left(self):
        if not self.__is_moving:
            self.labrador.engine_turn_right.pwm.stop()
            self.labrador.engine_turn_left.pwm.start()

            self.__is_moving = True
            print("Girando sentido anti-horário...")

    def stop_claw(self):
        self.__is_moving = False
        for pin in self.labrador.enabled_features:
            if pin.pwm is not None:
                pin.pwm.stop()
        print('Parando a garra...')
