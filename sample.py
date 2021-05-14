from flask import Flask,render_template,request
import pandas as pd
import numpy as np
from math import sqrt
import movieposters as mp
      
#from scipy.sparse import csr_matrix


# calculate the Euclidean distance between two vector
'''def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):#-1#remove confusion from here.#
       distance += (row1[i] - row2[i])**2
    return sqrt(distance)'''
    
def cosine_similarity(row1,row2):
    dot=0.0
    magnitude=1
    for i in range(len(row1)):
        dot=dot+(row1[i]*row2[i])
    for i in range(len(row1)):
        maginit=sqrt((row1[i]**2+row2[i]**2))
        if maginit !=0:
            magnitude*=maginit
        
    angle=dot/magnitude
    return (angle);

        
    
# Locate the most similar neighbors
def get_neighbors(train, test_row, num_neighbors,c):
    distances = list()
    x=1;
    for train_row in train:
        if c!=x:
           #dist = euclidean_distance(test_row, train_row)
           dist = cosine_similarity(test_row, train_row)#distance in terms of angle.more the value more will it be similar.
           distances.append((train_row, dist,x))#Create a tuple .
        x=x+1;
    distances.sort(key=lambda tup: tup[1],reverse=True)#asscending order.#####Descending order.
    neighbors = list()
    for i in range(num_neighbors):
       neighbors.append((distances[i][0],distances[i][2]))
    return neighbors;




def GeneraRecom(genres):
 data1 = pd.read_csv('C:/Users/anshu/Downloads/movie.csv')
 data2 = pd.read_csv('C:/Users/anshu/Downloads/ratings_small.csv')

 output1 = pd.merge(data1, data2,
                   on='movieId',
                   how='inner')
 movies_dict=dict(zip(data1.movieId,data1.title))


 df = output1[["movieId","genres","rating"]]
 df=df.groupby('movieId')
 c=0
 ll=0;
 s=''
 listt=[]
 x=0;
          
 for k in  movies_dict:
    if ll==10:
        break
    try:
      rating_mean=df.get_group(k)['rating'].mean()
      if rating_mean>4: 
         genres_name=df.get_group(k)['genres'][x]
         for j in range(len(genres_name)):
             if c==2:
                 break
             if genres_name[j]!='|':
                 s=s+genres_name[j]
             else:
                 c=c+1
                 if s==genres:
                     ll=ll+1
                     listt.append(k)
                 s=''
      x=x+df.get_group(k)['genres'].count()
      c=0
           
    except:
        print('ex')

 mainlist=[]
 for p in range(len(listt)):
  mainlist.append(movies_dict[listt[p]])
  try:
             link = mp.get_poster(title=movies_dict[listt[p]])
             print(link)
             mainlist.append(link)
  except:
             mainlist.append('0')
             print("excep");
        
 return mainlist
           
        

def supper(userrequest):
    data1 = pd.read_csv('C:/Users/anshu/Downloads/movie.csv')
    data2 = pd.read_csv('C:/Users/anshu/Downloads/ratings_small.csv')
    

#Dictionary
    movies_dict=dict(zip(data1.movieId,data1.title))
# using merge function by setting how='inner'
    output1 = pd.merge(data1, data2,
                   on='movieId',
                   how='inner')
#print(output1);

    output1=output1.sort_values(by=['userId'])

    output2=output1.head(60000);#when new user starts.
#created an array of movieId for traversing.
    arr=output2['movieId']
    arr=np.array(arr)
    arr=np.unique(arr);
    final_data=output2.pivot_table(index='userId',columns='movieId',values='rating').fillna(0);
 

#final_data=csr_matrix(final_data.values);
    final_data_list=final_data.values.tolist();


    userId_Search=int(userrequest)
    print(userId_Search)
    x=final_data_list[userId_Search-1];
    c=userId_Search;
    knn=9
    neigh=get_neighbors(final_data_list,x,knn,c);
    users_list=list();
    for i in range(knn):
       users_list.append(neigh[i][1])
    

    movies={}

    
    j=0   
    c=1; 
#print(final_data[131169][2])#key point.
    for i in range(knn):
         while j<len(final_data_list[users_list[i]-1]):
              if final_data[arr[j]][users_list[i]]!=0 and final_data[arr[j]][users_list[i]]>=3 and final_data[arr[j]][userId_Search]==0:
                  if movies_dict[arr[j]] in movies:
                      movies[movies_dict[arr[j]]]+=1
                  else:
                      movies[movies_dict[arr[j]]]=1
             
              j=j+1;
         
         j=0;
   
    
    print("Movies suggested for user with userId = "+ str(userId_Search)+" is :")
    print('\n');
    list_img=[]

    for k,val in movies.items():
        if val>1:
            try:
             list_img.append(k)
             link = mp.get_poster(title=k)
             print(link)
             list_img.append(link)
            except:
             list_img.append('0')
             print("excep");
             
    return list_img
          


app=Flask(__name__,template_folder='template')
@app.route('/',methods=["POST","GET"])#corresponds to dashboard.
def dashboard():
     if request.method=="POST":
         str="Recommend Movies by UserId"
         if str==request.form['bt']:
            return render_template("xsam.html")
         else : return render_template("Home_page.html")
            
      
     else:
        return render_template("dashboard.html")


@app.route('/i',methods=["POST","GET"])# when we call through url then method is Get/else Post.
def home():
    if request.method=="POST":
        userrequest=request.form['ur']
        list_img1=supper(userrequest)
        return render_template('tert.html',list_img1=list_img1)
    else:
        return render_template("xsam.html")
    
@app.route('/s',methods=["POST","GET"])# for genera based recommendation.
def generahome():
    if request.method=="POST":
       genera=request.form['genera']
       list_genera=GeneraRecom(genera)
       print(genera)
       return render_template('tert1.html',list_genera=list_genera)
    else:
       return render_template('Home_page.html')

if __name__=='__main__':
      app.run(debug=True)
      
        

    
