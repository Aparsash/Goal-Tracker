from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# مسیر فایل داده‌ها
DATA_FILE = 'goals.json'

def load_goals():
    """بارگیری اهداف از فایل JSON"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            print("Content of goals.json:")
            print(content)  # چاپ محتوای فایل
            return json.loads(content)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def save_goals(goals):
    """ذخیره اهداف در فایل JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(goals, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    """نمایش صفحه اصلی (فرم ثبت پیشرفت)"""
    goals = load_goals()
    return render_template('index.html', goals=goals)

@app.route('/submit', methods=['POST'])
def submit():
    """دریافت پیشرفت روزانه از فرم و ذخیره آن"""
    goals = load_goals()
    
    # دریافت تاریخ فعلی
    today = datetime.now().strftime('%Y-%m-%d')
    
    for goal in goals:
        # دریافت پیشرفت از فرم
        progress_value = float(request.form.get(str(goal['id']), 0))
        
        # اضافه کردن پیشرفت به لیست پیشرفت هدف
        goal['progress'].append({
            'date': today,
            'value': progress_value
        })
    
    # ذخیره اهداف به‌روزرسانی‌شده
    save_goals(goals)
    
    return redirect(url_for('report'))

@app.route('/report')
def report():
    """نمایش گزارش پیشرفت"""
    goals = load_goals()
    return render_template('report.html', goals=goals)

if __name__ == '__main__':
    app.run(debug=True)