from flask import Flask, render_template, request 
import pickle

app = Flask(__name__)

def prediction(lst):
    filename = 'Model Building/laptop_price.pkl'
    with open(filename,'rb') as f:
        model = pickle.load(f)
    pred = model.predict([lst])
    return pred


    

@app.route('/',methods=['POST','GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        touchscreen = request.form.get('touchscreen','off')
        ips = request.form.get('ips','off')
        company = request.form['company']
        type = request.form['type']
        os = request.form['os']
        cpu = request.form['cpu']
        gpu = request.form['gpu']
        
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        if touchscreen == 'on':
            feature_list.append(1)
        else:
            feature_list.append(0)
        if ips == 'on':
            feature_list.append(1)
        else:
            feature_list.append(0)
        
        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']
        
        def one_hot_encode(lst,values):
            for item in lst:
                if item == values:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        one_hot_encode(company_list,company)
        one_hot_encode(typename_list,type)
        one_hot_encode(opsys_list,os)
        one_hot_encode(cpu_list,cpu)
        one_hot_encode(gpu_list,gpu)
        
        print(feature_list)
        
        pred = prediction(feature_list)
        pred = pred[0]
        pred = round(pred,0) *300
        
        
    return render_template('index.html',pred=pred)

if __name__ == '__main__':
    app.run(debug=True,port=5001)