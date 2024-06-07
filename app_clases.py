from flask import Flask, render_template, request, redirect, url_for
from ConexionDB import DataBase
import datetime
import jsonify


app = Flask(__name__)

#===============================
#buscar por barcode
#===============================
@app.route('/buscar_barcode', methods=['GET'])
def buscar_barcode():
    term = request.args.get('term')
    db = DataBase('AxolBD.db')
    db.conectar()
    db.cursor.execute("SELECT Barcode, name_product FROM productos WHERE Barcode LIKE ?", ('%' + term + '%',))
    resultados = db.cursor.fetchall()
    db.cerrar_conexion()
    response = [{'label': f"{r[0]} - {r[1]}", 'value': r[0]} for r in resultados]
    return jsonify(response)



#===============================
#Generar Ventas
#===============================


@app.route('/sales', methods=['GET', 'POST'])
def ventas():
    if request.method == 'POST':
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_cliente = request.form['id_cliente']
        id_usuario = request.form['id_usuario']
        total = float(request.form['total'])

        db = DataBase('AxolBD.db')
        db.conectar()
        db.cursor.execute('''
        INSERT INTO ventas (fecha, id_cliente, id_usuario, total) 
        VALUES (?, ?, ?, ?)
        ''', (fecha, id_cliente, id_usuario, total))
        id_venta = db.cursor.lastrowid

        productos = request.form.getlist('productos')
        cantidades = request.form.getlist('cantidades')
        precios_unitarios = request.form.getlist('precios_unitarios')

        for producto, cantidad, precio_unitario in zip(productos, cantidades, precios_unitarios):
            db.cursor.execute('''
            INSERT INTO detalles_ventas (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
            ''', (id_venta, producto, cantidad, precio_unitario))

        db.conexion.commit()
        db.cerrar_conexion()

        return redirect(url_for('sales'))

    return render_template('sales.html')

#===============================
#Rute Add producto to DB
#===============================

@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        Barcode = request.form['Barcode']
        name_product = request.form['name_product']
        cantidad_cajas = int(request.form['cantidad_cajas'])
        precio_por_unidad = float(request.form['precio_por_unidad'])
        precio_mayoreo = float(request.form['precio_mayoreo'])
        tipo_de_producto = request.form['tipo_de_producto']
        marca = request.form['marca']
        unidades_por_caja = int(request.form['unidades_por_caja'])
        cantidad_unidades = int(request.form['cantidad_unidades'])
        
        db = DataBase('AxolBD.db')
        db.conect()
        db.InsProd(Barcode, name_product, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades)
        db.cerrar_conexion()

        return redirect(url_for('addProduct'))

    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
