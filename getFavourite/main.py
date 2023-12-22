from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mysql.connector import connect, Error
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "iznaursdatabase2"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("favourite2")


app = FastAPI()

def start_con():
    with tracer.start_as_current_span("izazursdata"):
        try:
            connection = connect(
                host=os.getenv('MYSQL_HOST', 'mysql_db'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'Iznarocky'),
            )
            print(connection)
            create_db_query = "CREATE DATABASE IF NOT EXISTS books"
            use_db_query = "USE books"
            create_table_query = "CREATE TABLE IF NOT EXISTS books (id int)"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                cursor.execute(use_db_query)
                cursor.execute(create_table_query)
            connection.commit()
        except Error as e:
            print(e)
            return
        return connection

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/', response_model=Any)
async def root(id: int):
    connection = start_con()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO books VALUES ({id})")
        connection.commit()
    except Error as e:
        print(e)
    return 1

@app.get('/')
async def get_data():
    connection = start_con()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM books.books")
            return [j for i in cursor.fetchall() for j in i]
    except Error as e:
        print(e)
    return list()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3001)
