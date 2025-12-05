# Summary Publication – Automação de Publicações Jurídicas

Automação completa para coleta, sumarização e envio de publicações jurídicas, integrada ao ecossistema Google Cloud.  
O projeto executa coleta diária, processamento inteligente com IA e envio automático por e-mail.

---

## 🚀 Tecnologias

- **Python 3.13**
- **FastAPI**
- **Google Cloud Run**
- **Cloud Scheduler**
- **Cloud Tasks**
- **Firestore**
- **GitHub Actions**
- **Docker**
- **Gemini API**
- **OpenIA**
- **Pandas**

---

## 🔄 Fluxo de Execução

1. **Cloud Scheduler** dispara diariamente.
2. Cada job roda no **Cloud Run**, processando:
   - Coleta das publicações (Astrea)
   - Sumarização com Gemini (ou OpenIA)
   - Criação do payload final
3. **Email Job** dispara o envio automático com excel.

---
