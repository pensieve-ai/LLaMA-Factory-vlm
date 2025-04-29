from llamafactory.chat import ChatModel

# Initialize model
model_args = {
    "model_name_or_path": "Qwen/Qwen2.5-VL-7B-Instruct",
    "adapter_name_or_path": "saves/qwen2.5_vl-7b/lora/sft/checkpoint-9",
    "template": "qwen2_vl",
    "trust_remote_code": True
}

# Pass the args dictionary to ChatModel
chat_model = ChatModel(model_args)

# Text-only query
response = chat_model.chat([{"role": "user", "content": "Tell me about this picture"}])
print(response)

# For images (since this is a VL model)
import base64
with open("/home/yoonseok-yang/images/2e449553-d1e9-4f72-8292-98970f70aab9.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

image_url = f"data:image/jpeg;base64,{encoded_image}"
response = chat_model.chat(
    [{"role": "user", "content": "What's in this image?"}], 
    images=[image_url]
)
print(response)