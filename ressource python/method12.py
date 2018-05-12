def get_sec(time_str):
    
    h = time_str.split(':')[0]
    m =  time_str.split(':')[1]
    a = time_str.split(':')[2]
    s = round(float(a))
    return int(h) * 3600 + int(m) * 60 + int(s)

def nombre_de_pts(stay_point_df,choix):
    compteur = 0
    length = max(stay_point_df["segment_mouvement"])
    for i in range(length):
        segment = stay_point_df[stay_point_df['segment_mouvement'] == i]
        segment_mouvement = segment[segment['is_mouvement'] == choix ]
        if(len(segment_mouvement["segment_mouvement"].tolist())!=0):
                compteur += 1

    nbr_de_pts = [[0]* 1 for _ in range(compteur)]
    j=0
    for i in range(length):
        segment = stay_point_df[stay_point_df['segment_mouvement'] == i]
        segment_mouvement = segment[segment['is_mouvement'] == choix ]
        b = segment_mouvement["segment_mouvement"].tolist()
        a = len(b)
        if( a != 0):
            nbr_de_pts[j] = list(set(segment_mouvement["segment_mouvement"].tolist()))[0]
            j = j + 1
    return nbr_de_pts

def repitition(stay_point_df,choix,num):
    segment = stay_point_df[stay_point_df['is_mouvement'] == choix ]
    segment_mouvement = segment[segment['segment_mouvement'] == num]
    b = segment_mouvement["segment_mouvement"].tolist()
    a = len(b)
    return a

def matrice_de_pts(stay_point_df,choix):
    nbr = nombre_de_pts(stay_point_df,choix)
    rep = [[0]*2 for _ in range(len(nbr))]

    for i in range(len(nbr)):
        rep[i][0] = nbr[i]
        rep[i][1] = repitition(stay_point_df,choix,nbr[i])
    return rep

from datetime import timedelta
def approxiamtion(stay_point,choix):
    segment = stay_point[stay_point['is_mouvement'] == choix ]
    a = nombre_de_pts(stay_point,choix)
    df = [[0]*6 for _ in range(len(a))]
    for i in range (len(a)):
        stay_point_app = segment[segment["segment_mouvement"]== a[i]]
        t = 0
        for j in range(len(stay_point_app["time"].tolist())):
                    
            t += get_sec(stay_point_app["time"].tolist()[j])
             
        df[i][0] = sum(stay_point_app["latitude"].tolist())/len(stay_point_app)
        df[i][1] = sum(stay_point_app["longitude"].tolist())/len(stay_point_app)
        df[i][2] = sum(stay_point_app["delay"].tolist())/len(stay_point_app)
        df[i][3] = sum(stay_point_app["velocity"].tolist())/len(stay_point_app)
        df[i][4] = str(timedelta(seconds=round(t)/len(stay_point_app)))
        df[i][5] = sum(stay_point_app["segment_mouvement"].tolist())/len(stay_point_app)

        
    return df

def filtrer(d , coeff):
    compteur = 0
    for i in range(1,len(d)):
        if(abs(d[i-1][0]-d[i][0])>coeff and abs(d[i-1][1]-d[i][1])>coeff):
            compteur += 1

    stay_pt_trajet = [[0]*6 for _ in range(compteur)]
    j=0
    for i in range(1,len(d)):
        if(abs(d[i-1][0]-d[i][0])>coeff and abs(d[i-1][1]-d[i][1])>coeff):
            stay_pt_trajet[j][0] = d[i-1][0]
            stay_pt_trajet[j][1] = d[i-1][1]
            stay_pt_trajet[j][2] = d[i-1][2]
            stay_pt_trajet[j][3] = d[i-1][3]
            stay_pt_trajet[j][4] = d[i-1][4]
            stay_pt_trajet[j][5] = d[i-1][5]
            j+=1
    k=0
    for i in range(1,len(stay_pt_trajet)):
            print("Trajectoire ",k+1)
            print("point depart : lat = ", stay_pt_trajet[i][0] , "long = ",stay_pt_trajet[i][1])
            print("point d'arrive : lat = ", stay_pt_trajet[i-1][0] , "long = ",stay_pt_trajet[i-1][1])
            print("Heure de depart : " , stay_pt_trajet[i][4])
            print("Heure d'arrive : " , stay_pt_trajet[i-1][4])
            a = get_sec(d[i-1][4])- get_sec(d[i][4])
            print("Duree : ",str(timedelta(seconds=a)))
            k += 1
            
    return stay_pt_trajet

def lat(stay_pt_trajet):
    lat1 = [0]*len(stay_pt_trajet)
    for i in range (len(stay_pt_trajet)):
        lat1[i] = stay_pt_trajet[i][0]
    return lat1

def log(stay_pt_trajet):
    log1 = [0]*len(stay_pt_trajet)
    for i in range (len(stay_pt_trajet)):
        log1[i] = stay_pt_trajet[i][1]
    return log1
