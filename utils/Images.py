import base64
import aiohttp
import io

async def generate_images(prompt: str, negative_prompts: str, config, steps, batch) -> list:
    async with aiohttp.ClientSession(headers=config['CUSTOM_HEADERS']) as session:
        async with session.post(url=f"{config['BACKEND_URL']}/sdapi/v1/txt2img", json={'prompt': prompt, 'negative_prompt': negative_prompts, 'steps': steps, 'batch_size': batch}) as response:
            if response.status == 200:
                response_data = await response.json()
                images = [io.BytesIO(base64.decodebytes(bytes(image, 'utf-8')))
                          for image in response_data['images']]
                return images
            else:
                return None