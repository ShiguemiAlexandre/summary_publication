import streamlit as st
from gemini.credencials import Credencials
from db.prompt import PromptsRefsFirestore
from model.system import System

class TabUpdatePrompt:
    def __init__(self):
        self.refs_prompts = PromptsRefsFirestore()
        self.type_sytems = System.ALL_SYSTEMS.value

    def _header(self):
        st.subheader("Atualizar prompt", divider=True)

    def _sub_header(self):
        cols = st.columns([1, 1])

        self.name_client = cols[0].text_input(
            label="Nome do cliente",
            value="franco"
        )
        self.type_system = cols[1].multiselect(
            label="Sistema",
            placeholder="Selecione o sistema",
            options=self.type_sytems,
            max_selections=1
        )[0]

        if not self.type_system:
            st.warning("Selecione o tipo do sistema")
            st.stop()

        with st.expander("Prompt atual", icon=":material/text_format:"):
            ref_last_prompt = self.refs_prompts.get_last_prompt_created(
                name_client=self.name_client,
                type_system=self.type_system
            )

            if not ref_last_prompt.get():
                st.warning("Nenhum prompt cadastrado")
                st.stop()

            self.text_prompt = ref_last_prompt.get()[0].to_dict()["prompt"]

            st.write(self.text_prompt)

    def _form_update_new_prompt(self):
        with st.form("new_prompt"):
            height = max(68, len(self.text_prompt) // 4)
            text = st.text_area("Prompt", value=self.text_prompt, height=height)

            data = {"prompt": text}

            if st.form_submit_button("Atualizar"):
                with st.spinner(":blue[Atualizando...]"):
                    result = self.refs_prompts.create_new_prompt(
                        name_client=self.name_client,
                        type_system=self.type_system,
                        **data
                    )
                if not result:
                    st.error("Ocorreu algum erro, contate o suporte")
                    st.stop()
                st.rerun()

    def render(self):
        self._header()
        self._sub_header()

        self._form_update_new_prompt()

ref_prompt = PromptsRefsFirestore()

tab_IA, tab_update_prompt = st.tabs([":material/robot: IA", ":material/edit: Atualizar prompt"])

with tab_update_prompt:
    TabUpdatePrompt().render()

with tab_IA:
    st.subheader("Teste de prompt", divider=True)

    txt_input = st.text_input(
        "Prompt",
        help="Digite o prompt para a API da IA",
    )

    options_model = st.selectbox(
        label="Modelo da IA",
        options=[
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ],
        placeholder="Selecione um modelo",
        index=2
    )

    if st.button("Gerar"):
        if not txt_input.strip():
            st.warning("Digite um prompt antes de gerar a resposta.")
        else:
            with st.spinner("Gerando resposta..."):
                credenciais = Credencials()
                gemini_model = credenciais.login(model_name=options_model)
                response_txt = gemini_model.generate_content(txt_input)

                st.divider()
                st.metric(
                    label="Token utilizado",
                    value=response_txt.usage_metadata.total_token_count
                )
                st.text(response_txt.text)
                st.toast(":green[:material/check: Gerado com sucesso]")

                with st.expander("Mais detalhes"):
                    st.json(response_txt.to_dict())
