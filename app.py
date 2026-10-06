import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response

app = Flask(__name__)
DATA_FILE = 'store_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "config": {
                "store_name": "Techsy Zone ✨",
                "logo_url": "https://imgur.com",
                "tagline": "HIGH-PERFORMANCE TECH STORE",
                "hero_title": "NEON—LAPTOPS",
                "hero_subtitle": "أفضل المنتجات العالمية بجودة استثنائية وأسعار تنافسية بين يديك عبر Techsy Zone",
                "btn_hero_text": "LAUNCH INVENTORY // تصفح العتاد",
                "section_title": "القطع والعتاد المتوفر حالياً",
                "whatsapp_number": "201000000000",
                "messenger_username": "your.fb.page",
                "cyan_color": "#00f3ff",
                "magenta_color": "#ff007f",
                "bg_color": "#090f1c",
                "card_bg": "#0d1527",
                "footer_text": "TECHSY ZONE STORE. ALL RIGHTS RESERVED.",
                "visitor_count": 0
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

@app.route('/')
def home():
    data = load_data()
    
    # 1. فحص إذا كان الزائر هو الأدمن (أنت) عبر الكوكيز المخصص
    is_admin_cookie = request.cookies.get('is_admin')
    
    # 2. فحص إذا كان الزائر هو بوت المراقبة تلقائياً (User-Agent)
    user_agent = request.headers.get('User-Agent', '').lower()
    bot_keywords = ['uptimerobot', 'cron-job', 'headlesschrome', 'curl', 'wget', 'robot', 'spider', 'bot']
    is_bot = any(keyword in user_agent for keyword in bot_keywords)
    
    # زيادة العداد فقط إذا لم يكن بوت ولم تكن أنت الأدمن
    if not is_admin_cookie and not is_bot:
        if "visitor_count" not in data['config']:
            data['config']['visitor_count'] = 0
        data['config']['visitor_count'] += 1
        save_data(data)
        
    return render_template('index.html', products=data['products'], config=data['config'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    data = load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_config':
            data['config']['store_name'] = request.form.get('store_name')
            data['config']['logo_url'] = request.form.get('logo_url')
            data['config']['tagline'] = request.form.get('tagline')
            data['config']['hero_title'] = request.form.get('hero_title')
            data['config']['hero_subtitle'] = request.form.get('hero_subtitle')
            data['config']['btn_hero_text'] = request.form.get('btn_hero_text')
            data['config']['section_title'] = request.form.get('section_title')
            data['config']['whatsapp_number'] = request.form.get('whatsapp_number')
            data['config']['messenger_username'] = request.form.get('messenger_username')
            data['config']['cyan_color'] = request.form.get('cyan_color')
            data['config']['magenta_color'] = request.form.get('magenta_color')
            data['config']['bg_color'] = request.form.get('bg_color')
            data['config']['card_bg'] = request.form.get('card_bg')
            data['config']['footer_text'] = request.form.get('footer_text')
            save_data(data)
            
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
    
    # عند دخولك لصفحة الأدمن، نزرع كوكيز في متصفحك يمنع احتساب زياراتك مستقبلاً
    response = make_response(render_template('admin.html', products=data['products'], config=data['config']))
    response.set_cookie('is_admin', 'true', max_age=31536000) # صالح لمدة سنة كاملة
    return response

# مسار تصفير عداد الزوار من جديد
@app.route('/admin/reset-visitors')
def reset_visitors():
    data = load_data()
    data['config']['visitor_count'] = 0
    save_data(data)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:product_id>')
def delete_product(product_id):
    data = load_data()
    data['products'] = [p for p in data['products'] if p['id'] != product_id]
    save_data(data)
    return redirect(url_for('admin'))

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
        "price": req_data.get('price', 'راجع الوصف'),
        "image": req_data.get('image', 'https://unsplash.com'),
        "desc": req_data.get('desc', '')
    }
    data['products'].append(new_product)
    save_data(data)
    return jsonify({"status": "success", "message": "تم التحديث"}), 200

if __name__ == '__main__':
    app.run(debug=True)
