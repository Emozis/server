class Constants:
    SQL_FOLDER_PATH = "app/resources/sql"

    GEMINI_MODEL="gemini-1.5-flash"
    TEMPLATE_PATH="app/resources/prompts/Demo.prompt"
    TEMPERATURE=0.7

    chatbot={"model": 'gpt-4o-mini', "temperature": 0.5}

    # DB settings
    POOL_SIZE=10
    MAX_OVERFLOW=5

constants = Constants()