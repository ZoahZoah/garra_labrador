import socketio
from garra import Garra

garra = Garra()
sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': './static/'
})

last_key = {}


@sio.event
async def connect(sid, environ):
    print(sid, 'connected')

@sio.event
async def disconnect(sid):
    print(sid, 'disconnected')

@sio.event
async def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    await sio.emit('sum_result', {'result': result}, to=sid)        

@sio.event
async def key_up(sid, data):
    await sio.emit('key_up', to=sid)
    garra.stop_claw()

@sio.event
async def key_pressed(sid, data):
    key = data['key']
    another_key = last_key.get(sid)
    if key != another_key:
        print(f'Tecla recebida do cliente {sid}: {key}')
    await sio.emit('key_pressed', key, to=sid)
    moving_claw(key)
    last_key[sid] = key

def moving_claw(key):
    if key == 'w':
        garra.foward_claw()
    elif key == 's':
        garra.backward_claw()
    elif key == 'a':
        garra.stretch_claw()
    elif key == 'd':
        garra.retract_claw()
    elif key == 'ArrowUp':
        garra.uplift()
    elif key == 'ArrowDown':
        garra.lower()
    elif key == 'ArrowLeft':
        garra.turn_left()
    elif key == 'ArrowRight':    
        garra.turn_right()  