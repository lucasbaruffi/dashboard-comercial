A seguir, um passo a passo para gerar as credenciais (arquivo JSON) utilizando uma Conta de Serviço no Google Cloud:

1. **Acesse o Google Cloud Console:**  
   Entre no [Google Cloud Console](https://console.cloud.google.com/) e faça login com sua conta Google.

2. **Crie ou selecione um projeto:**  
   Se você ainda não tem um projeto, clique em "Selecionar projeto" na barra superior e depois em "Novo Projeto". Dê um nome ao projeto e clique em "Criar".

3. **Habilite as APIs necessárias:**  
   - No menu lateral, vá em **APIs e Serviços > Biblioteca**.  
   - Procure por **Google Sheets API** e **Google Drive API** e clique em “Ativar” para cada uma delas.

4. **Crie uma Conta de Serviço:**  
   - No menu lateral, acesse **IAM e Administração > Contas de Serviço**.  
   - Clique em **Criar Conta de Serviço**.  
   - Informe um nome e, se desejar, uma descrição para a conta de serviço. Clique em **Criar**.
   - Na etapa de concessão de permissões (opcional), você pode pular ou configurar as permissões conforme sua necessidade. Clique em **Continuar** e depois em **Concluído**.

5. **Gere a chave da Conta de Serviço:**  
   - Na lista de contas de serviço, localize a conta recém-criada e clique nela para acessar os detalhes.  
   - Vá na aba **Chaves** e clique em **Adicionar Chave > Criar Nova Chave**.  
   - Selecione o formato **JSON** e clique em **Criar**.  
   - O arquivo de credenciais será baixado automaticamente para o seu computador.

6. **Proteja e utilize o arquivo de credenciais:**  
   - Coloque o arquivo (por exemplo, `credentials.json`) em um local seguro do seu projeto.  
   - Lembre-se de adicioná-lo ao **.gitignore** para evitar que seja versionado (veja instruções anteriores).

7. **Compartilhe a planilha com a Conta de Serviço:**  
   - Abra sua planilha no Google Sheets e clique em **Compartilhar**.  
   - Adicione o e-mail da Conta de Serviço (geralmente no formato `nome-da-conta@nome-do-projeto.iam.gserviceaccount.com`) para que a conta tenha acesso à planilha.

Com esses passos, você terá gerado as credenciais necessárias para autenticar sua aplicação Python com a API do Google Sheets. Agora você poderá utilizar bibliotecas como **gspread** para manipular suas planilhas programaticamente.