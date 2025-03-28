def iniciarPrograma():

    from logging_config import configurar_logging
    from auth import ghlAuthorization
    from meetings import getMeetings
    from database import Database
    from users import getUsers
    from calendars import getCalendars
    from contactCustomFields import getContactsCustomFields
    from contacts import getContacts
    from opportunityCustomFiels import getOpportunitiesCustomFields
    from pipelines import getPipelines
    from opportunities import getOpportunities
    
    # Configura o logger (Obrigatório em todos os arquivos)
    logger = configurar_logging()
    
    if __name__ == "__main__":
        try:
            logger.info("Aplicação Iniciada")
            
            # Inicializa conexão com banco
            Database.initialize()
            
            # Faz a autenticação com o GHL
            ghlAuthorization()
            
            # Busca usuários
            getUsers()
    
            # Busca calendários
            getCalendars()
    
            # Busca campos personalizados do contato
            getContactsCustomFields()
    
            # Busca contatos
            getContacts()
    
            # Busca campos personalizados da oportunidade
            getOpportunitiesCustomFields()
    
            # Busca pipelines
            getPipelines()
    
            # Busca oportunidades
            getOpportunities()
    
            # Busca reuniões
            getMeetings()
    
            logger.info("Programa finalizado com sucesso")
        
        except Exception as e:
            logger.error(f"Erro crítico: {e}")
            logger.critical("Programa finalizado com erro")

iniciarPrograma()
