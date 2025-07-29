import aiohttp
import asyncio
import os

class ImageDownloader:
    async def _fetch_image(self, session, url, save_path):
        async with session.get(url) as resp:
            resp.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(await resp.read())
        return save_path

    async def download_images(self, urls, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for idx, url in enumerate(urls):
                ext = os.path.splitext(url)[1]
                save_path = os.path.join(output_dir, f"{idx:03d}{ext}")
                tasks.append(self._fetch_image(session, url, save_path))
            
            downloaded_files = await asyncio.gather(*tasks)
            return sorted(downloaded_files)

    def download_chapter_images(self, urls, output_dir):
        return asyncio.run(self.download_images(urls, output_dir))
