
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

try:
    df = pd.read_excel(r"YOUNOUS SIR.xlsx")
except FileNotFoundError:
    print("Error: Excel file not found.")
    exit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        name=name.upper()
        matching_rows = df[df['Name of the Student'] == name]
        if not matching_rows.empty:
            roll_number = matching_rows['Roll No.'].iloc[0]
            dob = matching_rows['DOB'].iloc[0]
            f=0
            roll=str(roll_number).lower()
            dob=str(dob)[:10]
            dob=dob.strip()
            dob=dob.split("-")
            dob=dob[::-1]
            final_dob="/".join(dob)
            for i in range(2):
                url = 'http://portal.teleuniv.in//exam/examResults'
                data = {
                    'htno': roll,
                    'dob': final_dob,
                    'examname': 'B.Tech 1 Year 2 Sem RKR21 Regular SEPTEMBER-2023',
                    'examid': '32',
                    'resulttype': '1',
                    'examtype': 'Regular',
                    'year': '1',
                    'semester': '2',
                    'regulation': 'RKR21'
                }
                resp = requests.post(url, data=data)
                cont = BeautifulSoup(resp.content, 'html.parser')
                cont1 = cont.get_text()
                asp = list(cont1)
                ap = "".join(asp)
                try:
                    resp = requests.post(url, data=data)
                    cont = BeautifulSoup(resp.content, 'html.parser')
                    cont1 = cont.get_text()
                    asp = list(cont1)
                    ap = "".join(asp)

                    if ap == "   NO RESULTS FOUND":
                        data["dob"] = final_dob
                        resp = requests.post(url, data=data)
                        cont = BeautifulSoup(resp.content, 'html.parser')
                        cont1 = cont.get_text()
                        f=1
                        if i!=0 and f==1:
                            return render_template('index.html', result=cont1)

                    else:
                        x = ap.split('\n\n')
                        res = []
                        for i in x:
                            res.append(i.split('\n'))
                        final_res = []
                        for x in res:
                            if len(x) > 1:
                                final_res.append(x)
                        fin1=[]
                        for x in final_res:
                            fin2=[]
                            for y in x:
                                if y!='':
                                    fin2.append(y)
                            fin1.append(fin2)
                        final_ans=fin1[:3]
                        for x in fin1[3:-3]:
                            y=x.pop().split()
                            a1=y[0]
                            a2=y[1][0]
                            a3=y[1][1:]
                            p=[a1,a2,a3]
                            x.extend(p)
                            final_ans.append(x)
                        final_ans.extend(fin1[-3:])
                        return render_template('index.html', final_res=final_ans)            

                except requests.exceptions.RequestException as e:
                    return render_template('index.html', error=f"Error: {e}")
                if f==0:
                    break
                else:
                    dob1=[1,2,3]
                    dob1[0]=dob[1]
                    dob1[1]=dob[0]
                    dob1[2]=dob[2]
                    dob1="/".join(dob1)
                    final_dob=dob1
        else:
            return render_template('index.html', error="No matching records found.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')