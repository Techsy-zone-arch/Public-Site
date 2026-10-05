from flask import Flask, render_template

app = Flask(__name__)

# بيانات المنتجات التجريبية لمتجرك
PRODUCTS = [
    {
        "id": 1,
        "name": "سماعة رأس لاسلكية فاخرة",
        "price": "99$",
        "image": "https://unsplash.com",
        "desc": "صوت محيطي نقي مع ميزة إلغاء الضوضاء وعمر بطارية يدوم 40 ساعة."
    },
    {
        "id": 2,
        "name": "ساعة ذكية رياضية",
        "price": "149$",
        "image": "https://unsplash.com",
        "desc": "مقاومة للماء، تتبع نبضات القلب والأنشطة الرياضية مع شاشة AMOLED."
    },
    {
        "id": 3,
        "name": "حقيبة ظهر عصرية للمحمول",
        "price": "49$",
        "image": "https://unsplash.com",
        "desc": "منفذ شحن USB مدمج، مقاومة للسرقة والمياه، وتتسع لجميع مستلزماتك."
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

if __name__ == '__main__':
    app.run(debug=True)
