import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app=Flask(__name__)
model=pickle.load(open('classifier.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    data=[request.form.values()]
    #input=np.array(list(data.values())).reshape(1,-1)
    le=len(data)
    qty_hyphen_url=0
    qty_slash_url=0
    qty_tld_url=2
    qty_hyphen_params=0
    qty_slash_params=0
    qty_percent_params=0
    asn_ip=134
    time_domain_activation=0
    time_domain_expiration=500
    a=list()
    b=list()
    for i in data:
        if i=='?':
            for i in range(data.index(i),le):
                b.append(i)
            for i in b:
                if i=='-':
                    qty_hyphen_params=qty_hyphen_params+1
                elif i=='/':
                    qty_slash_params=qty_slash_params+1
                elif i=='%':
                    qty_percent_params=qty_percent_params+1
                else:
                    continue
        else:
            a.append(i)
    for i in a:
        if i=='-':
            qty_hyphen_url=qty_hyphen_url+1
        elif i=='/':
            qty_slash_url=qty_slash_url+1
        else:
            continue
    df=pd.DataFrame([[qty_hyphen_url,qty_slash_url,qty_tld_url,qty_hyphen_params,qty_slash_params,qty_percent_params,asn_ip,time_domain_activation,time_domain_expiration]],columns=['qty_hyphen_url','qty_slash_url','qty_tld_url','qty_hyphen_params','qty_slash_params','qty_percent_params','asn_ip','time_domain_activation','time_domain_expiration'])
    output=model.predict(df)
    outputt=0
    if output=='0':
        outputt='safe'
    else:
        outputt='phishing'
    print(output)
    return render_template("home.html",prediction_text="url is {}".format(outputt))
    #return variable   
        
        
            
    

if __name__=="__main__":
    app.run(debug=True)
    