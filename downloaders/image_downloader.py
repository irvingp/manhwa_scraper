import aiohttp
import asyncio
import os

class ImageDownloader:
    async def _fetch_image(self, session, url, output_dir, retries=3):
        file_name = os.path.basename(url).replace("/", "_")
        file_path = os.path.join(output_dir, file_name)

        for attempt in range(retries):
            try:
                async with session.get(url, timeout=60) as resp:
                    resp.raise_for_status()
                    with open(file_path, 'wb') as f:
                        f.write(await resp.read())
                #print(f"✅ Imagen descargada: {file_name}")
                return file_path
            except Exception as e:
                print(f"⚠️ Error descargando {url}: {e} (Intento {attempt+1}/{retries})")
                await asyncio.sleep(2)  # espera antes de reintentar

        print(f"❌ Falló la descarga tras {retries} intentos: {url}")
        return None

    async def download_images(self, urls, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_image(session, url, output_dir) for url in urls]
            downloaded_files = await asyncio.gather(*tasks)

        return [f for f in downloaded_files if f]

    def download_chapter_images(self, urls, output_dir):
        return asyncio.run(self.download_images(urls, output_dir))
