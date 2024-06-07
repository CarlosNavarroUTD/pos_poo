import sqlite3

class DataBase:
    def __init__(self, nombre_bd):
        self.nombre_bd = nombre_bd
        self.conexion = None
        self.cursor = None

    def conect(self):
        self.conexion = sqlite3.connect(self.nombre_bd)
        self.cursor = self.conexion.cursor()
#====================================
#          Crear Tablas
#====================================


    def crear_tablas(self):
        # Crear la tabla de usuarios si no existe
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER,
            email TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            Barcode TEXT NOT NULL,
            name_product TEXT NOT NULL,
            cantidad_cajas INTEGER,
            precio_por_unidad REAL,
            precio_mayoreo REAL,
            tipo_de_producto TEXT,
            marca TEXT,
            unidades_por_caja INTEGER,
            cantidad_unidades INTEGER
        )
        ''')

        self.conexion.commit()

#====================================
#          Insertar Usuario
#====================================

    def InsUser(self, nombre, edad, email):
        self.cursor.execute('''
        INSERT INTO usuarios (nombre, edad, email) VALUES (?, ?, ?)
        ''', (nombre, edad, email))
        self.conexion.commit()
        print("Usuario insertado correctamente.")




#====================================
#          CRUD PRODUCTS
#====================================
#====================================
#          Insertar Producto
#====================================
    def InsProd(self, Barcode, name_product, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades):
        self.cursor.execute('''
        INSERT INTO productos (Barcode, name_product, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (Barcode, name_product, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades))
        self.conexion.commit()
        print("Producto insertado correctamente.")

    
#====================================
#          Leer producto
#====================================
    def ReadProd(self, producto_id):
        self.cursor.execute('''
        SELECT * FROM productos WHERE id = ?
        ''', (producto_id,))
        producto = self.cursor.fetchone()
        if producto:
            print(f"Producto ID: {producto[0]}")
            print(f"Barcode: {producto[1]}")
            print(f"Nombre: {producto[2]}")
            print(f"Cantidad de cajas: {producto[3]}")
            print(f"Precio por unidad: {producto[4]}")
            print(f"Precio por mayoreo: {producto[5]}")
            print(f"Tipo de producto: {producto[6]}")
            print(f"Marca: {producto[7]}")
            print(f"Unidades por caja: {producto[8]}")
            print(f"Cantidad de unidades: {producto[9]}")
        else:
            print("Producto no encontrado.")


#====================================
#          Actualizar producto
#====================================

    def UptProd(self, producto_id, Barcode=None, name_product=None, cantidad_cajas=None, precio_por_unidad=None, precio_mayoreo=None, tipo_de_producto=None, marca=None, unidades_por_caja=None, cantidad_unidades=None):
        producto = self.cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,)).fetchone()
        if producto:
            Barcode = Barcode if Barcode else producto[1]
            name_product = name_product if name_product else producto[2]
            cantidad_cajas = cantidad_cajas if cantidad_cajas else producto[3]
            precio_por_unidad = precio_por_unidad if precio_por_unidad else producto[4]
            precio_mayoreo = precio_mayoreo if precio_mayoreo else producto[5]
            tipo_de_producto = tipo_de_producto if tipo_de_producto else producto[6]
            marca = marca if marca else producto[7]
            unidades_por_caja = unidades_por_caja if unidades_por_caja else producto[8]
            cantidad_unidades = cantidad_unidades if cantidad_unidades else producto[9]

            self.cursor.execute('''
            UPDATE productos
            SET Barcode = ?, name_product = ?, cantidad_cajas = ?, precio_por_unidad = ?, precio_mayoreo = ?, tipo_de_producto = ?, marca = ?, unidades_por_caja = ?, cantidad_unidades = ?
            WHERE id = ?
            ''', (Barcode, name_product, cantidad_cajas, precio_por_unidad, precio_mayoreo, tipo_de_producto, marca, unidades_por_caja, cantidad_unidades, producto_id))
            self.conexion.commit()
            print("Producto actualizado correctamente.")
        else:
            print("Producto no encontrado.")

#====================================
#          Eliminar producto
#====================================
    def DelProd(self, producto_id):
        self.cursor.execute('''
        DELETE FROM productos WHERE id = ?
        ''', (producto_id,))
        self.conexion.commit()
        print("Producto eliminado correctamente.")

#====================================
#          Cerrar Conexión
#====================================

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()








