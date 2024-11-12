# PcAnlizz Project

Project in development  
  
Objective: Read pc informations like cpu load and temperature, send to a database and deliver to a frontend with django api.  
  
Backend: Python Django REST Framework (DRF)  
Database used during development: PostgreSQL (Diff of default scheme below)  

### Database
```sql
CREATE TABLE public.accounts_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id uuid NOT NULL, --Change of default id from django to uuid
    email character varying(254) NOT NULL --Change to required and not null on django ORM
);

CREATE TABLE public.pcdata_pcdata (
    id uuid NOT NULL,
    cpu_json jsonb, --CPU info (Structure below)
    gpu_json jsonb, --GPU info (Structure below)
    memory_json jsonb, --Memory info (Structure below)
    "timestamp" timestamp with time zone NOT NULL, --Timestamp of data
    pc_id uuid NOT NULL --Owner of data (CONSTRAINT)
);

CREATE TABLE public.pcdata_pcinfo (
    id uuid NOT NULL,
    name character varying(140) NOT NULL,
    other_info text,
    os text,
    is_active boolean NOT NULL,
    date_added timestamp with time zone NOT NULL,
    user_id uuid NOT NULL --UUID of owner user (CONSTRAINT)
);

```
### JSON of PC Data
```json
        "cpu_json": {
            "Intel Core i7-9700KF": {
                "Load": {
                    "CPU Total": 21.266311645507812, -required
                    "CPU Core #1": 30.075496673583984,
                    "CPU Core #2": 29.545486450195312,
                    "CPU Core #3": 20.072101593017578,
                    "CPU Core #4": 16.466581344604492,
                    "CPU Core #5": 23.193920135498047,
                    "CPU Core #6": 18.42749786376953,
                    "CPU Core #7": 14.665931701660156,
                    "CPU Core #8": 17.683446884155273,
                    "CPU Core Max": 30.075496673583984
                },
                "Clock": {
                    "Bus Speed": 100.0000228881836,
                    "CPU Core #1": 4700.0009765625,
                    "CPU Core #2": 4700.0009765625,
                    "CPU Core #3": 4700.0009765625,
                    "CPU Core #4": 4700.0009765625,
                    "CPU Core #5": 4700.0009765625,
                    "CPU Core #6": 4700.0009765625,
                    "CPU Core #7": 4700.0009765625,
                    "CPU Core #8": 4700.0009765625
                },
                "Power": {
                    "CPU Cores": 29.602476119995117,
                    "CPU Memory": 0.0,
                    "CPU Package": 32.890174865722656
                },
                "Voltage": {
                    "CPU Core": 1.281982421875,
                    "CPU Core #1": 1.3170166015625,
                    "CPU Core #2": 1.238037109375,
                    "CPU Core #3": 1.2266845703125,
                    "CPU Core #4": 1.2271728515625,
                    "CPU Core #5": 1.223876953125,
                    "CPU Core #6": 1.268798828125,
                    "CPU Core #7": 1.2838134765625,
                    "CPU Core #8": 1.2547607421875
                },
                "Temperature": {
                    "Core Max": 37.0, -required
                    "CPU Core #1": 37.0,
                    "CPU Core #2": 36.0,
                    "CPU Core #3": 36.0,
                    "CPU Core #4": 35.0,
                    "CPU Core #5": 35.0,
                    "CPU Core #6": 36.0,
                    "CPU Core #7": 35.0,
                    "CPU Core #8": 35.0,
                    "CPU Package": 37.0,
                    "Core Average": 35.625, -required
                    "CPU Core #1 Distance to TjMax": 63.0,
                    "CPU Core #2 Distance to TjMax": 64.0,
                    "CPU Core #3 Distance to TjMax": 64.0,
                    "CPU Core #4 Distance to TjMax": 65.0,
                    "CPU Core #5 Distance to TjMax": 65.0,
                    "CPU Core #6 Distance to TjMax": 64.0,
                    "CPU Core #7 Distance to TjMax": 65.0,
                    "CPU Core #8 Distance to TjMax": 65.0
                }
            }
        },
        "gpu_json": {
            "NVIDIA GeForce RTX 2060 SUPER": {
                "Fan": {
                    "GPU Fan": 1059.0
                },
                "Load": {
                    "D3D 3D": 15.895452499389648, -required
                    "D3D VR": 0.0,
                    "GPU Bus": 6.0,
                    "D3D Copy": 0.0058392793871462345,
                    "D3D Cuda": 0.0,
                    "GPU Core": 14.0,
                    "GPU Power": 11.307000160217285,
                    "GPU Memory": 19.04749870300293, -required
                    "D3D Overlay": 0.0,
                    "D3D Security": 0.0,
                    "D3D Compute_0": 9.207598686218262,
                    "D3D Compute_1": 0.0,
                    "D3D Graphics_1": 0.0,
                    "GPU Board Power": 16.017000198364258,
                    "D3D Video Decode": 3.0686252117156982,
                    "D3D Video Encode": 44.69002151489258,
                    "GPU Video Engine": 44.0,
                    "GPU Memory Controller": 9.0
                },
                "Clock": {
                    "GPU Core": 525.0,
                    "GPU Memory": 405.0
                },
                "Power": {
                    "GPU Package": 20.80500030517578
                },
                "Control": {
                    "GPU Fan": 29.0
                },
                "SmallData": {
                    "GPU Memory Free": 6631.0,
                    "GPU Memory Used": 1560.0,
                    "GPU Memory Total": 8192.0,
                    "D3D Shared Memory Used": 155.04296875,
                    "D3D Dedicated Memory Used": 1382.75
                },
                "Throughput": {
                    "GPU PCIe Rx": 3020800.0,
                    "GPU PCIe Tx": 211507200.0
                },
                "Temperature": {
                    "GPU Core": 38.0, -required
                    "GPU Hot Spot": 49.875
                }
            }
        },
        "memory_json": {
            "Generic Memory": {
                "Data": {
                    "Memory Used": 9.523857116699219,
                    "Memory Available": 6.392730712890625,
                    "Virtual Memory Used": 15.398792266845703,
                    "Virtual Memory Available": 4.398708343505859
                },
                "Load": {
                    "Memory": 59.8360481262207, -required
                    "Virtual Memory": 77.781494140625
                }
            }
        },
```



# ROUTES AVAILABLE
Developed routes until now

## User routes: 
register/  

account/  
account/<uuid:pk>/  
account/resetpassword/ (In progress)  

### PC routes:
pc/  
pc/active/  
pc/<uuid:pk>/  

### Data routes:
pc/<uuid:pk>/data/  

### CPU Data
pc/<uuid:pk>/data/cpu/  

pc/<uuid:pk>/data/cpu/load/  
pc/<uuid:pk>/data/cpu/load/avr/  
pc/<uuid:pk>/data/cpu/load/avr/?time=30  

pc/<uuid:pk>/data/cpu/temp/  
pc/<uuid:pk>/data/cpu/temp/avr/  
pc/<uuid:pk>/data/cpu/temp/avr/?time=30  

pc/<uuid:pk>/data/cpu/temp/max/  
pc/<uuid:pk>/data/cpu/temp/max/?time=30  

### MEMORY Data
pc/<uuid:pk>/data/memory/  
pc/<uuid:pk>/data/memory/avr/  
pc/<uuid:pk>/data/memory/avr/?time=30  

### GPU Data
pc/<uuid:pk>/data/gpu/  

pc/<uuid:pk>/data/gpu/temp/  
pc/<uuid:pk>/data/gpu/temp/avr/  
pc/<uuid:pk>/data/gpu/temp/avr/?time=30  

pc/<uuid:pk>/data/gpu/load/  
pc/<uuid:pk>/data/gpu/load/avr/  
pc/<uuid:pk>/data/gpu/load/avr/?time=30  

pc/<uuid:pk>/data/gpu/memory/  
pc/<uuid:pk>/data/gpu/memory/avr/  
pc/<uuid:pk>/data/gpu/memory/avr/?time=30  
