import aiohttp
import asyncio

async def check_channel(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                return url
    except:
        return None

async def check_and_filter_m3u(m3u_url, output_file='working_playlist.m3u'):
    async with aiohttp.ClientSession() as session:
        response = await session.get(m3u_url)
        if response.status != 200:
            print(f"Ошибка: Не удалось загрузить плейлист. Код статуса: {response.status}")
            return

        lines = (await response.text()).splitlines()
        working_lines = []

        tasks = []
        for line in lines:
            if line.startswith('http'):
                tasks.append(check_channel(session, line))
            else:
                working_lines.append(line)

        results = await asyncio.gather(*tasks)
        working_lines.extend(filter(None, results))

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("\n".join(working_lines))
        print(f"Рабочие каналы сохранены в файл: {output_file}")

if __name__ == "__main__":
    m3u_url = "http://dmitry-tv.ddns.net/iptv/freesat/gtmedia/Playlist-01/custom_url.m3u"
    asyncio.run(check_and_filter_m3u(m3u_url))
