from pymongo import MongoClient
from flask import current_app
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

_client = None
_db = None

def init_db(app):
    """Inicializa el cliente y la base de datos a partir de app.config."""
    global _client, _db
    uri = app.config.get('MONGO_URI') or app.config.get('MONGODB_URI')
    if not uri:
        raise RuntimeError("MONGO_URI (o MONGODB_URI) no está configurada en app.config")
    _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db_name = app.config.get('MONGO_DBNAME') or (uri.rsplit('/', 1)[-1] if '/' in uri else None)
    if not db_name:
        db_name = 'InventarioCC'
    _db = _client[db_name]
    # guardar referencias en config para acceso desde current_app
    try:
        app.config['_db'] = _db
        app.config['_mongo_client'] = _client
    except Exception:
        pass
    return _db

def get_db():
    """Devuelve la instancia de la BD (requiere init_db llamada desde la app)."""
    global _db
    # comparar explícitamente con None (Database no implementa truth value testing)
    if _db is not None:
        return _db
    if current_app is not None and '_db' in current_app.config:
        return current_app.config['_db']
    raise RuntimeError("La BD no está inicializada. Llama a init_db(app) primero.")

def check_db_connection():
    """Hace ping al servidor MongoDB. Devuelve True si OK, lanza excepción si falla."""
    global _client
    # comparar explícitamente con None
    if _client is None:
        raise RuntimeError("Cliente Mongo no inicializado. Llama a init_db(app).")
    resp = _client.admin.command('ping')
    return resp.get('ok') == 1.0

# Inserciones y consultas útiles para probar
def add_inventory_item(item):
    """
    Inserta un documento de inventario.
    item: dict con campos (id, code, product, shelves, floors, packs) — flexible.
    Retorna inserted_id.
    """
    db = get_db()
    result = db.inventory.insert_one(item)
    return result.inserted_id

def add_transaction(tx):
    """
    Inserta un documento de transacción.
    tx: dict con campos (id, date, product, total, ...) — flexible.
    Retorna inserted_id.
    """
    db = get_db()
    result = db.transactions.insert_one(tx)
    return result.inserted_id

def find_inventory(query=None, limit=300):
    query = query or {}
    return list(get_db().inventory.find(query).limit(limit))

def find_transactions(query=None, projection=None, sort=None, limit=1000,
                      aggregate_by_product=False, group_by_code=False, tz_name="America/Bogota"):
    """
    Devuelve transacciones del día actual (según tz_name).
    - Si aggregate_by_product=False devuelve documentos individuales (incluye 'codigo' si existe).
    - Si aggregate_by_product=True devuelve suma de 'total' por producto;
      si group_by_code=True agrupa por (product,codigo,inventory_id) y además trae
      el campo 'packs' desde la colección inventory usando inventory_id.
    Resultado agregado (group_by_code=True) incluye:
      { product, codigo, inventory_id, total, count, packs }
    """
    db = get_db()

    tz = ZoneInfo(tz_name)
    now_tz = datetime.now(tz)
    start = now_tz.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    q = query.copy() if query else {}
    if 'date' not in q:
        q['date'] = {'$gte': start, '$lt': end}

    if aggregate_by_product:
        if group_by_code:
            # Agrupar por producto + código + inventory_id y luego lookup a inventory para obtener 'packs'
            pipeline = [
                {'$match': q},
                {'$group': {
                    '_id': {
                        'product': '$product',
                        'codigo': '$codigo',
                        'inventory_id': '$inventory_id'
                    },
                    'total': {'$sum': '$total'},
                    'count': {'$sum': 1}
                }},
                # proyectar campos raíz para facilitar lookup
                {'$addFields': {
                    'product': '$_id.product',
                    'codigo': '$_id.codigo',
                    'inventory_id': '$_id.inventory_id'
                }},
                # lookup para traer el documento de inventory que corresponde a inventory_id
                {'$lookup': {
                    'from': 'inventory',
                    'localField': 'inventory_id',
                    'foreignField': '_id',
                    'as': 'inventory_doc'
                }},
                # si existe, tomar el primero
                {'$unwind': {'path': '$inventory_doc', 'preserveNullAndEmptyArrays': True}},
                # proyectar resultado final y extraer 'packs' desde inventory_doc.packs (si existe)
                {'$project': {
                    '_id': 0,
                    'product': 1,
                    'codigo': 1,
                    'inventory_id': 1,
                    'total': 1,
                    'count': 1,
                    'packs': {'$ifNull': ['$inventory_doc.packs', None]}
                }},
                {'$sort': {'total': -1}}
            ]
            return list(db.transactions.aggregate(pipeline))
        else:
            # agrupar solo por producto; incluir un ejemplo de codigo (first)
            pipeline = [
                {'$match': q},
                {'$group': {
                    '_id': '$product',
                    'total': {'$sum': '$total'},
                    'count': {'$sum': 1},
                    'codigo': {'$first': '$codigo'},
                    'inventory_id': {'$first': '$inventory_id'}
                }},
                {'$project': {
                    '_id': 0,
                    'product': '$_id',
                    'codigo': 1,
                    'inventory_id': 1,
                    'total': 1,
                    'count': 1
                }},
                {'$sort': {'total': -1}}
            ]
            return list(db.transactions.aggregate(pipeline))

    # fallback: devolver documentos individuales (incluye 'codigo' y 'inventory_id' si están en los docs)
    cursor = db.transactions.find(q, projection or {})
    if sort:
        cursor = cursor.sort(sort)
    if limit and isinstance(limit, int) and limit > 0:
        cursor = cursor.limit(limit)
    return list(cursor)