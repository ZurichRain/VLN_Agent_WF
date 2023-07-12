import torch
import clip
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("/home/zhhz/sxu/fw_project/pretrained_model/CLIP/ViT-B/32/pytorch_model.bin", device=device)

model = CLIPModel.from_pretrained("/home/zhhz/sxu/fw_project/pretrained_model/CLIP/ViT-B/32/").to(device)
preprocess = CLIPProcessor.from_pretrained("/home/zhhz/sxu/fw_project/pretrained_model/CLIP/ViT-B/32/")

# image = preprocess(Image.open("fw_project/VLN_bert/0.jpg")).unsqueeze(0).to(device)
image = Image.open("fw_project/VLN_bert/0.jpg")

candidate_text = ["a photo of a window", "a photo of a dog", "a photo of a cat", "a photo of painting"]

inputs = preprocess(text=candidate_text,\
                     images=image, return_tensors="pt", padding=True).to(device)
# text = clip.tokenize(["a photo of a dog", "a photo of a dog", "a photo of a cat", "a photo of painting"]).to(device)
# print(inputs)
outputs = model(**inputs)
# print(outputs.keys())
# print(outputs.text_model_output.last_hidden_state.size())
# print(outputs.text_embeds.size())
print(outputs.logits_per_text.softmax(dim=0))
probs = torch.argmax(outputs.logits_per_text.softmax(dim=0),dim=0)
# print(probs)
print(candidate_text[probs])
exit()
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]