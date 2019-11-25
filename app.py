from flask import Flask, flash, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from math import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
Bootstrap(app)

def factor(num):
    factors = []
    if num<0:
        num = -num
    if num>6:
        for i in range(1,int(num/2)+1):
            if num%i == 0:
                factors.append(i)
                factors.append(int(num/i))
    else:
        for i in range(1,int(num)+1):
            if num%i == 0:
                factors.append(int(i))
    final_list = [] 
    for n in factors: 
        if n not in final_list: 
            final_list.append(n) 
    final_list.sort()
    return final_list

def foil(cd):
    c1,d1,c2,d2=cd
    c = []
    for i in c1:
        for j in c2:
            c.append(float(i)*float(j))
    d = []
    for i in d1:
        for j in d2:
            d.append(int(i)+int(j))
    dt = []
    for i in range(len(d)):
        for j in range(len(d)):
            if d[i] == d[j] and i!=j and j not in dt:
                c[j] = c[i]+c[j]
                dt.append(i)
    nc = []
    nd = []
    for i in range(len(d)):
        if i not in dt:
            nd.append(d[i])
            nc.append(c[i])
    c,d=[nc,nd]
    fin = ''
    for i in range(len(c)):
        if c[i] != 1:
            if c[i]%1 == 0:
                co = int(c[i])
            else:
                co = c[i]
        else:
            co = ''
        if d[i] == 0:
            deg = ''
        elif d[i] == 1:
            deg = 'x'
        else:
            deg = 'x^'+str(d[i])
        fin += str(co)+deg
        if i != len(c)-1:
            fin += ' + '
    return fin

def polyfact_calc_all_combinations(f1,f2):
    combinations = []
    for i in f1:
        for j in f2:
            if j%i==0:
                combinations.append(str(j/i))
            else:
                combinations.append(str(j)+'/'+str(i))
    return combinations

def polyfact_try_candidates(combos,cl):
    zeros = []
    recreated_eq = ''
    for j in range(len(cl)):
        recreated_eq+='('+str(cl[j])+')*x**('+str(len(cl)-j-1)+')+'
    recreated_eq=recreated_eq[:-1]
    print(recreated_eq)
    for i in combos:
        x = float(eval(i))
        print(x)
        print(eval(recreated_eq))
        if eval(recreated_eq)==0: zeros.append(i)
        x = -x
        if eval(recreated_eq)==0: zeros.append('-'+i)
    return zeros

@app.route('/')
def index():
    tools = [{'Basic Calculation':'/basic'},
             {'Polynomial Root Finder':'/polyfact',
             'Factor Expansion':'/foil',
             'Factoring':'/factor'},
             {'Arithmetic Series':'/arithseries',
             'Geometric Series':'/geoseries',
             'Convergent Geometric Sequences':'/congeoseq'},
             {'Arithmetic Sequences':'/arithseq',
             'Geometric Sequences':'/geoseq'
             }]
             #'Sequences':'/seq',
             #'Series':'/series'}
    return render_template('index.html',tools = tools)

@app.route('/basic',methods=['GET','POST'])
def gencalc():
    fields = ['Expression','Variable Value (optional)']
    if request.method == 'POST':
        exp = str(request.form['Expression'])
        try:
            x = float(request.form['Variable Value (optional)'])
            ans = eval(exp)
        except: 
            ans=''
            graph = True
        return render_template('calc.html',fields = fields, answer = ans, title = 'Basic Calculation', graph=graph, exp=exp)
    return render_template('calc.html',fields = fields, answer = '', title = 'Basic Calculation', graph=False)

@app.route('/factor',methods=['GET','POST'])
def factorpage():
    fields = ['Number']
    if request.method == 'POST':
        num = float(request.form['Number'])
        if num > 60000000:
            flash('Value too large.')
            return redirect(url_for('factorpage'))
        final_list = factor(num)
        return render_template('calc.html',fields = fields, answer = final_list, title='Factor Calculation')
    return render_template('calc.html',fields = fields, answer = '', title='Factor Calculation')

@app.route('/foil',methods=['GET','POST'])
def foilpage():
    fields = ['Coefficients of 1st Factor','Coefficients of 2nd Factor']
    if request.method == 'POST':
        c1 = request.form[fields[0]].split(' ')
        c2 = request.form[fields[1]].split(' ')
        d1 = []
        for i in range(len(c1))[::-1]:
            d1.append(i)
        d2 = []
        for i in range(len(c2))[::-1]:
            d2.append(i)
        exp = foil([c1,d1,c2,d2])
        return render_template('calc.html', title = 'Factor Expansion', fields = fields, answer = exp)
    return render_template('calc.html', title = 'Factor Expansion', fields = fields, answer = '')

@app.route('/polyfact',methods=['GET','POST'])
def polyfact():
    fields = ['Coefficients of Polynomial']
    if request.method == 'POST':
        coefficients = request.form['Coefficients of Polynomial'].split(' ')
        for i in coefficients:
            i = float(str(i))
        lc = coefficients[0]
        ct = coefficients[-1]
        f1 = factor(float(lc))
        f2 = factor(float(ct))
        combos = polyfact_calc_all_combinations(f1,f2)
        ans = 'Candidates: '+str(combos).strip('[]')
        ans += '<br>Roots: '+str(polyfact_try_candidates(combos,coefficients))
        return render_template('calc.html', title = 'Polynomial Root Finder', fields = fields, answer = ans)
    return render_template('calc.html', title = 'Factor Expansion', fields = fields, answer = '')

@app.route('/e',methods=['GET','POST'])
def egg():
    fields=['yes/no']
    if request.method == 'POST':
        if request.form['yes/no'] == 'yes':
            return render_template('calc.html',title='Is QQ Cute?',fields=fields, answer="That's what I thought.")
        elif request.form['yes/no'] == 'no':
            return render_template('calc.html',title='Is QQ Cute?',fields=fields, answer="Oh, really?")
    return render_template('calc.html',title='Is QQ Cute?',fields=fields, answer="")

@app.route('/arithseq')
def arithseq():
    return 'Under Construction'

@app.route('/arithseries',methods = ['GET','POST'])
def arithseries():
    fields = ['a_1','d','S']
    if request.method == 'POST':
        a1 = float(request.form['a_1'])
        d = float(request.form['d'])
        s = float(request.form['S'])
        ans = 'a_n = '+str(d)+' (n) + '+str(-d+a1)
        an = d*s+(-d+a1)
        ans += '<br>'+str(s)+'(('+str(a1)+' + '+str(an)+')/2)<br>'
        ans += str(s*((a1+an)/2))
        return render_template('calc.html',title='Arithmetic Series',answer = ans, fields = fields)
    return render_template('calc.html',title='Arithmetic Series',answer = '', fields = fields)

if __name__ == '__main__':
    app.run('0.0.0.0')
