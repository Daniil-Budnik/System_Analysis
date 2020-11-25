# Класс задач управления записями
class ReserveManagement:
   
# ----------------------------------------------------------------------------------------------------------------------------------------

    # Конструктор
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
 
# ----------------------------------------------------------------------------------------------------------------------------------------
    
    # Задача оптимального размера заказа
    def Optimal_Order_Size_Problem(self,D,K,h,L):
       
        # ---------------------------------------------------------------

        # Формулы
        def Y(K,D,h): from numpy import sqrt; return int(sqrt((2*K*D)/h))
        def t(Yi,D): return int(Yi/D)
        def n(L,T): return int(int(L)/int(T))
        def Le(L,N,T): return int(L-(N*T))

        # ---------------------------------------------------------------

        # Подсчёты
        sY = Y(K,D,h)
        sT = t(sY,D)
        sN = n(L,sT)
        sLE = Le(L,sN,sT)

        # ---------------------------------------------------------------

        # Приветствие
        print("\n>>> Optimal Order Size Problem <<< \n")
        print("\tGiven:\t\tD = ", D, ";\tK = ", K, ";\th = ", h, ";\tL = ", L, ";")
        print("\n\tСalculation: \ty* = ", sY, ";\tt0 = ", sT, ";\tn = ", sN, ";\tLe = ", sLE, ";")
        print("\n\tAnswer:\t Order", sY, "lamps as soon as the stock level is reduced to", sLE*D,"units.")
        

        # ---------------------------------------------------------------

        print("\n>>> --- --- --- --- --- <<<\n") 

# ----------------------------------------------------------------------------------------------------------------------------------------

    # Задача с ограниченной вместимостью склада
    def Task_With_Limited_Warehouse_Capacity(self,As,Ki,Di,Hi,Ai):

        # Кол-во индексов
        M =  len(Ki)

        # Функция Лангранжа
        def L(As,K,D,H,A,Lamd): from numpy import sqrt; return [ sqrt((2*K[i]*D[i])/(H[i]-2*Lamd*A[i])) for i in range(M) ]

        # Начальные условия
        Y, Triger, Lamd = L(As,Ki,Di,Hi,Ai,0), True, 0

        # ---------------------------------------------------------------

        # Приветствие
        print("\n>>> Task With Limited Warehouse Capacity <<< \n")
        print("\tGiven: \n\t  Ki = ", Ki, ";\n\t  Di = ", Di, ";\n\t  Hi = ", Hi, ";\n\t  Ai = ", Ai, ";\n\t  A  =  [" , As , "]")
        print("\n\t Yi: \t" , Y)

        # ---------------------------------------------------------------

        # Алгоритм минимизации
        while(Triger):
            Ss = sum(Y)
            if(Ss <= As): Triger = False; 
            if(Triger): 
                Lamd += (-0.5)
                Y = L(As,Ki,Di,Hi,Ai,Lamd) 
                print("\t Sum: \t", Ss, "\n\n\t Lamd: \t" , Lamd, "\n\t Yi: \t" , Y)
        print("\t Sum: \t", Ss)
        print("\n\t Answer:", Y)  

        # ---------------------------------------------------------------

        print("\n>>> --- --- --- --- --- <<<\n")   
     
# ----------------------------------------------------------------------------------------------------------------------------------------

    # Проблема ценового разрыва
    def PriceGapProblem(self, N, M, L, q, K, c1, c2, h): 

        # Нахождение корней функции на определённом диапозоне
        # Метод половинного деления
        # Функция, начало, конец, точность, увиличение мощности, смещение, вернуть кол-во шагов
        def Half_Division(F, A = 0, B = 1, E = 0.001, K1 = 1, K2 = 0, Step = False):
            S , I = abs(A - B), 0                                       # Узнаём длину, счётчик в нулевой момент времени
            while ( S > E ):                                            # Цикл нахождения корня
                I += 1                                                  # Счётчик
                C = (A + B) / 2                                         # Находим С (середину)
                # Проверка, откинуть левую или правую часть в случае f(x1) * f(x2) < 0
                if( ( ( F(A) * K1 ) + K2 ) * ( ( F(C) * K1 ) + K2 ) > 0): A = C
                else: B = C
                S = abs(A - B)                                          # Длина отрезка
            if(Step): return [( (A + B) / 2 ), I]                       # Возвращаем значение корня и кол-во шагов
            else: return ( (A + B) / 2 )                                # Возвращаем значение корня
       
        # ---------------------------------------------------------------

        from numpy import sqrt

        # Промежуточные данные
        def F_D(N,M): return (N*M)
        def F_Ym(K,D,h): return sqrt((2*K*D)/h)
        def F_TCU(c1,D,K,Ym,h): return (c1*D) + ((K*D)/Ym) + ((h*Ym)/2)

        # Получаем вычесления
        D   =   F_D(N,M)
        Ym  =   F_Ym(K,D,h)
        TCU =   F_TCU(c1,D,K,Ym,h)

        # ---------------------------------------------------------------

        # Подсчёт коэф. для уровнения Q
        def F_q1(c2,D,TCU,h): return ((2*(c2*D - TCU))/h)
        def F_q2(K,D,h): return  (2*K*D)/h

        # Считаем коэф. для уровнения Q
        q1  = F_q1(c2,D,TCU,h)
        q2  = F_q2(K,D,h)

        # Уровнение Q
        def F_Q(x): return (x**2) + (q1*x) + q2

        # ---------------------------------------------------------------

        # Нахождение корней
        KFC = 1
        Q1 = Half_Division(F_Q,0,KFC)
        while(KFC - Q1 < 5): KFC *= 10; Q1 = Half_Division(F_Q,0,KFC)
        Q2 = Half_Division(F_Q,Q1 + 1, 100000000)

        # ---------------------------------------------------------------

        # Вывод данных
        print("\n>>> Price Gap Problem <<< \n")
        print("\tGiven: ", "N = ", N, "; M = ", M, "; L = ", L, "; q = ", q, "; K = ", K, "; c1 = ", c1, "; c2 = ", c2, "; h = ", h)
        print("\n\tD: \t", D, "\n\tYm: \t", Ym, "\n\tTCU: \t", TCU, "\n\n\tq1: \t", q1, "\n\tq2: \t", q2)
        print("\n\tEquation:\t Q**2 + Q * (", q1, ") + (", q2, ")")
        print("\n\tRoot Q1: ", Q1, "\n\tRoot Q2: ",Q2)
        print("\n\tArea  II: (", Ym , ";", Q2, "); \n\tArea  III: (", Q2 , "; ∞ );" )

        # ---------------------------------------------------------------

        # Заключение
        if(q < Ym): 
            print("\n\tPosition 'q' - Area I")
            print("\n\tStrategy unknown...")
        elif(q >= Ym and q <= Q2):  
            print("\n\tPosition 'q' - Area II")
            print("\n\tOrder", q ,"liters of oil when the stock drops to", 2*D, "liters.")
        elif(q > Q2):  
            print("\n\tPosition 'q' - Area III")
            print("\n\tOrder", Ym ,"liters of oil when the stock drops to", 2*D, "liters.")
        else: 
            print("\n\tError position 'q'")
            print("\n\tStrategy unknown...")

        # ---------------------------------------------------------------

        print("\n>>> --- --- --- --- --- <<<\n")

# ----------------------------------------------------------------------------------------------------------------------------------------
    
def main():

    ReserveManagement().Optimal_Order_Size_Problem(D = 25, K = 1500, h = 0.8, L = 15)

    ReserveManagement().PriceGapProblem(N = 140, M = 4.5, L = 2, q = 5000, K = 600, c1= 90, c2 = 85, h = 1.8)

    iK = [500,300,550,250]
    iD = [2,3,4,1]
    iH = [0.3, 0.3, 0.4, 0.2]
    iA = [0.5, 1, 1.5, 1]
    
    ReserveManagement().Task_With_Limited_Warehouse_Capacity(80,iK,iD,iH,iA)


if __name__ == "__main__": main()
