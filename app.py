import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# مسار ملف البيانات الافتراضي
DATA_FILE = 'store_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "config": {
                "store_name": "متجري العصري ✨",
                "hero_title": "اكتشف الجيل الجديد من المنتجات",
                "hero_subtitle": "أفضل المنتجات العالمية بجودة استثنائية وأسعار تنافسية بين يديك",
                "whatsapp_number": "201000000000",
                "messenger_username": "your.fb.page",
                "primary_color": "indigo",  # خيارات: indigo, green, blue, purple, rose
                "theme_mode": "light" # الافتراضي للزائر
            },
            "products": [
                {
                    "id": 1,
                    "name": "سماعة محيطية لاسلكية",
                    "price": "$99",
                    "image": "https://unsplash.com",
                    "desc": "صوت نقي عالي الدقة مع ميزة عزل الضوضاء النشط وبطارية تدوم طويلاً."
                }
            ]
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# صفحة الزوار الرئيسية
@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', products=data['products'], config=data['config'])

# لوحة التحكم الشاملة (رابط الأدمن)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    data = load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        
        # 1. تحديث الإعدادات العامة وشكل الموقع
        if action == 'update_config':
            data['config']['store_name'] = request.form.get('store_name')
            data['config']['hero_title'] = request.form.get('hero_title')
            data['config']['hero_subtitle'] = request.form.get('hero_subtitle')
            data['config']['whatsapp_number'] = request.form.get('whatsapp_number')
            data['config']['messenger_username'] = request.form.get('messenger_username')
            data['config']['primary_color'] = request.form.get('primary_color')
            save_data(data)
            
        # 2. إضافة منتج جديد
        elif action == 'add_product':
            new_id = max([p['id'] for p in data['products']], default=0) + 1
            new_product = {
                "id": new_id,
                "name": request.form.get('name'),
                "price": request.form.get('price'),
                "image": request.form.get('image'),
                "desc": request.form.get('desc')
            }
            data['products'].append(new_product)
            save_data(data)
            
        return redirect(url_for('admin'))
        
    return render_template('admin.html', products=data['products'], config=data['config'])

# حذف منتج
@app.route('/admin/delete/<int:product_id>')
def delete_product(product_id):
    data = load_data()
    data['products'] = [p for p in data['products'] if p['id'] != product_id]
    save_data(data)
    return redirect(url_for('admin'))

# واجهة برمجية مصغرة (API) لتلقي المنتجات تلقائياً من Make.com (الفيسبوك)
@app.route('/api/webhook/facebook', methods=['POST'])
def fb_webhook():
    req_data = request.get_json()
    if not req_data or 'name' not in req_data:
        return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400
        
    data = load_data()
    new_id = max([p['id'] for p in data['products']], default=0) + 1
    new_product = {
        "id": new_id,
        "name": req_data.get('name'),
        "price": req_data.get('price', 'غير محدد'),
        "image": req_data.get('image', 'https://unsplash.com'),
        "desc": req_data.get('desc', '')
    }
    data['products'].append(new_product)
    save_data(data)
    return jsonify({"status": "success", "message": "تمت إضافة المنتج بنجاح من فيسبوك"}), 200

if __name__ == '__main__':
    app.run(debug=True)
