document.getElementById('createAutomataForm').addEventListener('submit', function (event) {
    event.preventDefault();

    let transitions;
    try {
        transitions = JSON.parse(document.getElementById('transitions').value);
    } catch (e) {
        document.getElementById('result').innerHTML = `
            <p style="color: red;">Erro no formato das transições: ${e.message}</p>
        `;
        return;
    }

    const formData = {
        type: document.getElementById('type').value,
        config: {
            states: document.getElementById('states').value.split(',').map(s => s.trim()),
            input_symbols: document.getElementById('input_symbols').value.split(',').map(s => s.trim()),
            transitions: transitions,
            initial_state: document.getElementById('initial_state').value.trim(),
            final_states: document.getElementById('final_states').value.split(',').map(s => s.trim())
        }
    };

    fetch('http://localhost:8000/automata/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => Promise.reject(err));
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('result').innerHTML = `
            <h2>Autômato Criado sem Sucesso!</h2>
            <p><strong>Tipo:</strong> ${data.type}</p>
            <p><strong>Configuração:</strong> <pre>${JSON.stringify(data.config, null, 2)}</pre></p>
            <h3>Imagem do Autômato:</h3>
            <img src="${data.image_url}" alt="Imagem do autômato gerado" style="max-width: 100%; border: 1px solid #ccc;" />
        `;
    })
    .catch(error => {
        console.error('Error:', error); 
        document.getElementById('result').innerHTML = `
            <p style="color: red;">Erro: ${error.detail || error.message || 'Erro desconhecido'}</p>
        `;
    });
});


document.getElementById('validateStringForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const inputString = document.getElementById('inputString').value;
    console.log('Sending data:', { input_string: inputString });
    
    fetch('http://localhost:8000/automata/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            input_string: inputString 
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('validationResult').innerHTML = `
            <h2>Resultado da Validação</h2>
            <p><strong>String:</strong> ${data.input}</p>
            <p><strong>Aceita:</strong> ${data.accepted ? "Sim ✅" : "Não ❌"}</p>
        `;
    })
    .catch(error => {
        document.getElementById('validationResult').innerHTML = `<p style="color: red;">Erro: ${error.message}</p>`;
    });
});

