import cv2
#Primeiro cria-se um objeto videocapture e le o video dos peixes.
cap = cv2.VideoCapture('/home/idle/Documents/nemo.mp4')

#Entra em um loop infinito
while(True):
    #Aqui se captura frame por frame
    ret,frame = cap.read()
    #O ret tem que ser verdade para que nao der problema no cadigo
    if ret == True:
        #Primeiro transforma o video de RGB para HSV
        n = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        '''Coloca-se em blur para poder melhorar a visualizacao do peixe'''
        nemo = cv2.medianBlur(n,1)
        #Declara-se as cores maximas e minimas do laranja e do branco
        lower_orange = (1,190,200)
        upper_orange = (18,255,255)
        lower_white = (0,0,200)
        upper_white = (145,60,255)
        #Primeiro, cria-se a mascara para o branco
        mask_white = cv2.inRange(nemo,lower_white,upper_white)
        #Entao, cria-se a mascara para o laranja
        mask = cv2.inRange(nemo, lower_orange, upper_orange)
        #Junta as duas em uma mascara so
        final_mask = mask + mask_white
        #Essa mascara vai ser colocada em cima do frame.
        res = cv2.bitwise_and(frame, frame, mask = final_mask)
        #Mostra-se, entao, o video original e o video com a mascara
        cv2.imshow('Frame',res)
        cv2.imshow('Original',frame)
        #Se a pessoa apertar que, o programa para de rodar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #Caso o ret de False, devemos redeclarar o cap.
    else: cap = cv2.VideoCapture('/home/idle/Documents/nemo.mp4')

#Quando acabar, ele solta o objeto
cap.release()
#Fecha todos os frames
cv2.destroyAllWindows()