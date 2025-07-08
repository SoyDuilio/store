PERSONAL_MOCK = [
    {
        "id": 1, 
        "nombre_completo": "Ana Paredes", 
        "cargo": "Cajera Principal", 
        "sueldo_base": 1200.00,
        "frecuencia_pago": "MENSUAL"
    },
    {
        "id": 2, 
        "nombre_completo": "Luis Torres", 
        "cargo": "Almacenero", 
        "sueldo_base": 1050.00,
        "frecuencia_pago": "MENSUAL"
    },
]

MOVIMIENTOS_PLANILLA_MOCK = {
    1: [ # Movimientos de Ana Paredes (id=1)
        {"tipo": "ADELANTO_EFECTIVO", "monto": 100.00, "descripcion": "Adelanto del 5 de mes"},
        {"tipo": "DESCUENTO_PRODUCTO", "monto": 35.00, "descripcion": "1x Ron Cartavio Black"},
        {"tipo": "BONO_DESEMPENO", "monto": 50.00, "descripcion": "Bono por ventas del mes"},
        {"tipo": "DESCUENTO_TARDANZA", "monto": 10.00, "descripcion": "2 tardanzas"},
    ],
    2: [ # Movimientos de Luis Torres (id=2)
        {"tipo": "ADELANTO_EFECTIVO", "monto": 50.00, "descripcion": "Adelanto del 10 de mes"},
    ]
}

GASTOS_MOCK = [
    {"id": 1, "fecha": "2024-05-20", "monto": 50.00, "tipo": "Servicios", "descripcion": "Pago de Internet del local", "responsable": "Ana Paredes", "autorizado_por": "Gerente"},
    {"id": 2, "fecha": "2024-05-19", "monto": 25.00, "tipo": "Movilidad", "descripcion": "Taxi para llevar documentos al contador", "responsable": "Luis Torres", "autorizado_por": "Gerente"},
    {"id": 3, "fecha": "2024-05-18", "monto": 250.00, "tipo": "Compras", "descripcion": "Compra de bolsas y material de limpieza", "responsable": "Ana Paredes", "autorizado_por": "Gerente"},
    {"id": 4, "fecha": "2024-05-15", "monto": 150.00, "tipo": "Contador", "descripcion": "Pago honorarios contador", "responsable": "Gerente", "autorizado_por": "Gerente"},
]