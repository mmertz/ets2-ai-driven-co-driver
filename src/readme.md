# Config Section

The `config` section of the `src/co_driver_profiles.json` file allows you to configure various providers and their settings for different functionalities such as text-to-text, text-to-audio, image-to-text, and dynamic co-driver.

## Text-to-Text

The `text_to_text` section configures the provider and settings for text-to-text functionality.

Example:```
"text_to_text": {
"provider": "openai",
"model_id": "gpt-3.5-turbo",
"temperature": 0.9
}```


Mistral replicate: ```
"text_to_text": {
    "provider": "replicate",
    "model_id": "mistralai/mixtral-8x7b-instruct-v0.1",
    "history_size": 5,
    "is_stream": true,
    "params": {
        "top_k": 50,
        "top_p": 0.9,
        "prompt": "{{text}}",
        "temperature": 1,
        "system_prompt": "{{system}}",
        "length_penalty": 1,
        "max_new_tokens": 1024,
        "prompt_template": "<s>[INST] {prompt} [/INST] ",
        "presence_penalty": 0
    }
},```


## Text-to-Audio

The `text_to_audio` section configures the provider and settings for text-to-audio functionality.

Arnold with replicate
JSON:```"text_to_audio": {
"provider": "replicate",
"model_id": "lucataco/xtts-v2:684bc3855b37866c0c65add2ff39c78f3dea3f4ff103a436465326e0f438d55e",
"params": {
"text": "{{text}}",
"language": "en",
"cleanup_voice": false,
"speaker": "https://racingleaguehub.s3.eu-west-2.amazonaws.com/stogie.mp3"
}
}```


Openai: ```"text_to_audio": {
    "provider": "openai",
    "model_id": "tts-1"
},```

edge tts(free): ```
"text_to_audio": {
    "provider": "microsoft_edge",
    "params": {
        "voice": "en-US-AndrewMultilingualNeural"
    }
},```


## Image-to-Text

The `image_to_text` section configures the provider and settings for image-to-text functionality.

Example:```
"image_to_text": {
"provider": "openai",
"model_id": "toonify",
"params": {
"api_key": "your-api-key"
}
}```


## Dynamic Co-Driver

The `dynamic_co_driver` section configures the provider and settings for the dynamic co-driver functionality.

Example:```
"dynamic_co_driver_nlp_example": {
"provider": "nlp"
}```