from PyLibreHardwareMonitor import Computer
from time import sleep
import datetime
import psycopg2

while True:
    computer = Computer()
    cpu_data = str(computer.cpu)
    cpu = cpu_data.replace("'", '"')
    data_cpu = cpu.replace('None', 'null')

    gpu_data = str(computer.gpu)
    gpu = gpu_data.replace("'", '"')
    data_gpu = gpu.replace('None', 'null')

    memory_data = str(computer.memory)
    memory = memory_data.replace("'", '"')
    data_memory = memory.replace('None', 'null')

    pc_id = '689cab89-746d-4546-beea-dcadb9fdcb72'

    # query = f"""insert into tbl_data (id, cpu_json, timestamp, pc_id) values (null, '{data}', null, '88cd81d1-51c6-4aaf-8799-eb74d703aa34');"""
    query = f"""INSERT INTO pcdata_pcdata (id, cpu_json, gpu_json, memory_json, "timestamp", pc_id) VALUES (gen_random_uuid(), '{data_cpu}', '{data_gpu}', '{data_memory}', now(), '{pc_id}');"""


    # print("\n",query)

    conn = psycopg2.connect(database = "db-pcanlizz", 
                        user = "postgres", 
                        host= '192.168.1.88',
                        password = ".24@Phenom#",
                        port = 5432)

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    print(datetime.datetime.now())
    # print(data_cpu)

    # sleep(60)

'''
drop table tbl_data;

create table tbl_data (
	id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	usr_id varchar(255) not null,
	cpu json,
	timestamp timestamp default current_timestamp
)
'''