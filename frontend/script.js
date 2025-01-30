document.getElementById('createAutomataForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = {
        type: document.getElementById('type').value,
        config: {
            states: document.getElementById('states').value.split(','),
            input_symbols: document.getElementById('input_symbols').value.split(','),
            transitions: JSON.parse(document.getElementById('transitions').value),
            initial_state: document.getElementById('initial_state').value,
            final_states: document.getElementById('final_states').value.split(',')
        }
    };

    fetch('http://localhost:8000/automata/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `
            <h2>Autômato Criado com Sucesso!</h2>
            <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Tipo:</strong> ${data.type}</p>
            <p><strong>Configuração:</strong> <pre>${JSON.stringify(data.config, null, 2)}</pre></p>
        `;
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<p style="color: red;">Erro: ${error.message}</p>`;
    });
});

// Adiciona funcionalidade para buscar um autômato pelo ID
document.getElementById('getAutomataForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const automataId = document.getElementById('automata_id').value;
    
    fetch(`http://localhost:8000/automata/${automataId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Autômato não encontrado');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('result').innerHTML = `
            <h2>Detalhes do Autômato</h2>
            <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Tipo:</strong> ${data.type}</p>
            <p><strong>Configuração:</strong> <pre>${JSON.stringify(data.config, null, 2)}</pre></p>
            <img src="http://localhost:8000/automata/${data.id}/image" alt="Visualização do Autômato" style="max-width:100%; margin-top: 10px;">
        `;
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<p style="color: red;">Erro: ${error.message}</p>`;
    });
});
