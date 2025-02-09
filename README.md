## 💻 Como rodar
1. Clone o repositório:
    ```bash
    git clone https://github.com/JoseJaan/automata
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv\bin\activate
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
4. Execute a API
    ```bash
    uvicorn main:app --reload
5. A API é executada em `localhost:8000`. Em `localhost:8000/docs`, encontra-se a documentação dos endpoints.
