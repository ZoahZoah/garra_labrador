const sio = io()
const buttons = document.querySelectorAll('.keys button');
let isKeyPressed = false; 

sio.on('connect', () => {
    console.log('connected');
});

sio.on('disconnect', () => {
    console.log('disconnected');
});

document.addEventListener('keyup', (event) => {
    sio.emit('key_up', {});
    buttons.forEach(button => {
        if (button.dataset.key === event.key) {
            button.classList.remove('active'); // Remove a classe 'active'
        }});
    isKeyPressed = false;
});

document.addEventListener('keydown', (event) => {
    if (!isKeyPressed) {
        const keyPressed = event.key;
        console.log(keyPressed);
        
        buttons.forEach(button => {
            console.log(button.dataset.key);
            if (button.dataset.key === event.key) {
                
                button.classList.add('active'); // Adiciona a classe 'active'
            }});
        sio.emit('key_pressed', { key: keyPressed }); // Envia a tecla para o servidor
        isKeyPressed = true;
}});
