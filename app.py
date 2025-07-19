from flask import Flask,render_template,redirect,request,url_for
import json,os
app = Flask(__name__)

@app.route('/')
def dummpy():
    return redirect(url_for('home'))

@app.route('/home',methods =['GET','POST'])
def home():
    dt = datetime.now(ZoneInfo("Asia/Kolkata"))  
    ctt = int(dt.strftime("%H"))    
    if 0 <= ctt < 12:
        greet = "Good morning"
    elif 12 <= ctt < 16:
        greet = "Good afternoon"
    elif 16 <= ctt < 19:
        greet = "Good evening"
    elif 19 <= ctt <= 23:
        greet = "Good night"
    if request.method == 'POST':
        choice = request.form['option']
        if choice.strip().lower() == 'task':
            return redirect(url_for('task_count'))
        elif choice.strip().lower() == 'diary':
            return redirect(url_for('diary'))
        else:
            pass
    return render_template('home.html',ctt = ctt,greet = greet,dt = dt)

@app.route('/task_count',methods = ['GET','POST'])
def task_count():
    if request.method == 'POST':
        count = int(request.form.get('count',0))
        return redirect(url_for('add_task', count=count))
    return render_template('task_count.html')

@app.route('/task_count/add_task',methods = ['GET'])
def add_task():
    count_str = request.args.get('count', '0')  # default is string '0'
    count = int(count_str)
    return render_template('add_task.html',count = count)
    
@app.route('/save_task',methods =['POST','GET'])
def save_task():
    tasks ={}
    choice = request.form.get('option', '').strip().lower()
    count = int(request.form.get('count',0))
    for i in range(count):
        task = request.form.get(f'task{i}',' ')
        tasks[str(i+1)] = task
    print("TASKS:", tasks)
    if choice == 'yes':
        if os.path.exists('tasks.json'):
            with open('tasks.json','r') as f:
                existing_data = json.load(f)
        else:
            existing_data = {}
        if existing_data:
            index = max(map(int, existing_data.keys())) + 1
        else:
            index = 1

        for i,task in enumerate(tasks.values(),start = index):
            existing_data[str(i)] = task

        with open('tasks.json','w') as f:
            json.dump(existing_data,f,indent=2)

    elif choice =='no':
        print('Your data will loss')
    return redirect(url_for('view_task'))

@app.route('/view_task',methods=['GET'])
def view_task():
    all_tasks ={}
    if os.path.exists('tasks.json'):
        with open('tasks.json','r') as f:
            all_tasks =json.load(f)
    return render_template('view_task.html',all_tasks = all_tasks)

@app.route('/task_action', methods =['POST','GET'])
def task_action():
    count = int(request.args.get('count', 0 ))  
    nav_option = request.form.get('action', '').strip().lower()
    if nav_option == 'add':
        return redirect(url_for('task_count', count=count))
    elif nav_option =='remove':
        return redirect(url_for('edit_remove_task'))



@app.route('/edit_remove_task', methods=['POST', 'GET'])
def edit_remove_task():
    if not os.path.exists('tasks.json'):
        return redirect(url_for('home'))

    with open('tasks.json', 'r') as f:
        data = json.load(f)

    if request.method == 'POST':
        digit = str(request.form.get('s.no_removes'))
        if digit in data:
            data.pop(digit)
            with open('tasks.json', 'w') as f:
                json.dump(data, f, indent=2)
            return render_template('view_task.html', all_tasks=data)
        else:
            return "<h1>No task found with that serial number</h1>"
    return render_template('edit_remove_task.html')


from datetime import datetime
from zoneinfo import ZoneInfo

@app.route('/diary',methods=['POST','GET'])
def diary():
    dt = datetime.now(ZoneInfo("Asia/Kolkata"))
    cd = dt.strftime("%Y-%m-%d %Z") 
    ct = dt.strftime("%I:%M %p")
    ctt = int(dt.strftime("%H"))
      
    if 0 <= ctt < 12:
        greet = "Good morning"
    elif 12 <= ctt < 16:
        greet = "Good afternoon"
    elif 16 <= ctt < 19:
        greet = "Good evening"
    elif 19 <= ctt <= 23:
        greet = "Good night"
    return render_template('diary.html',ctt = ctt,greet = greet)
@app.route('/save_diary',methods=['POST','GET'])
def save_diary():
    dt = datetime.now(ZoneInfo("Asia/Kolkata"))
    cd = dt.strftime("%Y-%m-%d %Z") 
    ct = dt.strftime("%I:%M %p")
    date = f"{cd} | {ct}"
    diary = request.form['diary_entry']
    if request.method == 'POST':
        choice = request.form.get('option').strip().lower()
    p_diary =[]    
    if choice == 'yes':
        if os.path.exists('diary.txt'):
            with open('diary.txt','r') as f:

                diary_text = f.readlines()
        p_diary = diary_text
        n_diary = diary.splitlines()
        
        with open('diary.txt','a') as f:
            f.write( date+'\n'+ diary + '\n\n')
        return render_template('save_diary.html', p_diary = p_diary, n_diary = n_diary,choice = choice,date = date)       
    elif choice =='no':
        unnamed ='Your data will loss'
        if os.path.exists('diary.txt'):
            with open('diary.txt','r') as f:
                diary_text = f.readlines()
        p_diary = diary_text
        n_diary = diary.splitlines()
        
    return render_template('save_diary.html', p_diary = p_diary, n_diary = n_diary,unnamed = unnamed ,choice = choice,date = date)


if __name__ == '__main__':
    app.run(debug = True)