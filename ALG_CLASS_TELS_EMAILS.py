import pandas as pd
import re
from itertools import groupby

def clas_tels(FINAL,columnas):
    """
    Algorithm that classifies phones by assigning values ​​from 0 to 4:
    
    Nivel 0: Invalid phone
    Nivel 1: Phone that starts with 0 or 1
    Nivel 2: Phone with exactly 7 and 8 characters
    Nivel 3: Phone with exactly 12 and 13 characters
    Nivel 4: Valid phone (10 characters)
    
    Inputs:
    columna -> List of columns to classifier
    FINAL -> Dataframe
    
    Outputs:
    NONE, THE ORIGINAL DATAFRAME IS MODIFIED.
    
    
    All of the above is designed and tested for phones in Mexico, however, 
    for phones from other countries the implementation is the same, only the logic changes.
    """
    for col in columnas:
        nueva = col+"_VAL"

        FINAL[col]=FINAL[col].astype(str).str.replace("\.0","")
        FINAL[col] = FINAL[col].str.replace("-","").str.replace(" ","").str.replace("/","").str.replace("_","").str.replace("*","").str.replace("(","").str.replace(")","")

        #PARTE 1: Not only numbers
        TELEFONOS = FINAL[col].value_counts().index.to_list()
        telefonos_feos = [TELEFONOS[i] for i,num in enumerate(TELEFONOS) if bool(re.match("^[0-9 ]*$",num))==False]
        FINAL.loc[FINAL[col].isin(telefonos_feos),nueva]=0 # 4PM78914 / 0198314526PF

        #PARTE 2: phones less than 6 digits and greater than 10
        no_digitos = [TELEFONOS[j] for j,numero in enumerate(TELEFONOS) if (len(str(numero))>=11 or len(str(numero))<=6 or len(str(numero))==9)]
        FINAL.loc[(FINAL[col].isin(no_digitos)) & (FINAL[nueva].isna()),nueva]=0 

        #PARTE 3: Phones that do not start with 1 or 0 with lengths other than 12 and 13
        FINAL.loc[(FINAL[col].str[0]=='1') | (FINAL[col].str[0]=='0') & (FINAL[nueva].isna()),nueva]=1 

        #PARTE 4: Phones with 7 and 8 digits
        digitos_7_8 = [TELEFONOS[i] for i,num in enumerate(TELEFONOS) if (len(num)==7 or len(num)==8)]
        FINAL.loc[(FINAL[col].isin(digitos_7_8)) & (FINAL[nueva].isna()),nueva]=2 

        #PARTE 5: Phones with 12 and 13 digits
        digitos_12_13 = [TELEFONOS[i] for i,num in enumerate(TELEFONOS) if (len(num)==12 or len(num)==13)]
        FINAL.loc[(FINAL[col].isin(digitos_12_13)),nueva]=3

        #PARTE 6: Valid phones (with 10 digits)
        digitos_10 = [TELEFONOS[i] for i,num in enumerate(TELEFONOS) if len(num)==10]
        FINAL.loc[(FINAL[col].isin(digitos_10)) & (FINAL[nueva].isna()),nueva]=4 

        #PARTE 7: Only repeat numbers
        repetidos = FINAL[col].loc[FINAL[col].str.match(r'((\w*)\2{3,})')].value_counts().index.to_list() 
        caracteres_repetidos = [repetidos[i] for i,letra in enumerate(repetidos) if len(set(letra))<=3 and len(letra)>4] 
        caracteres_consecutivos = [caracteres_repetidos[i] for i,num in enumerate(caracteres_repetidos) if any(ele>=4 for ele in [(sum(1 for n in grupo)) for j,grupo in groupby(num)])]
        FINAL.loc[FINAL[col].isin(caracteres_consecutivos),nueva]=0 #5555555555 / 5552135 
        
def clas_emails(FINAL,columnas):
    """
    Algorithm that classifies emails by assigning values ​​from 0 to 4:
    
    Level 0: Invalid email 
    Level 1: Email with less than 3 characters
    Level 2: Email with exactly 4 characters
    Level 3: Email with spelling errors that makes it invalid
    Level 4: Valid email
    
    Some commented parts should not be deleted, as it is important to keep different r-string sequences for possible matches.
    
    Inputs:
    columna -> List of columns to classifier
    FINAL -> Dataframe
    
    Outputs:
    NONE, THE ORIGINAL DATAFRAME IS MODIFIED.
    """
    for col in columnas:
        nueva = col+"_VAL"

        #PARTE 1: Emails with characters repeated many times and that only have numbers
        repetidos = FINAL[col].loc[FINAL[col].astype(str).str.match(r'((\w)\2{3,})')].value_counts().index.to_list() 
        parte_izq = [re.findall("\w\S*@",r) for r in repetidos]
        parte_izq = [r for listas in parte_izq for r in listas]   
        caracteres_repetidos = [repetidos[i] for i,letra in enumerate(parte_izq) if len(set(str(letra[0:-1])))<=2]
        buenos = list(set(repetidos).difference(caracteres_repetidos))
        numericos = [repetidos[i] for i,letra in enumerate(parte_izq) if (bool(re.match(r"^[0-9 ]*$",letra[0:-1])) and len(set(letra[0:-1].lower()))>=3)]

        FINAL.loc[FINAL[col].isin(caracteres_repetidos),nueva]=0 #xxxxxxxx@gmail.com 
        FINAL.loc[(FINAL[col].isin(numericos)) & (FINAL[nueva].isna()),nueva]=3 # 89213812@gmail.com

        #PARTE 1.1: Emails where a character is repeated and are valid as WWW.HOLA@gmail.com
        parte_izq = [re.findall("\w\S*@",r) for r in buenos]
        parte_izq = [r for listas in parte_izq for r in listas]   
        con_puntuaciones = [buenos[i] for i,letras in enumerate(parte_izq) if letras.find(',')>=1 or letras.find('.')>=1]

        FINAL.loc[(FINAL[col].isin(con_puntuaciones)) & (FINAL[nueva].isna()),nueva]=4 # www.google@gmail.com 

        #PARTE 1.2: Emails that start with a repeated digit like 000000lalo@gmaill.com / 8888edomex@edomex.mex /
        caracteres_consecutivos = [repetidos[i] for i,letra in enumerate(repetidos) if (letra[0:-1].find("00")>=0 and letra.lower().find('edomex')>=2)]
        FINAL.loc[FINAL[col].isin(caracteres_consecutivos),nueva]=0

        #PARTE 2: emails with only 1,2 and 3 characters before "@"
        menos_16 = FINAL[col].loc[(FINAL[col].astype(str).str.len()<20) & (FINAL[col].astype(str).str.contains('@'))].value_counts().index.to_list()
        parte_izq = [re.findall("\w\S*@",r) for r in menos_16]
        parte_izq = [r for listas in parte_izq for r in listas]  
        pocas_letras = [menos_16[i] for i,letra in enumerate(parte_izq) if len(letra[0:-1])<=3] #todos los que tienen menos de 4 caracteres antes del @ ---->  #1@gmail.com / 123@gmail.com / ab@gmail.com 
        cuatro_digitos = [menos_16[i] for i,letra in enumerate(parte_izq) if len(letra[0:-1])==4] # todos aquellos con 4 digitos

        FINAL.loc[FINAL[col].isin(cuatro_digitos) & FINAL[nueva].isna(),nueva]=2 #  abcd@gmail.com
        FINAL.loc[FINAL[col].isin(pocas_letras),nueva]=1 #  a@gmail.com / ab@hotmail.com / azm@att.net.mx

        #PARTE 3: emails with errors
        PUNTUACIONES_1 = FINAL[col].loc[FINAL[col].str.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")==False].value_counts().index.to_list() 
        #PUNTUACIONES_2 = FINAL[col].loc[FINAL[col].str.match(r"^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$")==False].value_counts().index.to_list() 
        #PUNTUACIONES_3 = FINAL[col].loc[FINAL[col].str.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')==False].value_counts().index.to_list() 
        DIAG = FINAL[col].loc[FINAL[col].astype(str).str.contains('/')].value_counts() # Correos con / ---> BLING/18@HOTMAIL.COM
        FINAL.loc[(FINAL[col].isin(PUNTUACIONES_1)) | (FINAL[col].isin(DIAG)) & (FINAL[nueva].isna()),nueva]=3 # @JANALUNA94@GMAIL.COM / PAPA_GLEZ@HOTMAIL.COM. / daniel.olivag@outlook..com 

        #PARTE 4: specific cases using keywords like 'NOEMAIL' /'SINCORREO' / 'EXAMPLE' 
        CLAVES = ["NOEMAIL","SINCORREO","NO"]
        palabras_clave = [FINAL[col].loc[FINAL[col].astype(str).str.contains(ele)].value_counts().index.to_list() for ele in CLAVES] # You can use "|".join(CLAVES) for not use list comprehension
        palabras_clave = [r for listas in  palabras_clave for r in listas]
        FINAL.loc[(FINAL[col].isin(palabras_clave)) & (FINAL[nueva].isna()),nueva]=0 
        #PARTE 5: specific cases where there is no "@"
        SIN_ARROBA = FINAL[col].loc[~FINAL[col].astype(str).str.contains('@')].value_counts().index.to_list()
        FINAL.loc[FINAL[col].isin(SIN_ARROBA),nueva]=0 

        #PARTE 6: The remainder must be valid emails
        FINAL.loc[(FINAL[nueva].isna()) & (~FINAL[col].isna()),nueva]=4 #

        #PARTE 7: Verifying that you have a mail structure to those who are level 3
        VERIFICACION_1 = FINAL[col].loc[FINAL[col].str.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")==True].value_counts().index.to_list() 
        #VERIFICACION_2 = FINAL[col].loc[FINAL[col].str.match(r"\A(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)\Z")==True].value_counts().index.to_list() 
        #VERIFICACION_3 = FINAL[col].loc[FINAL[col].str.match(r"^((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)$")==True].value_counts().index.to_list() 
        FINAL.loc[FINAL[col].isin(VERIFICACION_1) & (FINAL[nueva]==3),nueva]=4 
