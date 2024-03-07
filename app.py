from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'erterterterer'
cart_items = []

@app.route('/')
def main_site():
    return render_template("main_site.html")


@app.route('/cart')
def cart():
    total_cost = sum(float(item['price']) for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_cost=total_cost)



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        product = request.form.get('product')
        price = float(request.form.get('price'))
        existing_item = next((item for item in cart_items if item['product'] == product), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart_items.append({'product': product, 'price': price, 'quantity': 1})
    session['total_cost'] = sum(item['price'] * item['quantity'] for item in cart_items)
    return redirect(url_for('main_site'))

@app.route('/update_cart/<product>', methods=['POST'])
def update_cart(product):
    action = request.form['action']
    if action == '+':
        for item in cart_items:
            if item['product'] == product:
                item['quantity'] += 1
                break
    elif action == '-':
        for item in cart_items:
            if item['product'] == product:
                item['quantity'] -= 1
                if item['quantity'] == 0:
                    cart_items.remove(item)
                break
    session['total_cost'] = sum(item['price'] * item['quantity'] for item in cart_items)
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    cart_items.clear()
    session.pop('total_cost', None)
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
