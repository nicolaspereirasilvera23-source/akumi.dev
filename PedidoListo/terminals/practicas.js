// #1 importamos librerias y frameworks
const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

// #2 configuramos el servidor
const app = express();
const port = 3000;

// #3 configuramos la conexion a PostgreSQL
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'pedidos',
  password: 'password',
  port: 5432,
});

// #4 middlewares
app.use(cors());
app.use(express.json());

// #5 rutas

// obtener pedidos
app.get('/api/pedidos', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM pedidos');
    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error al obtener pedidos' });
  }
});

function validarItem(item, index) {
  const errores = [];

  if (!item || typeof item !== 'object') {
    errores.push(`items[${index}] debe ser un objeto`);
    return errores;
  }

  if (typeof item.nombre !== 'string' || item.nombre.trim().length === 0) {
    errores.push(`items[${index}].nombre es obligatorio`);
  }

  if (!Number.isInteger(item.cantidad) || item.cantidad <= 0) {
    errores.push(`items[${index}].cantidad debe ser un entero mayor a 0`);
  }

  if (typeof item.precio !== 'number' || Number.isNaN(item.precio) || item.precio < 0) {
    errores.push(`items[${index}].precio debe ser un numero mayor o igual a 0`);
  }

  return errores;
}

function validarPedido(body) {
  const errores = [];

  if (!body || typeof body !== 'object') {
    return ['El body del pedido es invalido'];
  }

  if (typeof body.cliente !== 'string' || body.cliente.trim().length === 0) {
    errores.push('cliente es obligatorio');
  }

  if (!Array.isArray(body.items)) {
    errores.push('items debe ser un array');
  } else if (body.items.length === 0) {
    errores.push('items no puede estar vacio');
  } else {
    body.items.forEach((item, index) => {
      errores.push(...validarItem(item, index));
    });
  }

  return errores;
}

// crear pedido
app.post('/api/pedidos', async (req, res) => {
  const { cliente, items } = req.body;
  const errores = validarPedido(req.body);

  if (errores.length > 0) {
    return res.status(400).json({ ok: false, errores });
  }

  try {
    const inserts = items.map((item) =>
      pool.query(
        'INSERT INTO pedidos (cliente, producto, cantidad) VALUES ($1, $2, $3) RETURNING *',
        [cliente.trim(), item.nombre.trim(), item.cantidad]
      )
    );

    const results = await Promise.all(inserts);
    const pedidosCreados = results.map((result) => result.rows[0]);

    res.status(201).json({ ok: true, pedidos: pedidosCreados });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error al crear pedido' });
  }
});

app.get('/', (req, res) => {
  return res.json({ ok: true, service: 'PedidoListo API' });
});

// #6 levantamos el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
