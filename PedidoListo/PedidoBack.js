// #1 importamos librerias y frameworks
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

// #2 configuramos el servidor
const app = express();
const port = Number(process.env.PORT) || 3000;

// #3 configuramos la conexion a PostgreSQL
const pool = new Pool({
  user: process.env.PGUSER || 'postgres',
  host: process.env.PGHOST || 'localhost',
  database: process.env.PGDATABASE || 'pedidos',
  password: process.env.PGPASSWORD || 'password',
  port: Number(process.env.PGPORT) || 5432,
});

// #4 middlewares
app.use(cors());
app.use(express.json());

const DB_UNAVAILABLE_CODES = new Set([
  'ECONNREFUSED',
  'ENOTFOUND',
  'ETIMEDOUT',
  'EAI_AGAIN',
  '57P01',
]);

function isDbUnavailableError(error) {
  return Boolean(error && DB_UNAVAILABLE_CODES.has(error.code));
}

function sendDbUnavailable(res, context) {
  return res.status(503).json({
    ok: false,
    error: 'Base de datos no disponible',
    code: 'DB_UNAVAILABLE',
    context,
  });
}

// #5 rutas

// obtener pedidos
app.get('/api/pedidos', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM pedidos');
    return res.json(result.rows);
  } catch (error) {
    console.error(error);
    if (isDbUnavailableError(error)) {
      return sendDbUnavailable(res, 'GET /api/pedidos');
    }
    return res.status(500).json({ ok: false, error: 'Error al obtener pedidos' });
  }
});

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
     if (!item || typeof item !== 'object') {
  errores.push(`items[${index}] debe ser un objeto`);
  return;
      }
      if (typeof item.nombre !== 'string' || item.nombre.trim().length === 0) {
        errores.push(`items[${index}].nombre es obligatorio`);
      }
      if (!Number.isInteger(item.cantidad) || item.cantidad <= 0) {
        errores.push(`items[${index}].cantidad debe ser un entero mayor a 0`);
      }
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

  let dbClient;

  try {
    dbClient = await pool.connect();
    await dbClient.query('BEGIN');

    const pedidosCreados = [];
    for (const item of items) {
      const result = await dbClient.query(
        'INSERT INTO pedidos (cliente, producto, cantidad) VALUES ($1, $2, $3) RETURNING *',
        [cliente.trim(), item.nombre.trim(), item.cantidad]
      );
      pedidosCreados.push(result.rows[0]);
    }

    await dbClient.query('COMMIT');
    return res.status(201).json({ ok: true, pedidos: pedidosCreados });
  } catch (error) {
    if (dbClient) {
      try {
        await dbClient.query('ROLLBACK');
      } catch (rollbackError) {
        console.error(rollbackError);
      }
    }

    console.error(error);
    if (isDbUnavailableError(error)) {
      return sendDbUnavailable(res, 'POST /api/pedidos');
    }
    return res.status(500).json({ ok: false, error: 'Error al crear pedido' });
  } finally {
    if (dbClient) {
      dbClient.release();
    }
  }
});

app.get('/health/db', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    return res.status(200).json({ ok: true, db: 'up' });
  } catch (error) {
    console.error(error);
    if (isDbUnavailableError(error)) {
      return res.status(503).json({ ok: false, db: 'down', code: 'DB_UNAVAILABLE' });
    }
    return res.status(500).json({ ok: false, db: 'error' });
  }
});

app.get('/', (req, res) => {
  return res.json({ ok: true, service: 'PedidoListo API' });
});

app.use((error, req, res, next) => {
  const isInvalidJson =
    error instanceof SyntaxError &&
    error.status === 400 &&
    Object.prototype.hasOwnProperty.call(error, 'body');

  if (isInvalidJson) {
    return res.status(400).json({
      ok: false,
      error: 'JSON invalido en el body',
    });
  }

  return next(error);
});

// #6 levantamos el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
}); 
