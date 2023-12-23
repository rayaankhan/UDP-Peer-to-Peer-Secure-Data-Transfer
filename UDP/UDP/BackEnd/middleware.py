from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dfs_server_sender import send_data
from dfs_server_receiver import receive_data
import socket

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend's actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Welcome to the FastAPI app!"

@app.post("/middleware")
async def middleware(data: dict):
    # Use a connected socket to get the local IP address
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect(("8.8.8.8", 80))  # Connect to a public IP address
    client_ip = client_socket.getsockname()[0]
    client_socket.close()

    print("Sender's IP:", client_ip)
    
    try:
        flag = data.get("flag")
        if flag == 1:
            print("mid: sender chal rha hai")
            with open('my_ip.txt', 'w') as file:
                file.write(client_ip)
            password = data.get("password")
            file_name = data.get("file_name")
            room_cap = data.get("room_cap")
            print("mid: room_cap_val",room_cap)
            response_data = {"password": password, "file_name": file_name, "ip_file": 'my_ip.txt',"flag":flag,"room_cap":room_cap}
            print("mid: sender chal gya!")
            result = send_data(response_data)
        elif flag == 2:
            with open('my_ip.txt', 'w') as file:
                file.write(client_ip)
            password = data.get("password")
            response_data = {"password": password, "ip_file": 'my_ip.txt',"flag":flag}
            result = receive_data(response_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
