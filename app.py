from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Usamos el backend 'Agg' para evitar el uso de Tkinter
matplotlib.use('Agg')

# Inicialización de la app
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db?check_'  # Puedes usar MySQL, PostgreSQL, etc.
db = SQLAlchemy(app)

# Modelo de la base de datos para los mensajes
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

# Función para generar los gráficos
def generar_graficos():
    # Cargar los archivos CSV
    df_price = pd.read_csv('price.csv')
    df_rating = pd.read_csv('rating.csv')

    # Gráfico de barras para los precios
    df_top10_price = df_price.head(10)  # Seleccionar los primeros 10 productos
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.bar(df_top10_price['title'], df_top10_price['price'], color='skyblue')
    ax.set_xlabel('Producto')
    ax.set_ylabel('Precio en pesos colombianos')
    ax.set_title('Precios de los productos principales')
    plt.xticks(rotation=25, ha='right')
    plt.savefig('static/img/grafico_precios_top10.png')
    plt.close(fig)  # Cerrar el gráfico para liberar memoria

    # Gráfico de pie para los ratings
    df_rating = df_rating.rename(columns={'title': 'Producto', 'rating': 'Valor'})
    df_top10_rating = df_rating.head(10)  # Seleccionar los primeros 10 productos
    valores = df_top10_rating['Valor']
    valores_porcentaje = (valores / valores.sum()) * 100  # Convertir a porcentaje

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(valores_porcentaje, labels=df_top10_rating['Producto'], autopct='%1.1f%%', startangle=140)
    ax.set_title('Los más buscados')
    plt.savefig('static/img/grafico_pie_rating.png')
    plt.close(fig)  # Cerrar el gráfico para liberar memoria

# Generar los gráficos cuando el servidor se inicia
generar_graficos()

# Rutas de la aplicación

# Página de inicio con los gráficos
@app.route('/')
def index():
    return render_template('index.html', img_barras='static/img/grafico_precios_top10.png', img_pie='static/img/grafico_pie_rating.png')

# Ruta para la página de ayuda (con formulario)

@app.route('/ayuda', methods=['GET', 'POST'])
def ayuda():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        mensaje = data.get('mensaje')

        # Guardar el mensaje en la base de datos
        nuevo_mensaje = Mensaje(nombre=nombre, correo=correo, mensaje=mensaje)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        return jsonify({"message": "Mensaje enviado con éxito"}), 200  # Responder con JSON
    
    return render_template('ayuda.html')


# Ruta para la página de mercado
@app.route('/mercado')
def mercado():
    return render_template('mercado.html')

# Ruta para la página de cupones
@app.route('/cupones')
def cupones():
    return render_template('cupones.html')

# Ruta para la página de carrito
@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

# Ruta para la página de inicio de sesión
@app.route('/iniciosesion')
def iniciosesion():
    return render_template('iniciosesion.html')

# Ruta para la página de términos y condiciones
@app.route('/terminoscondiciones')
def terminoscondiciones():
    return render_template('terminoscondiciones.html')

# Ejecutar la creación de la tabla dentro del contexto de la aplicación
if __name__ == '__main__':
    with app.app_context():  # Crear el contexto de la aplicación
        db.create_all()      # Crear todas las tablas
    app.run(debug=True)