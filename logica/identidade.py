import streamlit as st
import uuid


def obter_usuario_id() -> str:
    """
    Retorna um ID único para o usuário/dispositivo atual.
    - Salva no session_state (persiste durante a sessão).
    - Salva na URL via query_params (persiste se o usuário salvar o link ou recarregar).
    - Se não existir, gera um novo UUID.
    """
    # 1. Já temos na sessão? Usa esse.
    if "usuario_id" in st.session_state:
        return st.session_state.usuario_id

    # 2. Tem na URL? Recupera e salva na sessão.
    params = st.query_params
    if "uid" in params:
        uid = params["uid"]
    else:
        # 3. Não tem em lugar nenhum. Gera um novo.
        uid = str(uuid.uuid4())
        st.query_params["uid"] = uid

    st.session_state.usuario_id = uid
    return uid