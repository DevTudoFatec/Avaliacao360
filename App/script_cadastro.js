const formulario = document.querySelector('#formulario');

formulario.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(formulario);
    const data = {}

    for (let [key,value] of formData.entries()) {
        data[key] = value;
    }

    const json = JSON.stringify(data)

    console.log (json);
})