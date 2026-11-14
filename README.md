# Knowledge-Intelligence-System


# How to run?

### STEPS:


### STEP 01 - Create a Conda environment after opening the repository

```bash
conda create -n llmapp python=3.11 -y
```

```bash
conda activate llmapp
```

### STEP 02 - Configure the Gemini API key

Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey), then create a `.env` file in the repository root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Keep the key private and do not commit `.env`. The app uses Gemini for both chat (`gemini-3.8-flash`) and embeddings (`gemini-embedding-001`). You can override these defaults with `GEMINI_CHAT_MODEL` and `GEMINI_EMBEDDING_MODEL`.

The Gemini free tier has usage limits, and Google may use free-tier content to improve its products. Review Google's [API pricing](https://ai.google.dev/gemini-api/docs/pricing) and [terms](https://ai.google.dev/gemini-api/terms) before uploading sensitive documents.

The app stores Gemini vectors in a separate collection; re-upload your documents after switching so they are indexed with Gemini embeddings.

### STEP 03 - Install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
python app/main.py
```