def compteurpoint(stay_point_df, num):
    compteur = 0
    for i in range(len(stay_point_df)):
        if(stay_point_df["segment_mouvement"][i] == num):
            compteur += 1
    return compteur


def coordpoint(stay_point_df,num):
    compteur = compteurpoint(stay_point_df,num)
    df = [[0]* 2 for _ in range(compteur)]
    j=0
    for k in range(len(stay_point_df)):
        if(stay_point_df["segment_mouvement"][k] == num):
            df[j][0] = stay_point_df["latitude"][k]
            df[j][1] = stay_point_df["longitude"][k]
            j+=1

    return df

def transformation(stay_point_df):
    length = len(stay_point_df)
    df = [[0]* 4 for _ in range(length)]
    for i in range(length):
        df[i][0] = stay_point_df['latitude'].tolist()[i]
        df[i][1] = stay_point_df['longitude'].tolist()[i]
        df[i][2] = stay_point_df['is_mouvement'].tolist()[i]
        df[i][3] = stay_point_df['segment_mouvement'].tolist()[i]
    return df
                   
def segmentation(stay_point_df, segment):
    length = 0
    for k in range(len(stay_point_df)):
        if(stay_point_df[k][3] == segment):
            length += 1
            
    df = [[0]* 2 for _ in range(length)]
    j=0
    for i in range(len(stay_point_df)):
        if(stay_point_df[i][3] == segment):
            df[j][0] = stay_point_df[i][0]
            df[j][1] = stay_point_df[i][1]
            j+=1

    return df

import test11
from rdp import rdp
def methoderdp(stay_point_df,coeff):
    a = test11.nombre_de_pts(stay_point_df,True)
    data = transformation(stay_point_df)
    newtrajec = [[0]*2 for _ in range(2*len(a))]
    compteur = 0
    for i in range(len(a)):
        
            x = segmentation(data,a[i])
        
            c = rdp(x,epsilon=0.5)
            
            
            if(len(x)>3):
                
                    newtrajec[2*i][0] = c[1][0]

                    newtrajec[2*i][1] = c[1][1]

                    newtrajec[2*i+1][0] = c[0][0]

                    newtrajec[2*i+1][1] = c[0][1]
    compteur = 0
    for i in range(len(newtrajec)):
        if(newtrajec[i][0]!=0 or newtrajec[i][1]!=0):
            if(abs(newtrajec[i-1][0]-newtrajec[i][0])>coeff and abs(newtrajec[i-1][1]-newtrajec[i][1])>coeff):
                    compteur += 1

    newtrajec2 = [[0]*2 for _ in range(compteur)]
    j=0
    for i in range(len(newtrajec)):
        if(newtrajec[i][0]!=0 and newtrajec[i][1]!=0 ):
            if(abs(newtrajec[i-1][0]-newtrajec[i][0])>coeff and abs(newtrajec[i-1][1]-newtrajec[i][1])>coeff):
                    newtrajec2[j][0] = newtrajec[i][0]
                    newtrajec2[j][1] = newtrajec[i][1]
                    j+=1
    return newtrajec2
