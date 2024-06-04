const sio = io()

sio.on('connect', () => {
    console.log('connected');
});

sio.on('disconnect', () => {
    console.log('disconnected');
});


sio.on('sum_result', (data) => {
    console.log(data);
});

sio.on('key_W_pressed', (key) => {
    console.log(key);
});

document.addEventListener('keydown', (event) => {
    const keyPressed = event.key;
    sio.emit('key_pressed', { key: keyPressed }); // Envia a tecla para o servidor
});
