from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

def conectar_bd_sqlite():
    # Reemplaza 'tu_database.db' con el nombre de tu base de datos
    return sqlite3.connect('tu_database.db')

@app.route('/', methods=['GET', 'POST'])  # Cambio aquí para hacer que esta sea la ruta principal
def add_or_list_products():
    if request.method == 'POST':
        # Recogida de datos desde el formulario insert_product.html
        barcode = request.form['barcode']
        product_name = request.form['name_product']
        cantidad_cajas = int(request.form['cantidad_cajas'])
        precio_por_unidad = float(request.form['precio_por_unidad'])
        precio_mayoreo = float(request.form['precio_mayoreo'])
        tipo_de_producto = request.form['tipo_de_producto']
        marca = request.form['marca']
        unidades_por_caja = int(request.form['unidades_por_caja'])
        cantidad_unidades = int(request.form['cantidad_unidades'])

        # Conexión a la base de datos
        conn = conectar_bd_sqlite()
        cursor = conn.cursor()

        # Inserta los datos en la base de datos
        cursor.execute("INSERT INTO products (barcode, name, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (barcode, product_name, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades))
        conn.commit()
        cursor.close()
        conn.close()

        # Opcional: Redirigir a otra página, como una lista de productos, después de insertar
        return redirect('/productlist')
    else:
        # Renderiza insert_product.html por defecto si el método es GET
        return render_template('insert_product.html')

@app.route('/productlist')
def product_list():
    conn = conectar_bd_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('product_list.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
